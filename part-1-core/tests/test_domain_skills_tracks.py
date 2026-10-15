"""Tests: domain skill registry + learning tracks."""
import re

from app.adapters.outbound import domain_skills as ds
from app.adapters.outbound import tracks as tr


def _bank_tags():
    src = open("app/adapters/outbound/question_bank.py").read()
    out = {}
    for m in re.finditer(
        r'_q\(\s*\"[a-z0-9-]+\"\s*,\s*\"([a-z0-9-]+)\"\s*,'
        r'\s*\"(?:beginner|intermediate|advanced|expert)\"\s*,\s*\"([a-z0-9-]+)\"',
        src,
    ):
        out.setdefault(m.group(1), set()).add(m.group(2))
    return out


def test_registry_covers_every_bank_skill_tag():
    bank = _bank_tags()
    assert bank, "bank should not be empty"
    for topic, tags in bank.items():
        assert topic in ds.DOMAIN_SKILLS, f"topic missing: {topic}"
        missing = tags - set(ds.get_skills_for_topic(topic))
        assert not missing, f"{topic} missing tags: {missing}"


def test_every_entry_has_required_fields():
    for slug, e in ds.DOMAIN_SKILLS.items():
        assert e["name"] and e["icon"] and e["description"]
        assert isinstance(e["coding"], bool)
        assert e["skills"] and len(e["skills"]) == len(set(e["skills"]))


def test_unknown_topic_returns_empty():
    assert ds.get_skills_for_topic("nope") == []
    assert ds.is_coding_topic("nope") is False


def test_auto_skills_dedupes_and_orders():
    skills = ds.auto_skills_for_goal(["python", "webdev", "python", "nope"])
    assert len(skills) == len(set(skills))
    assert skills[0] == ds.get_skills_for_topic("python")[0]
    assert set(skills) == set(ds.get_skills_for_topic("python")) | set(
        ds.get_skills_for_topic("webdev")
    )


def test_tracks_reference_valid_topics():
    for slug, t in tr.TRACKS.items():
        assert t["name"] and t["icon"] and t["description"]
        assert t["topics"] and t["duration_weeks"] > 0
        for topic in t["topics"]:
            assert topic in ds.DOMAIN_SKILLS, f"track {slug}: bad topic {topic}"


def test_get_track_unknown_returns_none():
    assert tr.get_track("nope") is None


def test_track_skills_matches_auto():
    for slug in tr.list_tracks():
        assert tr.track_skills(slug) == ds.auto_skills_for_goal(
            tr.TRACKS[slug]["topics"]
        )
        assert tr.track_skills(slug), f"track {slug} has no skills"


def test_six_tracks_present():
    assert set(tr.list_tracks()) == {
        "fullstack",
        "frontend",
        "backend",
        "data-scientist",
        "data-analyst",
        "devops-engineer",
    }
