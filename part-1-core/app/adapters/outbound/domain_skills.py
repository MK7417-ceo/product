"""Outbound adapter: topic → skill tag registry + training-mode flags.

Central registry mapping every learning topic to its canonical skill tags.
Skill tags MUST match the `skill` field used in question_bank.py so gap
reports, roadmaps, and auto skill assignment stay consistent.

- coding=True  → code-lab style training (write + run code)
- coding=False → visual/theory style training (diagrams, concepts)

`auto_skills_for_goal()` powers the "auto add skills" feature: when a user
picks goal topics, their required skills are derived automatically — the
user never has to type skill names by hand.
"""
from __future__ import annotations

DOMAIN_SKILLS: dict[str, dict] = {
    "python": {
        "name": "Python",
        "icon": "🐍",
        "description": "General-purpose programming: basics to advanced.",
        "coding": True,
        "skills": [
            "python-basics",
            "data-structures",
            "functions",
            "iterators",
            "oop",
            "stdlib",
            "advanced-python",
        ],
    },
    "javascript": {
        "name": "JavaScript",
        "icon": "🟨",
        "description": "The language of the web: browser and Node.js.",
        "coding": True,
        "skills": [
            "js-basics",
            "js-arrays",
            "js-functions",
            "js-async",
        ],
    },
    "java": {
        "name": "Java",
        "icon": "☕",
        "description": "Enterprise OOP: syntax, collections, JVM.",
        "coding": True,
        "skills": [
            "java-basics",
            "java-oop",
            "java-collections",
            "java-exceptions",
            "java-generics",
            "java-streams",
            "java-jvm",
        ],
    },
    "webdev": {
        "name": "Web Development",
        "icon": "🌐",
        "description": "HTML, CSS, and how the browser works.",
        "coding": True,
        "skills": [
            "html-basics",
            "css-basics",
            "css-layout",
            "css-responsive",
            "http-basics",
            "browser-dom",
            "browser-security",
            "browser-storage",
        ],
    },
    "ml-basics": {
        "name": "ML Basics",
        "icon": "🤖",
        "description": "Machine learning fundamentals and workflow.",
        "coding": True,
        "skills": [
            "ml-concepts",
            "ml-workflow",
            "ml-libraries",
            "ml-metrics",
        ],
    },
    "data-science": {
        "name": "Data Science",
        "icon": "📊",
        "description": "Pandas, NumPy, visualization, and modeling.",
        "coding": True,
        "skills": [
            "pandas",
            "data-cleaning",
            "stats",
            "distributions",
            "hypothesis-testing",
            "data-visualization",
            "feature-engineering",
            "ml-features",
            "regression",
            "overfitting",
            "model-evaluation",
        ],
    },
    "data-analyst": {
        "name": "Data Analysis",
        "icon": "📈",
        "description": "SQL, spreadsheets, dashboards, business metrics.",
        "coding": True,
        "skills": [
            "sql",
            "sql-joins",
            "sql-aggregation",
            "excel",
            "pivot-tables",
            "data-types",
            "data-viz",
            "dashboards",
            "data-storytelling",
            "kpis",
            "business-metrics",
        ],
    },
    "r-lang": {
        "name": "R Language",
        "icon": "📉",
        "description": "Statistical computing with R.",
        "coding": True,
        "skills": [
            "r-basics",
            "r-dataframes",
            "r-factors",
            "r-functions",
            "r-apply",
            "r-dplyr",
            "r-ggplot2",
            "r-statistics",
        ],
    },
    "ruby": {
        "name": "Ruby",
        "icon": "💎",
        "description": "Elegant OOP scripting and Rails foundations.",
        "coding": True,
        "skills": [
            "ruby-basics",
            "ruby-oop",
            "ruby-blocks",
            "ruby-enumerables",
            "ruby-gems",
            "ruby-rails",
            "rails-basics",
        ],
    },
    "networking": {
        "name": "Computer Networking",
        "icon": "🛜",
        "description": "OSI, TCP/IP, DNS, routing — how the internet works.",
        "coding": False,
        "skills": [
            "networking-basics",
            "osi-model",
            "tcp-udp",
            "tcp-ip",
            "ip-addressing",
            "subnetting",
            "dns",
            "http",
            "http-protocols",
            "routing",
            "vpn",
            "latency",
            "networking-protocols",
            "networking-security",
        ],
    },
    "devops": {
        "name": "DevOps",
        "icon": "🛠️",
        "description": "Linux, CI/CD, containers, and cloud operations.",
        "coding": False,
        "skills": [
            "linux-basics",
            "git",
            "git-ops",
            "cicd",
            "docker",
            "kubernetes",
            "kubernetes-basics",
            "iac",
            "deployment",
            "cloud-basics",
            "monitoring",
        ],
    },
}


def get_skills_for_topic(slug: str) -> list[str]:
    """Skill tags for a topic slug. Unknown slugs → []."""
    entry = DOMAIN_SKILLS.get(slug)
    return list(entry["skills"]) if entry else []


def is_coding_topic(slug: str) -> bool:
    """True if the topic trains via code-lab; False → visual/theory."""
    entry = DOMAIN_SKILLS.get(slug)
    return bool(entry and entry["coding"])


def auto_skills_for_goal(topics: list[str]) -> list[str]:
    """Deduped skill tags across goal topics, in topic-then-skill order.

    This is the "auto add skills" feature: a user's goal topics fully
    determine their required skills — no manual skill entry needed.
    Unknown topic slugs are skipped silently.
    """
    seen: set[str] = set()
    out: list[str] = []
    for topic in topics:
        for skill in get_skills_for_topic(topic):
            if skill not in seen:
                seen.add(skill)
                out.append(skill)
    return out


def list_topics() -> list[str]:
    """All registered topic slugs."""
    return list(DOMAIN_SKILLS.keys())
