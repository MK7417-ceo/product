"""Inbound ports — what the outside world may ask the domain core to do.

API routers depend on these protocols, never on concrete services.
"""
from __future__ import annotations

from typing import Protocol

from app.domain.health import SystemStatus


class HealthService(Protocol):
    def get_status(self) -> SystemStatus:
        """Return the current system status."""
        ...
