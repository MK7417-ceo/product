"""1v1 battles API — queue, match, challenge, play, results."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from app.api.v1.auth import _domain_error, current_user_id
from app.domain.user import DomainError

router = APIRouter(tags=["battles"])


def _svc(request: Request):
    return request.app.state.battle_service


class QueueRequest(BaseModel):
    topic: str
    level: str
    window_seconds: int = Field(default=180, ge=60, le=600)


class ChallengeRequest(BaseModel):
    topic: str
    level: str
    opponent_email: str
    window_seconds: int = Field(default=180, ge=60, le=600)


class JoinRequest(BaseModel):
    invite_code: str
    level: str


class SubmitRequest(BaseModel):
    answers: dict  # {question_id: answer_index}
    answer_times: dict | None = None  # {question_id: seconds since start}


@router.get("/battles/fair-play")
def fair_play(request: Request):
    return _svc(request).fair_play()


@router.get("/battles/mine")
def my_battles(request: Request, user_id: str = Depends(current_user_id)):
    return _svc(request).mine(user_id)


@router.post("/battles/queue", status_code=201)
def queue_battle(body: QueueRequest, request: Request,
                 user_id: str = Depends(current_user_id)):
    try:
        return _svc(request).queue(user_id, body.topic, body.level,
                                   body.window_seconds)
    except DomainError as exc:
        raise _domain_error(exc)


@router.post("/battles/challenge", status_code=201)
def challenge_friend(body: ChallengeRequest, request: Request,
                     user_id: str = Depends(current_user_id)):
    try:
        return _svc(request).challenge(user_id, body.topic, body.level,
                                       body.opponent_email,
                                       body.window_seconds)
    except DomainError as exc:
        raise _domain_error(exc)


@router.post("/battles/join")
def join_challenge(body: JoinRequest, request: Request,
                   user_id: str = Depends(current_user_id)):
    try:
        return _svc(request).join_challenge(user_id, body.invite_code,
                                            body.level)
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/battles/{battle_id}")
def get_battle(battle_id: str, request: Request,
               user_id: str = Depends(current_user_id)):
    try:
        return _svc(request).get_battle(user_id, battle_id)
    except DomainError as exc:
        raise _domain_error(exc)


@router.post("/battles/{battle_id}/submit")
def submit_battle(battle_id: str, body: SubmitRequest, request: Request,
                  user_id: str = Depends(current_user_id)):
    try:
        return _svc(request).submit(user_id, battle_id, body.answers,
                                    body.answer_times)
    except DomainError as exc:
        raise _domain_error(exc)


@router.post("/battles/{battle_id}/rematch", status_code=201)
def rematch_battle(battle_id: str, request: Request,
                   user_id: str = Depends(current_user_id)):
    try:
        return _svc(request).rematch(user_id, battle_id)
    except DomainError as exc:
        raise _domain_error(exc)
