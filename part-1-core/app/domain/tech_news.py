"""Domain: tech news feed — Hacker News + dev.to, cached, never crashes.

Pure functions + thin HTTP fetchers. Every network failure returns []
so a dead API can never break the app or the page.

Cache: in-memory dict with timestamp, 1-hour TTL. The API layer calls
get_tech_news() which serves cache when fresh, refetches when stale.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field

HN_TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{id}.json"
DEVTO_URL = "https://dev.to/api/articles"
USER_AGENT = "SkillForge-NewsFeed/1.0 (+https://skillforge.ai)"

# Score above this = "BIG NEWS" highlight
BIG_NEWS_SCORE = 200
# In-memory cache: {"data": [...], "at": epoch_seconds}
_CACHE: dict = {"data": [], "at": 0.0}
CACHE_TTL_SECONDS = 3600


@dataclass
class NewsItem:
    title: str
    url: str
    source: str  # "hackernews" | "devto"
    score: int = 0
    author: str = ""
    comments: int = 0
    published_at: str = ""
    is_big_news: bool = False

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "url": self.url,
            "source": self.source,
            "score": self.score,
            "author": self.author,
            "comments": self.comments,
            "published_at": self.published_at,
            "is_big_news": self.is_big_news,
        }


def _http_get(url: str, params: dict | None = None, timeout: int = 10):
    """Lazy httpx import; returns response or None on ANY failure."""
    try:
        import httpx

        resp = httpx.get(
            url, params=params, headers={"User-Agent": USER_AGENT}, timeout=timeout
        )
        if resp.status_code == 200:
            return resp
        return None
    except Exception:
        return None


def fetch_hackernews(limit: int = 20) -> list[NewsItem]:
    """Top Hacker News stories. Never raises — returns [] on failure."""
    try:
        resp = _http_get(HN_TOP_URL, timeout=8)
        if resp is None:
            return []
        ids = resp.json()[:limit]
        items: list[NewsItem] = []
        for sid in ids:
            try:
                r = _http_get(HN_ITEM_URL.format(id=sid), timeout=6)
                if r is None:
                    continue
                d = r.json()
                if not d or d.get("type") not in ("story", None):
                    continue
                score = int(d.get("score") or 0)
                items.append(
                    NewsItem(
                        title=str(d.get("title") or "Untitled"),
                        url=str(d.get("url") or f"https://news.ycombinator.com/item?id={sid}"),
                        source="hackernews",
                        score=score,
                        author=str(d.get("by") or ""),
                        comments=int(d.get("descendants") or 0),
                        published_at=str(d.get("time") or ""),
                        is_big_news=score >= BIG_NEWS_SCORE,
                    )
                )
            except Exception:
                continue
        return items
    except Exception:
        return []


def fetch_devto(limit: int = 20) -> list[NewsItem]:
    """Latest dev.to programming articles. Never raises."""
    try:
        resp = _http_get(
            DEVTO_URL,
            params={"per_page": limit, "tag": "programming", "state": "rising"},
            timeout=8,
        )
        if resp is None:
            return []
        items: list[NewsItem] = []
        for a in resp.json():
            try:
                reactions = int(a.get("public_reactions_count") or 0)
                comments = int(a.get("comments_count") or 0)
                score = reactions + comments * 2
                items.append(
                    NewsItem(
                        title=str(a.get("title") or "Untitled"),
                        url=str(a.get("url") or ""),
                        source="devto",
                        score=score,
                        author=str((a.get("user") or {}).get("name") or ""),
                        comments=comments,
                        published_at=str(a.get("published_at") or ""),
                        is_big_news=score >= BIG_NEWS_SCORE,
                    )
                )
            except Exception:
                continue
        return items
    except Exception:
        return []


def get_big_news(items: list[NewsItem]) -> list[NewsItem]:
    """Stories with score >= BIG_NEWS_SCORE, highest first."""
    big = [i for i in items if i.is_big_news]
    return sorted(big, key=lambda i: i.score, reverse=True)


def get_tech_news(force_refresh: bool = False) -> dict:
    """Cached tech news. Returns {"big_news", "latest", "cached_at", "stale"}.

    Serves the 1-hour cache when fresh. On fetch failure keeps serving
    stale cache (marked stale=True) rather than erroring. Never raises.
    """
    now = time.time()
    if not force_refresh and _CACHE["data"] and (now - _CACHE["at"]) < CACHE_TTL_SECONDS:
        items = _CACHE["data"]
        return _build_response(items, cached_at=_CACHE["at"], stale=False)

    fresh: list[NewsItem] = []
    try:
        fresh = fetch_hackernews(20) + fetch_devto(20)
    except Exception:
        fresh = []

    if fresh:
        _CACHE["data"] = fresh
        _CACHE["at"] = now
        return _build_response(fresh, cached_at=now, stale=False)

    # Fetch failed: serve stale cache if we have any, else empty
    if _CACHE["data"]:
        return _build_response(_CACHE["data"], cached_at=_CACHE["at"], stale=True)
    return {"big_news": [], "latest": [], "cached_at": None, "stale": True}


def _build_response(items: list[NewsItem], cached_at: float | None, stale: bool) -> dict:
    big = get_big_news(items)
    big_ids = {id(i) for i in big}
    latest = [i for i in items if id(i) not in big_ids]
    latest = sorted(latest, key=lambda i: i.score, reverse=True)
    return {
        "big_news": [i.to_dict() for i in big],
        "latest": [i.to_dict() for i in latest],
        "cached_at": cached_at,
        "stale": stale,
        "total": len(items),
    }


def clear_cache() -> None:
    """Test helper."""
    _CACHE["data"] = []
    _CACHE["at"] = 0.0
