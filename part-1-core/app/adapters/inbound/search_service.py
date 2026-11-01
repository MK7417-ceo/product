"""Inbound adapter: implements the SearchService port."""
from __future__ import annotations

from app.domain.search import (
    SearchResult,
    build_snippet,
    mark_matches,
    score_candidate,
    validate_query,
    validate_types,
)
from app.domain.user import DomainError


class SearchServiceImpl:
    def __init__(self, search_repo) -> None:
        self._repo = search_repo

    def search(self, user_id: str, query: str, types: str | None = None,
               limit: int = 20) -> list[SearchResult]:
        terms = validate_query(query)
        wanted = validate_types(types)
        if not 1 <= limit <= 50:
            raise DomainError("limit must be between 1 and 50")

        candidates = self._repo.search(user_id, terms, wanted)
        results: list[SearchResult] = []
        for c in candidates:
            score = score_candidate(c["title"], c["body"], terms)
            if score <= 0:
                continue
            created = c["created_at"]
            results.append(SearchResult(
                type=c["type"],
                id=c["id"],
                title=mark_matches(c["title"], terms),
                snippet=build_snippet(c["body"], terms),
                score=round(score, 2),
                created_at=created.isoformat() if hasattr(created, "isoformat") else str(created),
            ))
        results.sort(key=lambda r: (-r.score, r.created_at))
        return results[:limit]
