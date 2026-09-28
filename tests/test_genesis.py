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


def test_world_has_real_terrain_and_resources():
    being = Genesis()
    assert len(being.world.state["terrain"]) == being.world.height
    assert len(being.world.state["resources"]) > 0
    before = (being.world.genesis["x"], being.world.genesis["y"])
    being.autonomous_step()
    assert being.steps == 1
    assert being.learner.history
    assert being.world.clock == 1
    assert before != (being.world.genesis["x"], being.world.genesis["y"]) or being.world.genesis["energy"] < 100


def test_policy_evolves():
    being = Genesis()
    for _ in range(25):
        being.autonomous_step()
    assert being.mutations == 1
