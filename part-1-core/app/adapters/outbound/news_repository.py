"""Outbound adapter: tech news persistence with 1-year retention.

Policy:
- Fetched news is stored in the `tech_news` table.
- Rows older than 1 year are auto-deleted on every write (cleanup).
- Reads return latest-first (fetched_at DESC).
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.adapters.outbound.models import TechNewsModel

RETENTION_DAYS = 365


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def save_news(session: Session, items: list[dict]) -> int:
    """Upsert fetched news (dedupe by URL). Returns # newly inserted."""
    inserted = 0
    for item in items:
        url = (item.get("url") or "").strip()
        if not url:
            continue
        exists = session.query(TechNewsModel).filter_by(url=url).first()
        if exists:
            continue
        session.add(TechNewsModel(
            id=str(uuid.uuid4()),
            title=(item.get("title") or "")[:500],
            url=url[:1000],
            source=(item.get("source") or "")[:60],
            score=int(item.get("score") or 0),
            published_at=str(item.get("published_at") or "")[:40],
            fetched_at=_utcnow(),
        ))
        inserted += 1
    session.commit()
    cleanup_old_news(session)
    return inserted


def cleanup_old_news(session: Session) -> int:
    """DELETE FROM tech_news WHERE fetched_at < NOW() - 1 year. Returns # deleted."""
    cutoff = _utcnow() - timedelta(days=RETENTION_DAYS)
    deleted = (
        session.query(TechNewsModel)
        .filter(TechNewsModel.fetched_at < cutoff)
        .delete(synchronize_session=False)
    )
    session.commit()
    return deleted


def get_latest_news(session: Session, limit: int = 40) -> list[dict]:
    """Latest news first (fetched_at DESC)."""
    rows = (
        session.query(TechNewsModel)
        .order_by(TechNewsModel.fetched_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "title": r.title,
            "url": r.url,
            "source": r.source,
            "score": r.score,
            "published_at": r.published_at,
            "fetched_at": r.fetched_at.isoformat() if r.fetched_at else None,
        }
        for r in rows
    ]


def count_news(session: Session) -> int:
    return session.query(TechNewsModel).count()
