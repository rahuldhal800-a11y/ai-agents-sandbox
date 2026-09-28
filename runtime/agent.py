"""Safe agent abstraction for the AI Agents Sandbox.

Agents receive an execution function explicitly. This layer never grants host,
production, or unrestricted credential access by itself.
"""

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class Agent:
    agent_id: str
    name: str
    executor: Callable[[dict[str, Any]], dict[str, Any]] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def run(self, task: dict[str, Any]) -> dict[str, Any]:
        if self.executor is None:
            return {
                "status": "blocked",
                "reason": "No execution backend configured",
                "agent_id": self.agent_id,
            }

        result = self.executor(task)
        return {
            "status": "completed",
            "agent_id": self.agent_id,
            "result": result,
        }
