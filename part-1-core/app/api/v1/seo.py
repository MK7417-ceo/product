"""Inbound adapter (HTTP): public SEO endpoints.

No auth: sitemap.xml and robots.txt must be readable by search-engine
crawlers without any login. The sitemap lists ONLY real public pages:

- static public routes (/, /topics, /en/topics, /directory, /login,
  /register)
- one /topics/<slug> AND one /en/topics/<slug> URL per active topic
  that actually has theory content (topics with zero theory blocks are
  excluded — never promise content that does not exist).

Language pairing: each topics URL carries hreflang alternates for both
versions (hi = /topics/..., en = /en/topics/...), so crawlers see the
two language versions as one paired page, not duplicates. Pages with no
language counterpart (/, /directory, /login, /register) carry none.

Base URL: settings.PUBLIC_BASE_URL when the deployment sets it (needed
when the frontend and the API live on different origins — the sitemap
must point at the origin where the pages live). Otherwise it falls back
to the request's own base URL, which is correct for same-origin proxy
deployments. No domain is hardcoded or invented here.
"""
from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse, Response
from xml.sax.saxutils import escape

from app.core.config import settings

# The router is registered WITHOUT the /api/v1 prefix (see main.py):
# crawlers expect /sitemap.xml and /robots.txt at the site root.

router = APIRouter(tags=["seo"])

_STATIC_PAGES = [
    ("/", "weekly", "1.0"),
    ("/topics", "weekly", "0.9"),
    ("/en/topics", "weekly", "0.9"),
    ("/directory", "weekly", "0.9"),
    ("/register", "monthly", "0.8"),
    ("/login", "monthly", "0.5"),
]

# Paths that exist in both languages -> hreflang pair (hi, en).
_PAIRED_PATHS = {"/topics", "/en/topics"}


def _base_url(request: Request) -> str:
    configured = (settings.PUBLIC_BASE_URL or "").strip()
    if configured:
        return configured.rstrip("/")
    return str(request.base_url).rstrip("/")


def _public_topics(request: Request) -> list[dict]:
    """Active topics with real theory content, via the content service."""
    try:
        topics = request.app.state.content_service.list_topics(True)
    except Exception:
        return []
    return [t for t in topics if (t.get("theory_count") or 0) > 0]


@router.get("/robots.txt", response_class=PlainTextResponse)
def robots(request: Request):
    base = _base_url(request)
    lines = [
        "User-agent: *",
        "Allow: /",
        "Allow: /topics",
        "Allow: /en/topics",
        "Allow: /directory",
        "Disallow: /api/",
        "Disallow: /login",
        "Disallow: /register",
        "",
        f"Sitemap: {base}/sitemap.xml",
        "",
    ]
    return "\n".join(lines)


def _url_entry(base: str, path: str, changefreq: str, priority: str,
                alternates: list[tuple[str, str]] | None = None) -> list[str]:
    lines = ["  <url>", f"    <loc>{escape(base + path)}</loc>"]
    for hreflang, href in (alternates or []):
        lines.append(
            f'    <xhtml:link rel="alternate" hreflang="{hreflang}" '
            f'href="{escape(base + href)}" />'
        )
    lines.append(f"    <changefreq>{changefreq}</changefreq>")
    lines.append(f"    <priority>{priority}</priority>")
    lines.append("  </url>")
    return lines


def _topic_pair(slug: str) -> list[tuple[str, str]]:
    """hreflang alternates for one topic in both languages."""
    return [("hi", f"/topics/{slug}"), ("en", f"/en/topics/{slug}")]


@router.get("/sitemap.xml")
def sitemap(request: Request):
    base = _base_url(request)
    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
             'xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for path, changefreq, priority in _STATIC_PAGES:
        alternates = (
            [("hi", "/topics"), ("en", "/en/topics")]
            if path in _PAIRED_PATHS else None
        )
        parts.extend(_url_entry(base, path, changefreq, priority, alternates))
    for topic in _public_topics(request):
        slug = topic.get("slug")
        if slug:
            pair = _topic_pair(slug)
            parts.extend(_url_entry(base, f"/topics/{slug}", "weekly", "0.8", pair))
            parts.extend(_url_entry(base, f"/en/topics/{slug}", "weekly", "0.8", pair))
    parts.append("</urlset>")
    return Response(content="\n".join(parts) + "\n",
                    media_type="application/xml")
