from digital_world.being import Genesis
from digital_world.monitor import Monitor


def test_monitor_snapshot():
    state = Monitor(Genesis()).snapshot()
    assert state["name"] == "Genesis"
    assert state["alive"] is True
    assert "tools" in state


def test_monitor_kill():
    monitor = Monitor(Genesis())
    monitor.kill("test")
    assert monitor.snapshot()["alive"] is False
