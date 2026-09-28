from runtime.agent import Agent


def test_agent_uses_injected_executor():
    agent = Agent(
        agent_id="test-agent",
        name="Test Agent",
        executor=lambda task: {"echo": task["goal"]},
    )
    result = agent.run({"goal": "solve a test problem"})
    assert result["status"] == "completed"


def test_agent_kill_switch_stops_future_runs():
    agent = Agent(
        agent_id="test-agent",
        name="Test Agent",
        executor=lambda task: {"echo": task["goal"]},
    )
    agent.kill("Operator emergency stop")
    result = agent.run({"goal": "must not execute"})
    assert agent.is_killed
    assert result["status"] == "killed"
    assert result["reason"] == "Operator emergency stop"


def test_agent_can_be_reset_by_operator():
    agent = Agent(
        agent_id="test-agent",
        name="Test Agent",
        executor=lambda task: {"echo": task["goal"]},
    )
    agent.kill()
    agent.reset()
    result = agent.run({"goal": "run after reset"})
    assert not agent.is_killed
    assert result["status"] == "completed"
