"""Inbound adapter (HTTP): tech news router.

Public (no auth): GET /news/tech — cached Hacker News + dev.to feed.
Never errors: worst case returns empty lists with stale=True.
"""
from __future__ import annotations

from fastapi import APIRouter, Query

from app.domain import tech_news

router = APIRouter(prefix="", tags=["news"])


@router.get("/news/tech")
def get_tech_news(refresh: bool = Query(default=False)):
    """Tech news feed: big_news (score >= 200) + latest, cached 1 hour."""
    try:
        return tech_news.get_tech_news(force_refresh=refresh)
    except Exception:
        return {"big_news": [], "latest": [], "cached_at": None, "stale": True}
