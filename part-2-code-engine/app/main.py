"""HTTP API for the Code Execution Engine (v1)."""
from __future__ import annotations

import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.adapters.runners import CodeRunnerServiceImpl
from app.domain.execution import ExecutionError, ExecutionRequest, Limits
from app.domain.plagiarism import check as plagiarism_check

REQUEST_ID_HEADER = "X-Request-ID"


class RunRequest(BaseModel):
    language: str
    code: str
    stdin: str = ""
    limits: dict = {}


class RunResponse(BaseModel):
    run_id: str
    verdict: str
    stdout: str
    stderr: str
    truncated: bool
    exit_code: int | None
    cpu_ms: int | None
    peak_ram_mb: float | None
    timed_out: bool


class PlagiarismRequest(BaseModel):
    language: str
    code: str
    candidates: list[dict]  # [{id, code}]
    boilerplate: str = ""


def create_app() -> FastAPI:
    app = FastAPI(title="SkillForge Code Engine", version="0.1.0")
    svc = CodeRunnerServiceImpl()

    @app.middleware("http")
    async def request_id(request: Request, call_next):
        rid = request.headers.get(REQUEST_ID_HEADER, uuid.uuid4().hex[:12])
        response = await call_next(request)
        response.headers[REQUEST_ID_HEADER] = rid
        return response

    @app.get("/v1/health")
    def health():
        return {"ok": True, "service": "code-engine"}

    @app.get("/v1/languages")
    def languages():
        return {"languages": svc.languages()}

    @app.post("/v1/run", response_model=RunResponse)
    def run(body: RunRequest):
        t0 = time.monotonic()
        try:
            lim = Limits(**(body.limits or {}))
            req = ExecutionRequest(language=body.language, code=body.code,
                                   stdin=body.stdin, limits=lim)
        except ExecutionError as exc:
            return JSONResponse(status_code=400,
                                content={"error": exc.code, "message": str(exc)})
        except TypeError as exc:
            return JSONResponse(status_code=400,
                                content={"error": "bad_limits", "message": str(exc)})
        try:
            res = svc.run(req)
        except ExecutionError as exc:
            return JSONResponse(status_code=400,
                                content={"error": exc.code, "message": str(exc)})
        payload = RunResponse(
            run_id=res.run_id, verdict=res.verdict, stdout=res.stdout,
            stderr=res.stderr, truncated=res.truncated, exit_code=res.exit_code,
            cpu_ms=res.cpu_ms, peak_ram_mb=res.peak_ram_mb, timed_out=res.timed_out,
        ).model_dump()
        payload["server_ms"] = int((time.monotonic() - t0) * 1000)
        return payload

    @app.post("/v1/plagiarism/check")
    def plagiarism(body: PlagiarismRequest):
        if body.language not in ("python", "c", "cpp", "java"):
            return JSONResponse(status_code=400, content={
                "error": "unsupported_language",
                "message": "language must be python|c|cpp|java"})
        if not body.code.strip() or not body.candidates:
            return JSONResponse(status_code=400, content={
                "error": "bad_request",
                "message": "code and non-empty candidates are required"})
        try:
            verdicts = plagiarism_check(body.code,
                                        [{"id": c.get("id", "?"), "code": c.get("code", "")}
                                         for c in body.candidates],
                                        body.language, body.boilerplate)
        except (ValueError, SyntaxError) as exc:
            return JSONResponse(status_code=400, content={
                "error": "bad_request", "message": str(exc)})
        return {"results": [
            {"candidate_id": v.candidate_id, "score": v.score,
             "flagged": v.flagged, "reasons": list(v.reasons),
             "fingerprint_a": v.fingerprint_a, "fingerprint_b": v.fingerprint_b}
            for v in verdicts]}

    return app


app = create_app()
