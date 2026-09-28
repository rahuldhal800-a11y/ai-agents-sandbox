from digital_world.being import Genesis
from digital_world.tools import Tool


def test_genesis_starts_without_model():
    being = Genesis()
    assert being.name == "Genesis"
    assert being.alive


def test_genesis_discovers_and_uses_tools():
    being = Genesis()
    being.tools.register(Tool("hello", "Return a constant.", lambda: "hello"))
    assert "hello" in being.discover_tools()
    assert being.act("hello") == "hello"


def test_genesis_learns_from_experience():
    being = Genesis()
    being.learn_from_result("test", "hello", "ok", 1.0)
    assert being.learner.values["hello"] > 0


def test_genesis_kill_switch():
    being = Genesis()
    being.kill("test stop")
    assert not being.alive
    assert being.act("anything")["status"] == "killed"
    being.reset()
    assert being.alive
