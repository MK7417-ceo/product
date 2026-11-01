"""Inbound adapter (HTTP): practice router — daily questions + aaj ka plan."""
from __future__ import annotations

import ast
import re
import uuid
from dataclasses import asdict
from datetime import date as date_cls

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.adapters.inbound.dsa_service import get_daily_dsa
from app.adapters.outbound.dsa_bank import get_problem, get_problems, list_topics
from app.api.v1.auth import _domain_error, current_user_id
from app.domain.user import DomainError
from app.ports.outbound import CodeEngineError

router = APIRouter(prefix="", tags=["practice"])


# ---- DSA function-contract harness (P0-2) ----
# Problems ship a function starter (e.g. "def sum_n(n: int) -> int:") and
# examples written as assignments ("n = 5"). The old harness ran submitted
# code as a raw stdin/stdout script, so a correct function solution printed
# nothing and always scored 0/2. When a problem has a plain top-level
# Python function contract AND every example parses as assignments for its
# parameters, the harness instead appends a driver that calls the function
# with the example inputs and compares the return value (or, for
# None-returning functions, the mutated argument or captured stdout).
# Anything else (class-based starters, linked-list/tree inputs, non-Python
# languages, unparsable examples) keeps the previous stdin/stdout behavior.

_TOP_DEF_RE = re.compile(r"^def\s+([A-Za-z_]\w*)\s*\(([^)]*)\)", re.M)
_CLASS_DEF_RE = re.compile(r"^class\s+\w+", re.M)
_ASSIGN_RE = re.compile(r"^([A-Za-z_]\w*)\s*=\s*(.+)$", re.S)
_RESULT_MARKER = "__SF_RESULT__:"
_STDOUT_MARKER = "__SF_STDOUT__"


def _split_top_level(text: str) -> list[str]:
    """Split on top-level commas (ignoring commas inside []/()/{} and strings)."""
    parts, depth, quote, buf = [], 0, "", ""
    i = 0
    while i < len(text):
        ch = text[i]
        if quote:
            buf += ch
            if ch == "\\" and i + 1 < len(text):
                buf += text[i + 1]
                i += 2
                continue
            if ch == quote:
                quote = ""
        elif ch in "\"'":
            quote, buf = ch, buf + ch
        elif ch in "[({":
            depth, buf = depth + 1, buf + ch
        elif ch in "])}":
            depth, buf = depth - 1, buf + ch
        elif ch == "," and depth == 0:
            parts.append(buf)
            buf = ""
        else:
            buf += ch
        i += 1
    if buf.strip():
        parts.append(buf)
    return parts


def _parse_literal(text: str):
    """Parse a Python literal, tolerating JSON-style true/false/null."""
    t = text.strip()
    low = t.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low == "null":
        return None
    return ast.literal_eval(re.sub(r"\bnull\b", "None", t))


def _function_contract(problem, language: str):
    """Return (fn_name, param_names) if the problem has a usable Python
    function contract, else None. All examples must parse as assignments
    whose names exactly match the parameters."""
    if language != "python":
        return None
    starter = (problem.starter_code or {}).get("python", "")
    if not starter or _CLASS_DEF_RE.search(starter) or "class " in starter:
        return None  # class-based problem (Stack/Queue) or a node class the
        # driver cannot construct (ListNode/TreeNode): no plain function
    m = _TOP_DEF_RE.search(starter)
    if not m:
        return None
    params = []
    for raw in _split_top_level(m.group(2)):
        raw = raw.strip()
        if not raw or raw.startswith(("*", "**")):
            return None
        name = re.split(r"[:=]", raw, 1)[0].strip()
        if not re.fullmatch(r"[A-Za-z_]\w*", name):
            return None
        params.append(name)
    if not params:
        return None
    for ex in problem.examples or []:
        names = set()
        for part in _split_top_level(str(ex.get("input", ""))):
            am = _ASSIGN_RE.match(part.strip())
            if not am:
                return None
            try:
                _parse_literal(am.group(2))
            except Exception:
                return None  # e.g. "head = 1 -> 2 -> 3", tree annotations
            names.add(am.group(1))
        if names != set(params):
            return None
    return m.group(1), params


def _driver_code(user_code: str, fn_name: str, param_names: list[str],
                 example_input: str) -> str:
    """User code + driver that calls fn with this example's inputs and
    prints a marker line carrying the outcome."""
    args = {}
    for part in _split_top_level(example_input):
        am = _ASSIGN_RE.match(part.strip())
        args[am.group(1)] = _parse_literal(am.group(2))
    arg_exprs = ", ".join(repr(args[p]) for p in param_names)
    return (
        user_code
        + "\n\nimport copy as _sf_copy, io as _sf_io, contextlib as _sf_ctx\n"
        + f"_sf_args = [{arg_exprs}]\n"
        + "_sf_before = _sf_copy.deepcopy(_sf_args)\n"
        + "_sf_buf = _sf_io.StringIO()\n"
        + "_sf_result = None\n"
        + "with _sf_ctx.redirect_stdout(_sf_buf):\n"
        + f"    _sf_result = {fn_name}(*_sf_args)\n"
        + "if _sf_result is None:\n"
        + "    _sf_mut = next((_sf_a for _sf_a, _sf_b in zip(_sf_args, _sf_before)"
        + " if _sf_a != _sf_b), None)\n"
        + "    if _sf_mut is not None:\n"
        + f"        print({_RESULT_MARKER!r} + repr(_sf_mut))\n"
        + "    else:\n"
        + f"        print({_STDOUT_MARKER!r})\n"
        + "        print(_sf_buf.getvalue(), end='')\n"
        + "else:\n"
        + f"    print({_RESULT_MARKER!r} + repr(_sf_result))\n"
    )


def _extract_actual(stdout: str) -> str:
    """Pull the driver's outcome out of stdout, ignoring any stray prints
    from the submitted code itself."""
    lines = stdout.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(_RESULT_MARKER):
            return line[len(_RESULT_MARKER):].strip()
        if line == _STDOUT_MARKER:
            return "\n".join(lines[i + 1:]).strip()
    return stdout.strip()


def _parsed_value(text: str):
    """(value, ok) — literal parse with true/false/null tolerated."""
    try:
        return _parse_literal(text), True
    except Exception:
        return None, False


def _values_equal(actual: str, expected: str) -> bool:
    a, a_ok = _parsed_value(actual.strip())
    e, e_ok = _parsed_value(expected.strip())
    if a_ok and e_ok:
        if isinstance(a, bool) != isinstance(e, bool):
            return False  # True == 1 in Python; a bool is not an int answer
        return a == e
    if e_ok and isinstance(e, str):
        return actual.strip() == e
    return actual.strip() == expected.strip()


class DailySubmitRequest(BaseModel):
    answers: dict[str, int]
    date: str = ""


def _svc(request: Request):
    return request.app.state.practice_service


@router.get("/practice/daily")
def get_daily(request: Request, date: str = Query(default=""),
              user_id: str = Depends(current_user_id)):
    try:
        return _svc(request).daily(user_id, date)
    except DomainError as exc:
        raise _domain_error(exc)


@router.post("/practice/daily/submit")
def submit_daily(body: DailySubmitRequest, request: Request,
                 user_id: str = Depends(current_user_id)):
    try:
        result = _svc(request).submit_daily(user_id, body.date, body.answers)
        request.app.state.streak_service.record_activity(user_id)
        # +2 coins per correct answer
        correct = sum(1 for a in (result.get("results") or [])
                      if isinstance(a, dict) and a.get("correct"))
        if correct:
            request.app.state.coin_service.earn(user_id, "question_solved", correct)
            result["coins_earned"] = correct  # +1 per correct answer
        return result
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/practice/today")
def get_today(request: Request, date: str = Query(default=""),
              user_id: str = Depends(current_user_id)):
    try:
        return _svc(request).today(user_id, date)
    except DomainError as exc:
        raise _domain_error(exc)


# ---- DSA problem bank (TakeUForward-style, 30 original problems) ----

@router.get("/practice/dsa-bank")
def list_dsa_bank(topic: str = Query(default=""),
                  difficulty: str = Query(default=""),
                  user_id: str = Depends(current_user_id)):
    """List DSA problems, optionally filtered by topic/difficulty."""
    problems = get_problems(topic or None, difficulty or None)
    return {
        "count": len(problems),
        "topics": list_topics(),
        "problems": [asdict(p) for p in problems],
    }


@router.get("/practice/dsa-bank/{pid}")
def get_dsa_problem(pid: str, user_id: str = Depends(current_user_id)):
    """Single DSA problem with theory, examples, hints, starter code."""
    problem = get_problem(pid)
    if problem is None:
        raise HTTPException(status_code=404, detail="DSA problem not found")
    return asdict(problem)


@router.get("/practice/dsa-daily")
def get_dsa_daily(date: str = Query(default=""),
                  user_id: str = Depends(current_user_id)):
    """Deterministic daily DSA problem (same for everyone, changes daily)."""
    seed = date or date_cls.today().isoformat()
    problem = get_daily_dsa(seed)
    d = asdict(problem)
    d["topic_tags"] = [problem.topic] if problem.topic else []
    d["date"] = seed
    return d


class DSASubmitRequest(BaseModel):
    date: str = ""
    language: str = "python"
    code: str = ""


@router.post("/dsa/daily/submit")
def submit_dsa_daily(body: DSASubmitRequest, request: Request,
                     user_id: str = Depends(current_user_id)):
    """Run submitted code against the daily problem's example test cases."""
    if not body.code.strip():
        raise HTTPException(status_code=400, detail="code is required")
    seed = body.date or date_cls.today().isoformat()
    try:
        problem = get_daily_dsa(seed)
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    client = request.app.state.code_runner
    request_id = request.headers.get("x-request-id", uuid.uuid4().hex[:12])
    examples = problem.examples or []
    contract = _function_contract(problem, body.language)
    passed = 0
    failed_case = None

    for ex in examples:
        expected = str(ex.get("output", "")).strip()
        try:
            if contract is not None:
                fn_name, params = contract
                code = _driver_code(body.code, fn_name, params,
                                    str(ex.get("input", "")))
                result = client.run(body.language, code, "", {}, request_id)
                actual = _extract_actual(str(result.get("stdout", "")))
                ok = (result.get("verdict") == "OK"
                      and _values_equal(actual, expected))
                if ok:
                    passed += 1
                elif failed_case is None:
                    err = str(result.get("stderr", "")).strip()
                    failed_case = (f"input={ex.get('input', '')!r} "
                                   f"expected={expected!r} got={actual!r}"
                                   + (f" stderr={err!r}" if err else ""))
                continue
            stdin = str(ex.get("input", ""))
            result = client.run(body.language, body.code, stdin, {}, request_id)
            actual = str(result.get("stdout", "")).strip()
            if result.get("verdict") == "OK" and actual == expected:
                passed += 1
            elif failed_case is None:
                failed_case = f"input={stdin!r} expected={expected!r} got={actual!r}"
        except CodeEngineError as exc:
            return JSONResponse(
                status_code=exc.status,
                content={"error": exc.code, "message": str(exc)})

    total = len(examples)
    accepted = total > 0 and passed == total
    return {
        "date": seed,
        "question_id": problem.id,
        "passed": passed,
        "total": total,
        "verdict": "ACCEPTED" if accepted else "WRONG_ANSWER",
        "accepted": accepted,
        "failed_case": failed_case,
    }
