from runtime.agent import Agent
from runtime.evaluator import Evaluator
from runtime.policy import CapabilityPolicy


def test_agent_uses_injected_executor():
    agent = Agent(
        agent_id="test-agent",
        name="Test Agent",
        executor=lambda task: {"echo": task["goal"]},
    )

    result = agent.run({"goal": "solve a test problem"})

    assert result["status"] == "completed"
    assert result["result"]["echo"] == "solve a test problem"


def test_production_access_is_denied_by_default():
    policy = CapabilityPolicy()

    assert policy.allows("code_execution")
    assert not policy.allows("production_access")
    assert not policy.allows("host_device_access")
    assert not policy.allows("unrestricted_secrets")


def test_evaluator_rejects_failed_runs():
    evaluation = Evaluator().evaluate({"status": "failed"})

    assert not evaluation.success
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
