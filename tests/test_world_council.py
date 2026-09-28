from world.council import AGENTS, WorldCouncil
from world.sim import create_world, spawn_entity


def test_council_has_six_roles():
    assert len(AGENTS) == 6
    assert len({agent.agent_id for agent in AGENTS}) == 6


def test_council_grows_world():
    world = create_world(width=12, height=8, seed=7)
    spawn_entity(world, "genesis")
    result = WorldCouncil(world).tick()
    assert any(item.get("action") == "spawn" for item in result.executed)
    assert len(world.entities) >= 2


def test_council_is_bounded():
    world = create_world(width=8, height=8, seed=1)
    spawn_entity(world, "genesis")
    result = WorldCouncil(world, max_actions_per_tick=3).tick()
    assert len(result.proposals) >= 1
    assert len(result.executed) <= 3
