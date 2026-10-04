"""Inbound adapter: implements the HealthService port."""
from __future__ import annotations

from app.domain.health import SystemStatus, assess_system
from app.ports.outbound import DatabaseProbe


class SystemHealthService:
    def __init__(self, db_probe: DatabaseProbe) -> None:
        self._db_probe = db_probe

    def get_status(self) -> SystemStatus:
        db_ok, db_detail = self._db_probe.check()
        return assess_system(
            [
                ("database", db_ok, db_detail),
                ("api", True, "serving requests"),
            ]
        )
