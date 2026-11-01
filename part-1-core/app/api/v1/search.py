"""Inbound adapter (HTTP): global search router — Notes-style unified search."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request

from app.api.v1.auth import _domain_error, current_user_id
from app.domain.user import DomainError

router = APIRouter(prefix="", tags=["search"])


def _svc(request: Request):
    return request.app.state.search_service


@router.get("/search")
def global_search(
    request: Request,
    q: str = Query(min_length=1, max_length=100),
    types: str | None = Query(default=None, max_length=100,
                              description="comma-separated subset of: roadmap,task,evidence,assessment,certificate"),
    limit: int = Query(default=20, ge=1, le=50),
    user_id: str = Depends(current_user_id),
):
    try:
        results = _svc(request).search(user_id, q, types, limit)
    except DomainError as exc:
        raise _domain_error(exc)
    return {
        "query": q.strip(),
        "count": len(results),
        "results": [
            {
                "type": r.type, "id": r.id, "title": r.title,
                "snippet": r.snippet, "score": r.score,
                "created_at": r.created_at,
            }
            for r in results
        ],
    }
