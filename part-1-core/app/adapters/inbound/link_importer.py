"""Inbound adapter: link importer — the "paste a link" foundation for the CMS.

Fetches a public URL and extracts structured preview data (title, description,
headings, text snippets) for an admin to review/edit before saving as theory.
No LLM involved yet — that slot comes later.

Rules:
- Only http/https URLs.
- Basic SSRF guard: blocks localhost + private/link-local IP literals and
  hostnames that resolve to private IPs.
- Graceful failures: timeouts, blocks (403/429), non-HTML content and parse
  errors all return an honest {"ok": False, "error": ...} dict — never raises.
"""
from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse

import httpx

USER_AGENT = "SkillForgeBot/1.0 (+https://skillforge.ai; admin content import)"
TIMEOUT_S = 12.0
MAX_BYTES = 2_000_000


def _is_private_host(host: str) -> bool:
    host = (host or "").lower().strip().rstrip(".")
    if host in ("localhost",):
        return True
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
    except ValueError:
        pass  # not an IP literal — resolve below
    try:
        infos = socket.getaddrinfo(host, None, family=socket.AF_UNSPEC,
                                   type=socket.SOCK_STREAM)
    except (socket.gaierror, UnicodeError):
        return True  # unresolvable → treat as unsafe
    for _fam, _typ, _proto, _canon, sockaddr in infos:
        try:
            ip = ipaddress.ip_address(sockaddr[0])
        except ValueError:
            continue
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
            return True
    return False


def _fail(error: str) -> dict:
    return {"ok": False, "error": error, "title": "", "description": "",
            "headings": [], "snippets": [], "url": ""}


def import_from_url(url: str) -> dict:
    """Fetch url and extract a structured preview. Never raises."""
    url = (url or "").strip()
    try:
        parsed = urlparse(url)
    except Exception:
        return _fail("invalid url")
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        return _fail("only http/https urls are allowed")
    if _is_private_host(parsed.hostname):
        return _fail("private/internal hosts are not allowed")

    try:
        resp = httpx.get(url, headers={"User-Agent": USER_AGENT},
                         timeout=TIMEOUT_S, follow_redirects=True)
    except httpx.TimeoutException:
        return _fail("request timed out")
    except httpx.ConnectError:
        return _fail("could not connect to host")
    except httpx.HTTPError as exc:
        return _fail(f"request failed: {type(exc).__name__}")
    except Exception:
        return _fail("unexpected fetch error")

    if resp.status_code == 403:
        return _fail("site blocked automated access (403)")
    if resp.status_code == 429:
        return _fail("site rate-limited the request (429)")
    if resp.status_code >= 400:
        return _fail(f"site returned http {resp.status_code}")

    content_type = resp.headers.get("content-type", "")
    if "html" not in content_type.lower():
        return _fail(f"not an html page (content-type: {content_type[:60] or 'unknown'})")

    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return _fail("html parser not installed (beautifulsoup4)")

    try:
        raw = resp.content[:MAX_BYTES]
        soup = BeautifulSoup(raw, "html.parser")
        for tag in soup(["script", "style", "noscript", "nav", "footer"]):
            tag.decompose()

        title = (soup.title.string or "").strip() if soup.title else ""
        desc_tag = soup.find("meta", attrs={"name": "description"}) or \
            soup.find("meta", attrs={"property": "og:description"})
        description = (desc_tag.get("content", "") or "").strip() if desc_tag else ""

        headings: list[str] = []
        for h in soup.find_all(["h1", "h2"]):
            text = " ".join(h.get_text(" ", strip=True).split())
            if text and len(headings) < 12:
                headings.append(text[:200])

        snippets: list[str] = []
        for p in soup.find_all("p"):
            text = " ".join(p.get_text(" ", strip=True).split())
            if len(text) >= 40 and len(snippets) < 8:
                snippets.append(text[:500])

        if not title and not headings and not snippets:
            return _fail("no readable content found on page")
        return {"ok": True, "error": "", "url": str(resp.url),
                "title": title[:200], "description": description[:500],
                "headings": headings, "snippets": snippets}
    except Exception:
        return _fail("could not parse page content")
