"""Weekly tests API — schedule, start, submit, grade."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from app.api.v1.auth import _domain_error, current_user_id
from app.domain.user import DomainError

router = APIRouter(tags=["weekly-tests"])


def _svc(request: Request):
    return request.app.state.weekly_test_service


class SubmitRequest(BaseModel):
    answers: dict  # {question_id: answer_index}


@router.get("/weekly-tests/mine")
def my_tests(request: Request, user_id: str = Depends(current_user_id)):
    return _svc(request).my_tests(user_id)


@router.post("/weekly-tests/start/{test_id}")
def start_test(test_id: str, request: Request,
               user_id: str = Depends(current_user_id)):
    try:
        return _svc(request).start_test(user_id, test_id)
    except DomainError as exc:
        raise _domain_error(exc)


@router.post("/weekly-tests/{test_id}/submit")
def submit_test(test_id: str, body: SubmitRequest, request: Request,
                user_id: str = Depends(current_user_id)):
    try:
        return _svc(request).submit_test(user_id, test_id, body.answers)
    except DomainError as exc:
        raise _domain_error(exc)
