"""Domain unit tests — zero infrastructure, pure logic."""
from app.domain.health import SystemStatus, assess_system


def test_all_healthy():
    status = assess_system([("database", True, "reachable"), ("api", True, "serving")])
    assert isinstance(status, SystemStatus)
    assert status.ok is True
    assert status.summary() == "all systems operational"


def test_one_component_down():
    status = assess_system([("database", False, "refused"), ("api", True, "serving")])
    assert status.ok is False
    assert "database" in status.summary()
    assert len(status.components) == 2


def test_status_is_immutable():
    status = assess_system([("api", True, "serving")])
    try:
        status.ok = False  # frozen dataclass must reject
    except Exception:
        pass
    assert status.ok is True
