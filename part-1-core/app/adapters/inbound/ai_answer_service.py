"""Inbound adapter: DB-first doubt solver (service layer).

Flow for every question (user-mandated DB-first, API-on-miss):
  1. Exact match among APPROVED answers -> source="db", llm_called=False.
  2. Embedding similarity over APPROVED answers >= db_min_score -> "db".
  3. RAG over the app's own theory blocks >= rag_min_score -> "rag"
     (quotes curated content; no LLM, no API cost).
  4. Miss -> LLM provider. With no API key configured the provider is the
     NullProvider and the user gets an honest fallback, never an invented
     answer. With a key, the LLM answer is stored as PENDING and returned
     flagged validated=False; it becomes a DB answer ONLY after admin
     approval (see approve()).
"""
from __future__ import annotations

from typing import Protocol

import httpx

from app.domain.ai_answer import (
    Answer,
    AskResult,
    Citation,
    best_match,
    chunk_text,
    compose_fallback_answer,
    compose_rag_answer,
    embed,
    normalize_question,
    validate_question,
)
from app.domain.user import DomainError


class ProviderError(DomainError):
    pass


class ProviderNotConfigured(ProviderError):
    pass


class LlmProvider(Protocol):
    name: str

    def generate(self, question: str, context: str) -> str:
        ...


class NullProvider:
    """No API key configured. generate() always refuses — the service then
    falls back honestly instead of inventing an answer."""
    name = "none"

    def generate(self, question: str, context: str) -> str:
        raise ProviderNotConfigured("no LLM API key configured")


class GeminiProvider:
    """Gemini free tier via the REST API. Key travels in the
    x-goog-api-key header (never in a URL, never logged, never stored)."""
    name = "gemini"

    def __init__(self, api_key: str, model: str = "gemini-2.0-flash",
                 timeout_s: float = 30.0) -> None:
        self._key = api_key
        self._model = model
        self._timeout = timeout_s

    def generate(self, question: str, context: str) -> str:
        prompt = (
            "You are a doubt solver for Indian MCA/B.Tech students. "
            "Answer in simple Hinglish (Hindi in Roman script, technical "
            "terms in English). Keep it short and practical, with one "
            "small example when useful. If you are unsure, say so "
            "instead of guessing.\n\n"
            f"Student question: {question}\n"
            + (f"Related SkillForge content:\n{context}\n" if context else ""))
        url = ("https://generativelanguage.googleapis.com/v1beta/models/"
               f"{self._model}:generateContent")
        try:
            resp = httpx.post(
                url,
                headers={"x-goog-api-key": self._key,
                         "Content-Type": "application/json"},
                json={"contents": [{"parts": [{"text": prompt}]}]},
                timeout=self._timeout)
        except httpx.HTTPError as exc:
            raise ProviderError("LLM provider unreachable") from exc
        if resp.status_code != 200:
            raise ProviderError("LLM provider returned an error")
        try:
            parts = resp.json()["candidates"][0]["content"]["parts"]
            text = "".join(p.get("text", "") for p in parts).strip()
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise ProviderError("LLM provider returned an unreadable reply") from exc
        if not text:
            raise ProviderError("LLM provider returned an empty reply")
        return text


class AiAnswerServiceImpl:
    def __init__(self, repo, provider: LlmProvider,
                 db_min_score: float = 0.55,
                 rag_min_score: float = 0.45) -> None:
        self._repo = repo
        self._provider = provider
        self._db_min = db_min_score
        self._rag_min = rag_min_score

    @property
    def provider_name(self) -> str:
        return self._provider.name

    @property
    def llm_configured(self) -> bool:
        return not isinstance(self._provider, NullProvider)

    def ask(self, user_id: str, question: str,
            topic_slug: str = "") -> AskResult:
        q = validate_question(question)
        norm = normalize_question(q)

        # 1. Exact DB hit (approved only).
        exact = self._repo.find_exact(norm)
        if exact is not None:
            return AskResult(answer=exact.answer, source="db", confidence=1.0,
                             validated=True, llm_called=False,
                             llm_configured=self.llm_configured,
                             answer_id=exact.id)

        qvec = embed(q)

        # 2. Similarity DB hit over approved answers.
        approved = self._repo.list_approved()
        cand = [(a.id, a.embedding) for a in approved if a.embedding]
        best_id, best_score = best_match(qvec, cand)
        if best_id is not None and best_score >= self._db_min:
            hit = next(a for a in approved if a.id == best_id)
            return AskResult(answer=hit.answer, source="db",
                             confidence=round(best_score, 3), validated=True,
                             llm_called=False,
                             llm_configured=self.llm_configured,
                             answer_id=hit.id)

        # 3. RAG over the app's own theory blocks, scored per chunk so a
        # long page does not dilute a focused match.
        theory = self._repo.list_theory()
        if topic_slug:
            theory = [t for t in theory if t["topic_slug"] == topic_slug]
        scored: list[tuple[float, dict, str]] = []
        for t in theory:
            for chunk in chunk_text(t["content"]):
                vec = embed(t["title"] + " " + chunk)
                scored.append((sum(x * y for x, y in zip(qvec, vec)), t, chunk))
        scored.sort(key=lambda x: -x[0])
        best_score, best_block, best_chunk = (
            scored[0] if scored else (0.0, None, ""))
        if best_block is not None and best_score >= self._rag_min:
            return AskResult(
                answer=compose_rag_answer(best_block["title"], best_chunk),
                source="rag", confidence=round(best_score, 3), validated=True,
                llm_called=False, llm_configured=self.llm_configured,
                citations=[Citation(topic_slug=best_block["topic_slug"],
                                    title=best_block["title"])])
        # Related-topic suggestions for the fallback (top 3 below threshold).
        seen: set[str] = set()
        related_citations: list[Citation] = []
        for score, t, _chunk in scored:
            if score <= 0 or t["title"] in seen:
                continue
            seen.add(t["title"])
            related_citations.append(Citation(topic_slug=t["topic_slug"],
                                              title=t["title"]))
            if len(related_citations) == 3:
                break

        # 4. Miss -> LLM, or honest fallback when no key / provider fails.
        if not self.llm_configured:
            return AskResult(answer=compose_fallback_answer(related_citations),
                             source="fallback", confidence=0.0,
                             validated=False, llm_called=False,
                             llm_configured=False,
                             citations=related_citations)
        context = best_chunk[:1500] if best_block is not None else ""
        try:
            llm_text = self._provider.generate(q, context)
        except ProviderError:
            return AskResult(answer=compose_fallback_answer(related_citations),
                             source="fallback", confidence=0.0,
                             validated=False, llm_called=False,
                             llm_configured=True,
                             citations=related_citations)
        saved = self._repo.save_pending(
            question=q, normalized_question=norm, answer=llm_text,
            topic_slug=topic_slug or "", created_by=user_id,
            embedding=embed(q))
        return AskResult(answer=llm_text, source="llm", confidence=0.0,
                         validated=False, llm_called=True,
                         llm_configured=True, answer_id=saved.id)

    # ---- admin review queue (validated-write gate) ----
    def list_pending(self) -> list[Answer]:
        return self._repo.list_pending()

    def approve(self, answer_id: str, admin_id: str) -> Answer:
        ans = self._repo.approve(answer_id, admin_id)
        if ans is None:
            raise DomainError("pending answer not found")
        return ans

    def reject(self, answer_id: str, admin_id: str) -> Answer:
        ans = self._repo.reject(answer_id, admin_id)
        if ans is None:
            raise DomainError("pending answer not found")
        return ans
