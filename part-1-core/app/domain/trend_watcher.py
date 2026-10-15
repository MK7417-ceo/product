"""Domain: trend watcher — detect emerging tech from public signals.

Pure functions + a thin HTTP fetcher. The fetcher NEVER raises:
every network failure returns [] so a weekly cron can never crash the app.

Weekly cron (documented, not scheduled here — admin sets it up):
    # Every Monday 06:00 — refresh trend candidates for admin review
    0 6 * * 1 curl -s -H "Authorization: Bearer $ADMIN_TOKEN" \\
        https://api.skillforge.ai/api/v1/admin/trends > /tmp/trends.json
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, timedelta

GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"
USER_AGENT = "SkillForge-TrendWatcher/1.0 (+https://skillforge.ai)"

# Generic words that are never "new tech"
STOPWORDS = {
    "awesome", "tutorial", "guide", "course", "learn", "example", "examples",
    "demo", "template", "boilerplate", "starter", "project", "projects",
    "list", "collection", "notes", "book", "roadmap", "interview",
    "awesome-list", "free", "open", "source",
}


@dataclass
class TrendingRepo:
    name: str
    full_name: str
    description: str
    language: str | None
    stars: int
    topics: list[str] = field(default_factory=list)


@dataclass
class TechCandidate:
    """A technology that looks new vs our known domain slugs."""
    id: str            # slug
    name: str
    category: str      # language | tech-domain
    reason: str        # why we think it's new/trending
    stars: int         # combined stars of repos mentioning it
    repo: str          # example repo full_name
    modules: list[dict] = field(default_factory=list)


def _github_headers() -> dict:
    return {"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"}


def fetch_trending_repos(client=None, days: int = 30, per_page: int = 30) -> list[TrendingRepo]:
    """Fetch recently-created, highly-starred repos from GitHub search.

    `client` is injectable for tests: any object with
    `.get(url, params=..., headers=..., timeout=...)` returning an object
    with `.status_code` and `.json()`. Defaults to httpx (lazy import).
    Never raises — returns [] on any failure.
    """
    try:
        since = (date.today() - timedelta(days=days)).isoformat()
        params = {
            "q": f"created:>{since} stars:>200",
            "sort": "stars",
            "order": "desc",
            "per_page": per_page,
        }
        if client is None:
            import httpx  # lazy: only needed when actually fetching
            resp = httpx.get(GITHUB_SEARCH_URL, params=params,
                             headers=_github_headers(), timeout=15)
        else:
            resp = client.get(GITHUB_SEARCH_URL, params=params,
                              headers=_github_headers(), timeout=15)
        if resp.status_code != 200:
            return []
        items = (resp.json() or {}).get("items", [])
        repos = []
        for it in items:
            repos.append(TrendingRepo(
                name=it.get("name", ""),
                full_name=it.get("full_name", ""),
                description=it.get("description") or "",
                language=it.get("language"),
                stars=int(it.get("stargazers_count") or 0),
                topics=list(it.get("topics") or []),
            ))
        return repos
    except Exception:
        return []


def normalize_tech(name: str) -> str:
    """Canonical key for comparing tech names: lowercase alnum only."""
    return re.sub(r"[^a-z0-9]", "", (name or "").lower())


def _is_language_like(name: str) -> bool:
    langs = {"rust", "go", "zig", "bun", "deno", "typescript", "kotlin",
             "swift", "julia", "elixir", "haskell", "scala", "dart", "mojo"}
    return normalize_tech(name) in langs


def detect_new_tech(known_slugs: list[str] | set[str],
                    repos: list[TrendingRepo] | None = None,
                    client=None) -> list[TechCandidate]:
    """Compare trending repos against known domain slugs; return new-tech candidates.

    Signals used per repo: `language`, `topics`, and capitalized words in the
    repo name/description. Anything already in `known_slugs` (normalized) is
    skipped. Never raises.
    """
    try:
        known = {normalize_tech(s) for s in (known_slugs or [])}
        if repos is None:
            repos = fetch_trending_repos(client=client)
        buckets: dict[str, dict] = {}
        for repo in repos:
            signals: list[tuple[str, str]] = []
            if repo.language:
                signals.append((repo.language, f"language of trending repo {repo.full_name}"))
            for t in repo.topics:
                signals.append((t, f"topic of trending repo {repo.full_name}"))
            # capitalized tokens in name/description often name frameworks
            for token in re.findall(r"\b[A-Z][A-Za-z0-9+]{2,}\b",
                                    f"{repo.name} {repo.description}"):
                signals.append((token, f"mentioned in trending repo {repo.full_name}"))
            for raw, why in signals:
                key = normalize_tech(raw)
                if not key or key in known or key in STOPWORDS or len(key) < 3:
                    continue
                b = buckets.setdefault(key, {"name": raw.strip(), "stars": 0,
                                             "repo": repo.full_name, "why": why})
                b["stars"] += repo.stars
                if repo.stars > b["stars"] - repo.stars and not b["repo"]:
                    b["repo"] = repo.full_name
        candidates = []
        for key, b in buckets.items():
            name = b["name"]
            candidates.append(TechCandidate(
                id=key,
                name=name,
                category="language" if _is_language_like(name) else "tech-domain",
                reason=f"Trending on GitHub ({b['stars']:,} stars): {b['why']}",
                stars=b["stars"],
                repo=b["repo"],
                modules=suggest_modules(name),
            ))
        candidates.sort(key=lambda c: c.stars, reverse=True)
        return candidates
    except Exception:
        return []


def suggest_modules(tech_name: str) -> list[dict]:
    """Starter module outline for a brand-new domain."""
    n = tech_name.strip()
    return [
        {"slug": "fundamentals", "name": f"{n} Fundamentals",
         "description": f"What {n} is, why it exists, ecosystem overview",
         "estimated_days": 7},
        {"slug": "core-concepts", "name": "Core Concepts",
         "description": f"Key ideas and mental models behind {n}", "estimated_days": 10},
        {"slug": "hands-on", "name": "Hands-On",
         "description": f"Build your first real thing with {n}", "estimated_days": 10},
        {"slug": "advanced", "name": "Advanced & Production",
         "description": f"Best practices, performance, deploying {n}", "estimated_days": 7},
    ]


def suggest_domain(candidate: TechCandidate) -> dict:
    """Turn a candidate into a domain payload ready for admin approval."""
    return {
        "slug": candidate.id,
        "name": candidate.name,
        "description": f"{candidate.name} — {candidate.reason}",
        "icon": "🆕",
        "category": candidate.category,
        "modules": candidate.modules or suggest_modules(candidate.name),
    }


def run_weekly_check(known_slugs: list[str] | set[str], client=None) -> list[TechCandidate]:
    """One call the weekly cron (or admin panel) uses. Never raises."""
    try:
        return detect_new_tech(known_slugs, client=client)
    except Exception:
        return []
