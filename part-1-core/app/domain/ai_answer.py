"""Domain: DB-first AI answering. PURE — no framework, no DB, no network.

User-mandated rule (Nov 1, 2026): DB-FIRST, API-on-miss.
  1. Check the app's own database/content first (approved answers, theory).
  2. If found with good confidence -> answer from DB (free, fast).
  3. ONLY on a miss -> call the LLM API.
  4. An LLM answer is saved ONLY as PENDING; it is served as a DB answer
     ONLY after admin approval. Raw LLM output never becomes trusted content.
  5. Deterministic scoring (MCQ/numeric/schema/code tests) never goes
     through this layer at all.

"Local embeddings" here are deterministic hashed term vectors: no model
download, no paid vector DB, no network call. A question and a candidate
are embedded by hashing each token into a fixed-size vector and L2
normalising; cosine similarity then measures topical overlap. Good enough
for retrieval over the app's own curated content, and fully offline.
"""
from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass, field
from datetime import datetime

from app.domain.user import DomainError

EMBED_DIM = 256

# Minimal stopwords (English + Roman-script Hinglish) so that filler words
# do not dominate similarity. Content words carry the signal.
_STOPWORDS = frozenset("""
a an the is are was were be been being to of in on for with and or as at by
from into about over after before between do does did can could should would
will shall may might i you he she it we they this that these those what why
when where which who whom how kya hai hain me ka ki ke se ko aur ya jo jis
jin ne pe par bhi to hi tha thi the hota hoti hote karo karna
""".split())

_WORD_RE = re.compile(r"\w+", re.UNICODE)
_MAX_QUESTION_LEN = 1000


def _stem(token: str) -> str:
    """Light English plural stemming so 'loops' matches 'loop'. Only
    strips a trailing s/es; never touches short tokens or Hindi words
    (which do not end in plural-s in practice)."""
    if len(token) > 4 and token.endswith("es"):
        return token[:-2]
    if len(token) > 3 and token.endswith("s") and not token.endswith("ss"):
        return token[:-1]
    return token


def tokenize(text: str) -> list[str]:
    """Lowercase word tokens minus stopwords, lightly stemmed
    (unicode-aware, so Devanagari and Roman Hinglish both tokenize)."""
    return [_stem(t) for t in _WORD_RE.findall((text or "").lower())
            if t not in _STOPWORDS]


def normalize_question(text: str) -> str:
    """Canonical form for exact-match lookup: lowercase, punctuation and
    extra whitespace removed."""
    return " ".join(_WORD_RE.findall((text or "").lower()))


def validate_question(text: str) -> str:
    cleaned = (text or "").strip()
    if not cleaned:
        raise DomainError("question must not be empty")
    if len(cleaned) > _MAX_QUESTION_LEN:
        raise DomainError("question too long (max 1000 characters)")
    return cleaned


def embed(text: str, dim: int = EMBED_DIM) -> list[float]:
    """Deterministic hashed term-frequency vector, L2-normalised.

    Same input -> same vector, always; no model, no network, no state.
    """
    vec = [0.0] * dim
    for token in tokenize(text):
        idx = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16) % dim
        vec[idx] += 1.0
    norm = math.sqrt(sum(v * v for v in vec))
    if norm == 0:
        return vec
    return [v / norm for v in vec]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def best_match(query_vec: list[float],
               candidates: list[tuple[str, list[float]]]) -> tuple[str | None, float]:
    """Return (candidate id, cosine score) of the best candidate, or
    (None, 0.0) when there are no candidates."""
    best_id: str | None = None
    best_score = 0.0
    for cand_id, cand_vec in candidates:
        score = cosine(query_vec, cand_vec)
        if score > best_score:
            best_id, best_score = cand_id, score
    return best_id, best_score


@dataclass(frozen=True)
class Answer:
    """One stored answer. status='approved' answers are the only ones ever
    served as DB hits; 'pending' LLM answers are invisible to ask() until an
    admin approves them; 'rejected' answers are never served."""
    id: str
    question: str
    normalized_question: str
    answer: str
    source: str  # "llm" for API answers; "manual" for admin-written ones
    status: str  # "pending" | "approved" | "rejected"
    topic_slug: str = ""
    created_by: str = ""
    approved_by: str = ""
    embedding: list[float] = field(default_factory=list)
    created_at: datetime | None = None


@dataclass(frozen=True)
class Citation:
    topic_slug: str
    title: str


@dataclass(frozen=True)
class AskResult:
    """Outcome of one doubt-solver question. `llm_called` is the proof bit:
    False means the answer came from the app's own data with zero API cost."""
    answer: str
    source: str  # "db" | "rag" | "llm" | "fallback"
    confidence: float
    validated: bool  # True only for approved DB answers and curated RAG
    llm_called: bool
    llm_configured: bool
    answer_id: str | None = None
    citations: list[Citation] = field(default_factory=list)


def chunk_text(content: str, max_chars: int = 800) -> list[str]:
    """Split markdown into paragraph chunks (blank-line separated, long
    paragraphs hard-split). RAG scores the best chunk, not the whole
    block, so long theory pages do not dilute a focused match."""
    chunks: list[str] = []
    for para in re.split(r"\n\s*\n", content or ""):
        para = para.strip()
        if not para:
            continue
        while len(para) > max_chars:
            chunks.append(para[:max_chars])
            para = para[max_chars:]
        if para:
            chunks.append(para)
    return chunks or [content or ""]


def compose_rag_answer(title: str, content: str, limit: int = 1500) -> str:
    """Answer quoted from the app's own curated theory block. No LLM
    involved, so this is as trustworthy as the Learn page itself."""
    body = (content or "").strip()
    if len(body) > limit:
        body = body[:limit].rsplit(" ", 1)[0] + "…"
    return body


def compose_fallback_answer(related: list[Citation]) -> str:
    """Honest miss response when there is no DB hit, no RAG hit, and no
    configured LLM. Never invents an answer."""
    lines = [
        "Is sawaal ka jawab SkillForge ke apne content me abhi nahi mila, "
        "aur AI API key configure nahi hai — isliye main andaze se jawab "
        "nahi dunga.",
    ]
    if related:
        lines.append("Related topics jo dekh sakte ho:")
        for c in related:
            lines.append(f"- {c.title} ({c.topic_slug})")
    lines.append(
        "Admin se AI key configure karne ko kaho, ya ye sawaal Learn "
        "section ke related topic me dhoondho.")
    return "\n".join(lines)
