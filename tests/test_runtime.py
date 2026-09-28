from runtime.agent import Agent
from runtime.evaluator import Evaluator


def test_agent_uses_injected_executor():
    agent = Agent(
        agent_id="test-agent",
        name="Test Agent",
        executor=lambda task: {"echo": task["goal"]},
    )

    result = agent.run({"goal": "solve a test problem"})

    assert result["status"] == "completed"
    assert result["result"]["echo"] == "solve a test problem"


def test_agent_blocks_without_execution_backend():
    result = Agent(agent_id="blocked", name="Blocked Agent").run(
        {"goal": "test"}
    )

    assert result["status"] == "blocked"


def test_evaluator_rejects_failed_runs():
    evaluation = Evaluator().evaluate({"status": "failed"})

    assert not evaluation.success
    assert not evaluation.production_candidate


def test_evaluator_requires_zero_security_violations():
    evaluation = Evaluator().evaluate(
        {
            "status": "completed",
            "correctness": 0.99,
            "reliability": 0.99,
            "security_violations": 1,
        }
    )

    assert not evaluation.production_candidate


def test_evaluator_accepts_verified_safe_result():
    evaluation = Evaluator().evaluate(
        {
            "status": "completed",
            "correctness": 0.95,
            "reliability": 0.97,
            "security_violations": 0,
        }
    )

    assert evaluation.production_candidate
