"""Agent runtime with an operator-controlled kill switch."""

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class KillSwitch:
    killed: bool = False
    reason: str | None = None

    def kill(self, reason: str = "Emergency stop") -> None:
        self.killed = True
        self.reason = reason

    def reset(self) -> None:
        self.killed = False
        self.reason = None


@dataclass
class Agent:
    agent_id: str
    name: str
    executor: Callable[[dict[str, Any]], dict[str, Any]] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    kill_switch: KillSwitch = field(default_factory=KillSwitch)

    def kill(self, reason: str = "Emergency stop") -> None:
        self.kill_switch.kill(reason)

    def reset(self) -> None:
        self.kill_switch.reset()

    @property
    def is_killed(self) -> bool:
        return self.kill_switch.killed

    def run(self, task: dict[str, Any]) -> dict[str, Any]:
        if self.is_killed:
            return {
                "status": "killed",
                "reason": self.kill_switch.reason or "Agent has been killed",
                "agent_id": self.agent_id,
            }
        if self.executor is None:
            return {
                "status": "blocked",
                "reason": "No execution backend configured",
                "agent_id": self.agent_id,
            }
        result = self.executor(task)
        return {"status": "completed", "agent_id": self.agent_id, "result": result}
