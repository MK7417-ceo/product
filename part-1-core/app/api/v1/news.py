"""Inbound adapter (HTTP): tech news router.

Public (no auth): GET /news/tech — cached Hacker News + dev.to feed.
Retention: 1 year in DB, older rows auto-deleted.
Serves latest-first. Never errors: worst case returns empty lists.
"""
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.adapters.outbound import news_repository
from app.api.v1.auth import require_admin
from app.core.database import get_db
from app.domain import tech_news

router = APIRouter(prefix="", tags=["news"])


@router.get("/news/tech")
def get_tech_news(
    refresh: bool = Query(default=False),
    db: Session = Depends(get_db),
):
    """Tech news: big_news (score >= 200) + latest, latest-first, 1-year retention."""
    try:
        if refresh or news_repository.count_news(db) == 0:
            # Fresh fetch → persist to DB (dedupes by URL, cleans >1yr old)
            fresh = tech_news.get_tech_news(force_refresh=True)
            items = fresh.get("big_news", []) + fresh.get("latest", [])
            news_repository.save_news(db, items)

        stored = news_repository.get_latest_news(db, limit=40)
        big = [n for n in stored if (n.get("score") or 0) >= 200][:10]
        big_urls = {n["url"] for n in big}
        latest = [n for n in stored if n["url"] not in big_urls][:30]

        # "Updated X min ago" — from most recent fetched_at
        updated_min_ago = None
        if stored and stored[0].get("fetched_at"):
            try:
                fa = stored[0]["fetched_at"]
                dt = datetime.fromisoformat(fa)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                updated_min_ago = max(
                    0, int((datetime.now(timezone.utc) - dt).total_seconds() / 60)
                )
            except Exception:
                pass

        return {
            "big_news": big,
            "latest": latest,
            "updated_min_ago": updated_min_ago,
            "retention": "1 year",
            "stale": False,
        }
    except Exception:
        return {
            "big_news": [],
            "latest": [],
            "updated_min_ago": None,
            "retention": "1 year",
            "stale": True,
        }


@router.post("/news/cleanup")
def cleanup_news(db: Session = Depends(get_db),
                 _admin: str = Depends(require_admin)):
    """Maintenance: delete news older than 1 year. Returns count deleted."""
    deleted = news_repository.cleanup_old_news(db)
    return {"deleted": deleted, "retention": "1 year"}
