"""Domain: plagiarism similarity. PURE, deterministic, no LLM.

Pipeline (mirrors docs/part-2-code-engine/SPECS.md S5):
  1. Normalize: strip comments, canonicalize identifiers (v1, v2, ... in
     order of first appearance), fold string literals -> STR, numbers -> NUM,
     drop whitespace. Supplied boilerplate/starter code is excluded first.
  2. Fingerprint: token 5-gram hashes (all languages) + AST-shape hash
     (Python via `ast`).
  3. Score: Jaccard over 5-gram sets, blended 70/30 with AST-shape
     similarity for Python; 100% n-gram for other languages.
  4. Decide: score >= 0.85 -> flagged=true + human-readable reasons.

FLAG-ONLY: this never accuses anyone. A flag means "a human should look".
"""
from __future__ import annotations

import ast
import hashlib
import keyword
import re
from dataclasses import dataclass

FLAG_THRESHOLD = 0.85
NGRAM = 5

# language families for comment syntax
_HASH_COMMENT = {"python"}
_C_COMMENT = {"c", "cpp", "java"}

_C_KEYWORDS = frozenset("""
auto break case char const continue default do double else enum extern
float for goto if inline int long register restrict return short signed
sizeof static struct switch typedef union unsigned void volatile while
_Bool _Complex _Imaginary true false nullptr
class public private protected template typename namespace using virtual
override final new delete try catch throw operator this friend constexpr
decltype noexcept static_assert thread_local alignas alignof
""".split())
_PY_KEYWORDS = frozenset(keyword.kwlist)

_TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*|\d+(?:\.\d+)?|\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*'|.")
_STR_RE = re.compile(r"\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*'")
_NUM_RE = re.compile(r"^\d+(\.\d+)?$")
_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _strip_comments(code: str, language: str) -> str:
    if language in _HASH_COMMENT:
        out = []
        for line in code.splitlines():
            # crude but deterministic: cut at first # outside a string
            cut = len(line)
            in_s = None
            for i, ch in enumerate(line):
                if in_s:
                    if ch == in_s:
                        in_s = None
                elif ch in "\"'":
                    in_s = ch
                elif ch == "#":
                    cut = i
                    break
            out.append(line[:cut])
        return "\n".join(out)
    # C-family: remove /* */ then //
    code = re.sub(r"/\*.*?\*/", " ", code, flags=re.DOTALL)
    out = []
    for line in code.splitlines():
        cut = len(line)
        in_s = None
        i = 0
        while i < len(line) - 1:
            ch = line[i]
            if in_s:
                if ch == "\\":
                    i += 2
                    continue
                if ch == in_s:
                    in_s = None
            elif ch in "\"'":
                in_s = ch
            elif ch == "/" and line[i + 1] == "/":
                cut = i
                break
            i += 1
        out.append(line[:cut])
    return "\n".join(out)


def _keywords(language: str) -> frozenset:
    return _PY_KEYWORDS if language == "python" else _C_KEYWORDS


def normalize(code: str, language: str, boilerplate: str = "") -> list[str]:
    """Code -> canonical token list."""
    if boilerplate:
        code = code.replace(boilerplate, " ")
    code = _strip_comments(code, language)
    code = _STR_RE.sub(" STR ", code)
    kws = _keywords(language)
    mapping: dict[str, str] = {}
    counter = 0
    tokens: list[str] = []
    for m in _TOKEN_RE.finditer(code):
        tok = m.group(0)
        if not tok.strip():
            continue
        if _NUM_RE.match(tok):
            tokens.append("NUM")
        elif _IDENT_RE.match(tok):
            if tok in kws:
                tokens.append(tok)
            else:
                if tok not in mapping:
                    counter += 1
                    mapping[tok] = f"v{counter}"
                tokens.append(mapping[tok])
        elif tok.strip() in ";,(){}[]":
            tokens.append(tok.strip())
        else:
            tokens.append(tok.strip())
    return [t for t in tokens if t]


def _ngrams(tokens: list[str], n: int = NGRAM) -> set[str]:
    if len(tokens) < n:
        return {" ".join(tokens)} if tokens else set()
    return {" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1)}


def _ast_shape(code: str) -> str:
    """Python AST with all names/constants blanked -> structural shape."""
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            node.id = "_"
        elif isinstance(node, ast.arg):
            node.arg = "_"
        elif isinstance(node, ast.Constant):
            node.value = 0
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            node.name = "_"
        elif isinstance(node, ast.Attribute):
            node.attr = "_"
    return ast.dump(tree)


def _ast_similarity(a: str, b: str) -> float:
    """Deterministic shape similarity via difflib on normalized dumps."""
    import difflib
    sa, sb = _ast_shape(a), _ast_shape(b)
    if sa == sb:
        return 1.0
    return difflib.SequenceMatcher(None, sa, sb).ratio()


def fingerprint(code: str, language: str, boilerplate: str = "") -> dict:
    tokens = normalize(code, language, boilerplate)
    grams = _ngrams(tokens)
    fp = {
        "ngram_count": len(grams),
        "ngram_hash": hashlib.sha256(
            "|".join(sorted(grams)).encode()).hexdigest()[:16],
    }
    if language == "python":
        try:
            fp["ast_shape_hash"] = hashlib.sha256(
                _ast_shape(code).encode()).hexdigest()[:16]
        except SyntaxError:
            fp["ast_shape_hash"] = None
    return fp


def similarity(code_a: str, code_b: str, language: str,
               boilerplate: str = "") -> tuple[float, dict]:
    """(score 0..1, debug info)."""
    ta = normalize(code_a, language, boilerplate)
    tb = normalize(code_b, language, boilerplate)
    ga, gb = _ngrams(ta), _ngrams(tb)
    if not ga and not gb:
        return 1.0, {"jaccard": 1.0, "ast": 1.0}
    union = ga | gb
    jaccard = len(ga & gb) / len(union) if union else 0.0
    info = {"jaccard": round(jaccard, 4), "ast": None}
    if language == "python":
        try:
            ast_sim = _ast_similarity(code_a, code_b)
        except SyntaxError:
            ast_sim = 0.0
        info["ast"] = round(ast_sim, 4)
        score = 0.7 * jaccard + 0.3 * ast_sim
    else:
        score = jaccard
    return round(score, 4), info


@dataclass(frozen=True)
class PlagiarismVerdict:
    candidate_id: str
    score: float
    flagged: bool
    reasons: tuple[str, ...]
    fingerprint_a: dict
    fingerprint_b: dict


def check(code: str, candidates: list[dict], language: str,
          boilerplate: str = "") -> list[PlagiarismVerdict]:
    """Compare code against each candidate. Deterministic."""
    if language not in ("python", "c", "cpp", "java"):
        raise ValueError(f"unsupported language: {language}")
    fp_a = fingerprint(code, language, boilerplate)
    out = []
    for cand in candidates:
        score, info = similarity(code, cand["code"], language, boilerplate)
        reasons: list[str] = []
        flagged = score >= FLAG_THRESHOLD
        if flagged:
            reasons.append(f"similarity {score:.2f} >= {FLAG_THRESHOLD}")
            if info["jaccard"] is not None and info["jaccard"] >= 0.9:
                reasons.append("near-identical token structure")
            if info["ast"] is not None and info["ast"] >= 0.9:
                reasons.append("near-identical AST shape")
            reasons.append("flag for human review — not a verdict of guilt")
        out.append(PlagiarismVerdict(
            candidate_id=cand["id"], score=score, flagged=flagged,
            reasons=tuple(reasons),
            fingerprint_a=fp_a,
            fingerprint_b=fingerprint(cand["code"], language, boilerplate)))
    return out
