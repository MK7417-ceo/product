"""Outbound ports — what the domain core needs from the outside world.

Adapters implement these. The core never imports an adapter.
"""
from __future__ import annotations

from typing import Protocol


class DatabaseProbe(Protocol):
    def check(self) -> tuple[bool, str]:
        """Return (reachable, detail). Must never raise."""
        ...
