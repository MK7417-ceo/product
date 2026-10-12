"""Inbound adapter (HTTP): code proxy — Core -> Part 2 engine.

Auth-gated. The browser calls THIS; Core forwards to the engine with the
request ID so runs are traceable end to end.
"""
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.api.v1.auth import current_user_id
from app.ports.outbound import CodeEngineError

router = APIRouter(prefix="", tags=["code"])


class CodeRunRequest(BaseModel):
    language: str
    code: str
    stdin: str = ""
    limits: dict = {}


@router.post("/code/run")
def run_code(body: CodeRunRequest, request: Request,
             user_id: str = Depends(current_user_id)):
    request_id = request.headers.get("x-request-id", uuid.uuid4().hex[:12])
    client = request.app.state.code_runner
    try:
        result = client.run(body.language, body.code, body.stdin,
                            body.limits, request_id)
    except CodeEngineError as exc:
        return JSONResponse(status_code=exc.status,
                            content={"error": exc.code, "message": str(exc)})
    return result


@router.get("/code/languages")
def code_languages(request: Request, user_id: str = Depends(current_user_id)):
    client = request.app.state.code_runner
    try:
        return {"languages": client.languages()}
    except CodeEngineError as exc:
        return JSONResponse(status_code=exc.status,
                            content={"error": exc.code, "message": str(exc)})
