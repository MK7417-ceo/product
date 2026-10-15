"""Outbound adapter: curated learning tracks (career paths).

A track bundles topics in learning order with an estimated duration.
Tracks feed the "Make a Plan" flow: pick a track → topics resolve to
skills automatically via domain_skills.auto_skills_for_goal().
"""
from __future__ import annotations

TRACKS: dict[str, dict] = {
    "fullstack": {
        "name": "Full Stack Developer",
        "icon": "🧩",
        "description": (
            "Build complete web apps: frontend, backend APIs, "
            "databases, and deployment."
        ),
        "topics": ["webdev", "javascript", "python", "devops"],
        "duration_weeks": 24,
    },
    "frontend": {
        "name": "Frontend Developer",
        "icon": "🎨",
        "description": (
            "Craft fast, beautiful user interfaces for the web."
        ),
        "topics": ["webdev", "javascript"],
        "duration_weeks": 16,
    },
    "backend": {
        "name": "Backend Developer",
        "icon": "⚙️",
        "description": (
            "APIs, databases, and server-side systems that scale."
        ),
        "topics": ["python", "java", "networking", "devops"],
        "duration_weeks": 20,
    },
    "data-scientist": {
        "name": "Data Scientist",
        "icon": "🔬",
        "description": (
            "From raw data to ML models: analysis, statistics, "
            "and machine learning."
        ),
        "topics": ["python", "data-science", "ml-basics", "r-lang"],
        "duration_weeks": 28,
    },
    "data-analyst": {
        "name": "Data Analyst",
        "icon": "📊",
        "description": (
            "Turn data into decisions with SQL, dashboards, "
            "and business metrics."
        ),
        "topics": ["data-analyst", "python", "data-science"],
        "duration_weeks": 16,
    },
    "devops-engineer": {
        "name": "DevOps Engineer",
        "icon": "🚀",
        "description": (
            "Ship reliably: Linux, CI/CD pipelines, containers, "
            "and cloud infrastructure."
        ),
        "topics": ["devops", "networking", "python"],
        "duration_weeks": 20,
    },
}


def get_track(slug: str) -> dict | None:
    """Track dict for a slug, or None if unknown."""
    track = TRACKS.get(slug)
    return dict(track) if track else None


def list_tracks() -> list[str]:
    """All registered track slugs."""
    return list(TRACKS.keys())


def track_skills(slug: str) -> list[str]:
    """Auto-derived skill list for a track (deduped, in learning order)."""
    from app.adapters.outbound.domain_skills import auto_skills_for_goal

    track = TRACKS.get(slug)
    if not track:
        return []
    return auto_skills_for_goal(track["topics"])
