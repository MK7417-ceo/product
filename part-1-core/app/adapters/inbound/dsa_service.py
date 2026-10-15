"""Inbound adapter: deterministic daily DSA problem picker."""
from __future__ import annotations

import hashlib

from app.adapters.outbound.dsa_bank import DSAProblem, get_problems


def _index_for_seed(seed: str, n: int) -> int:
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    return int(digest, 16) % n


def get_daily_dsa(seed: str) -> DSAProblem:
    """Return the DSA problem for the given seed (e.g. "2026-10-15").

    Deterministic: the same seed always yields the same problem.
    Uniform over the bank via SHA-256.
    """
    problems = get_problems()
    if not problems:
        raise ValueError("DSA bank is empty")
    return problems[_index_for_seed(seed, len(problems))]
