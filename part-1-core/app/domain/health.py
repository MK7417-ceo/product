"""Domain layer — PURE business logic.

No FastAPI, no SQLAlchemy, no HTTP clients, no framework imports.
Everything here is unit-testable with zero infrastructure.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ComponentStatus:
    name: str
    ok: bool
    detail: str = ""


@dataclass(frozen=True)
class SystemStatus:
    ok: bool
    components: tuple[ComponentStatus, ...]

    def summary(self) -> str:
        bad = [c.name for c in self.components if not c.ok]
        if not bad:
            return "all systems operational"
        return "degraded: " + ", ".join(bad)


def assess_system(results: list[tuple[str, bool, str]]) -> SystemStatus:
    """Pure aggregation: component (name, ok, detail) triples -> SystemStatus."""
    components = tuple(ComponentStatus(name=n, ok=ok, detail=d) for n, ok, d in results)
    return SystemStatus(ok=all(c.ok for c in components), components=components)
