"""Agent abstraction used by the sandbox orchestrator."""

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class Observation:
    success: bool
    output: str = ""
    metrics: dict[str, float] = field(default_factory=dict)
    error: str | None = None


class Agent(Protocol):
    name: str

    def run(self, goal: str, context: dict) -> Observation:
        ...


@dataclass
class SandboxAgent:
    name: str

    def run(self, goal: str, context: dict) -> Observation:
        # Deliberately deterministic placeholder. The execution backend will
        # be injected later; agents never receive raw host credentials here.
        return Observation(
            success=True,
            output=f"Sandbox agent '{self.name}' accepted goal: {goal}",
        )
