"""Domain: Career Launchpad — resume + JD matching. PURE.

The JD matcher is deliberately explainable and deterministic: keyword
overlap between the JD and the resume, weighted by JD frequency. No LLM,
no black box — the user sees exactly which keywords matched and which
are missing, with concrete suggestions.
"""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field

from app.domain.user import DomainError

STOPWORDS = frozenset("""
a an the and or but of to in on for with as at by from is are was were be
been being will would should could can may might must shall do does did
have has had having this that these those it its we you they he she our
your their his her him them us me my mine yours theirs ours i me
who whom whose what which when where why how all any both each few more
most other some such no nor not only own same so than too very
looking seek seeking join team work working ability able strong proven
experience experienced years year plus including include includes including
etc role position opportunity opportunities candidate candidates
you'll we're we're we've they'll develop developing developed
hiring hire required requirement requirements must know knowledge
preferred prefer bonus plus day days onsite remote hybrid full-time
full time part-time contract ctc salary compensation benefits
company companies client customer business businesses product products
project projects deliver deliverables stakeholder stakeholders
apply application applications resume cv cover letter interview hiring
manager team teams lead leadership mentorship mentor collaborate
collaboration cross-functional agile scrum sprint standup
fast-paced fast paced dynamic environment culture values mission
vision passionate passion enthusiastic love lover ninja guru rockstar
wizard evangelist thought leader
growth grow growing scale scaling large-scale high-performance
best practices standards quality clean maintainable robust reliable
secure security compliance ownership end-to-end e2e lifecycle
design designed architect architecture implement implementation
build building built ship shipping deploy deployment production
monitor monitoring debug debugging troubleshoot troubleshooting
optimize optimization performance tune tuning refactor refactoring
test testing tested tests tdd ci cd pipeline pipelines automation
document documentation document docs write writing written review
reviews code review reviews peer feedback communicate communication
present presentation present articulate explain collaborate partner
stakeholder management independently independent self-starter
self motivated proactive ownership accountability responsible
deadline deadlines prioritize prioritization multitask
bachelor masters degree btech mtech phd computer science engineering
related field equivalent practical relevant hands-on
familiar familiarity exposure understanding understand solid grasp
excellent outstanding exceptional superior remarkable amazing great good
nice ideally ideally bonus points extra credit
come comes coming go goes going get gets getting make makes making
take takes taking give gives giving use uses using used utilize
utilizes part within without within across per via upon onto
across between among around along across throughout toward towards
under over above below up down out off again further once here there
when where which while during before after above below up down
out off over under again further then once here there when where why
how all any both each few more most other some such no nor not only
own same so than too very can will just don should now
""".split())

_WORD_RE = re.compile(r"[a-z0-9]+(?:[+#][a-z0-9]+)?")


def keywords(text: str) -> Counter:
    """Lowercased content words with frequencies."""
    words = _WORD_RE.findall(text.lower())
    return Counter(w for w in words if w not in STOPWORDS and len(w) > 1)


@dataclass(frozen=True)
class Experience:
    title: str
    company: str
    start: str = ""
    end: str = ""
    bullets: tuple[str, ...] = ()

    def validate(self) -> None:
        if not self.title.strip() or not self.company.strip():
            raise DomainError("experience needs title and company")


@dataclass(frozen=True)
class Project:
    name: str
    description: str = ""
    tech: tuple[str, ...] = ()
    link: str = ""

    def validate(self) -> None:
        if not self.name.strip():
            raise DomainError("project needs a name")


@dataclass(frozen=True)
class Education:
    degree: str
    school: str
    year: str = ""

    def validate(self) -> None:
        if not self.degree.strip() or not self.school.strip():
            raise DomainError("education needs degree and school")


@dataclass(frozen=True)
class Resume:
    id: str
    user_id: str
    title: str
    summary: str = ""
    skills: tuple[str, ...] = ()
    experience: tuple[Experience, ...] = ()
    projects: tuple[Project, ...] = ()
    education: tuple[Education, ...] = ()
    links: dict = field(default_factory=dict)

    def validate(self) -> None:
        if not self.title.strip():
            raise DomainError("resume needs a title")
        for e in self.experience:
            e.validate()
        for p in self.projects:
            p.validate()
        for ed in self.education:
            ed.validate()

    def full_text(self) -> str:
        parts = [self.title, self.summary, *self.skills]
        for e in self.experience:
            parts += [e.title, e.company, *e.bullets]
        for p in self.projects:
            parts += [p.name, p.description, *p.tech]
        for ed in self.education:
            parts += [ed.degree, ed.school]
        return "\n".join(parts)


@dataclass(frozen=True)
class KeywordHit:
    keyword: str
    jd_count: int


@dataclass(frozen=True)
class JDMatch:
    score: float  # 0..100
    matched: tuple[KeywordHit, ...]
    missing: tuple[KeywordHit, ...]
    suggestions: tuple[str, ...]
    jd_keyword_count: int

    @property
    def matched_count(self) -> int:
        return len(self.matched)


def match_jd(resume: Resume, jd_text: str, top_missing: int = 10) -> JDMatch:
    """Score a resume against a job description. Deterministic."""
    if not jd_text or not jd_text.strip():
        raise DomainError("jd_text must not be empty")
    jd_kw = keywords(jd_text)
    if not jd_kw:
        raise DomainError("jd_text has no meaningful keywords")
    resume_words = set(keywords(resume.full_text()))
    total = sum(jd_kw.values())
    matched = tuple(KeywordHit(k, c) for k, c in jd_kw.most_common()
                    if k in resume_words)
    missing = tuple(KeywordHit(k, c) for k, c in jd_kw.most_common()
                    if k not in resume_words)
    hit_weight = sum(h.jd_count for h in matched)
    score = round(100 * hit_weight / total, 1)
    suggestions = tuple(
        f"Add '{h.keyword}' (mentioned {h.jd_count}x in the JD) — "
        f"a bullet or skill that proves it"
        for h in missing[:top_missing]
    )
    return JDMatch(score=score, matched=matched, missing=missing,
                   suggestions=suggestions, jd_keyword_count=len(jd_kw))
