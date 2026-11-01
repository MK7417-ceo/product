"""Pure domain logic for global search.

Mirrors how Apple Notes search behaves, adapted to SKILL_FORGE content:
- one query searches across many content types (roadmaps, tasks, evidence,
  assessments, certificates) — like Notes searching every note at once;
- title matches rank above body matches;
- every hit carries a snippet showing the match in context, with the matched
  terms wrapped in <mark> (like Notes highlighting the matched text);
- all HTML is escaped before marking, so result HTML is safe to inject.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from html import escape

#: content types the global search knows about
SEARCH_TYPES = ("roadmap", "task", "evidence", "assessment", "certificate")

#: title hits outrank body hits — same idea as Notes surfacing title
#: matches first when you search from Spotlight.
_TITLE_WEIGHT = 10.0
_BODY_WEIGHT = 1.0

_SNIPPET_RADIUS = 60


@dataclass
class SearchResult:
    type: str
    id: str
    title: str  # safe HTML: escaped, matches wrapped in <mark>
    snippet: str  # safe HTML: escaped, matches wrapped in <mark>
    score: float
    created_at: str
    extra: dict = field(default_factory=dict)


def tokenize(query: str) -> list[str]:
    """Split a query into lowercase search terms, dropping empties."""
    return [t for t in query.casefold().split() if t]


def _find_spans(text: str, terms: list[str]) -> list[tuple[int, int]]:
    """Case-insensitive match spans for any term, merged and sorted."""
    lowered = text.casefold()
    spans: list[tuple[int, int]] = []
    for term in terms:
        start = 0
        while True:
            idx = lowered.find(term, start)
            if idx == -1:
                break
            spans.append((idx, idx + len(term)))
            start = idx + 1
    spans.sort()
    merged: list[tuple[int, int]] = []
    for s, e in spans:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    return merged


def mark_matches(text: str, terms: list[str]) -> str:
    """Escape HTML in *text*, wrapping every term match in <mark>."""
    spans = _find_spans(text, terms)
    if not spans:
        return escape(text)
    out: list[str] = []
    pos = 0
    for s, e in spans:
        out.append(escape(text[pos:s]))
        out.append(f"<mark>{escape(text[s:e])}</mark>")
        pos = e
    out.append(escape(text[pos:]))
    return "".join(out)


def score_candidate(title: str, body: str, terms: list[str]) -> float:
    """Rank a candidate: title term hits weigh far more than body hits."""
    title_spans = _find_spans(title, terms)
    body_spans = _find_spans(body, terms)
    if not title_spans and not body_spans:
        return 0.0
    # distinct terms matched matters more than raw hit count
    title_terms = {t for t in terms if t in title.casefold()}
    body_terms = {t for t in terms if t in body.casefold()}
    coverage = (len(title_terms) + len(body_terms)) / (2 * len(terms))
    return (
        len(title_spans) * _TITLE_WEIGHT
        + len(body_spans) * _BODY_WEIGHT
        + coverage * 5.0
    )


def build_snippet(body: str, terms: list[str], radius: int = _SNIPPET_RADIUS) -> str:
    """Snippet of *body* centred on the first match, matches marked.

    Like Notes showing the matched line in context under the note title.
    """
    spans = _find_spans(body, terms)
    if not spans:
        head = body[: radius * 2].strip()
        return escape(head) + ("…" if len(body) > radius * 2 else "")
    first = spans[0][0]
    start = max(0, first - radius)
    end = min(len(body), spans[-1][1] + radius)
    # don't cut words at the edges
    while start > 0 and not body[start].isspace():
        start -= 1
    while end < len(body) and not body[end].isspace():
        end += 1
    window = body[start:end].strip()
    prefix = "…" if start > 0 else ""
    suffix = "…" if end < len(body) else ""
    return prefix + mark_matches(window, terms) + suffix


def validate_query(query: str) -> list[str]:
    """Validate a raw query string, returning its terms or raising."""
    from app.domain.user import DomainError  # local import: avoid cycle

    q = query.strip()
    if len(q) < 2:
        raise DomainError("search query must be at least 2 characters")
    if len(q) > 100:
        raise DomainError("search query must be at most 100 characters")
    terms = tokenize(q)
    if not terms:
        raise DomainError("search query must contain searchable text")
    return terms


def validate_types(types: str | None) -> tuple[str, ...]:
    """Validate a comma-separated type filter, defaulting to all types."""
    from app.domain.user import DomainError  # local import: avoid cycle

    if not types:
        return SEARCH_TYPES
    wanted = tuple(t.strip().lower() for t in types.split(",") if t.strip())
    if not wanted:
        return SEARCH_TYPES
    unknown = [t for t in wanted if t not in SEARCH_TYPES]
    if unknown:
        raise DomainError(f"unknown search types: {', '.join(unknown)}")
    # de-dupe, keep canonical order
    return tuple(t for t in SEARCH_TYPES if t in wanted)
