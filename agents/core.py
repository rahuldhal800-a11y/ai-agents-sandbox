"""Production-oriented autonomous agent core.

The core is provider-neutral: model inference and sandbox execution are injected
through interfaces. Agents can reason, plan, act through scoped tools, evaluate
results, reflect, and continue until the objective is complete or a policy
boundary stops the run.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol, Sequence


class AgentState(str, Enum):
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    EVALUATING = "evaluating"
    REFLECTING = "reflecting"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


@dataclass(frozen=True)
class AgentGoal:
    objective: str
    success_criteria: Sequence[str] = ()


@dataclass
class AgentObservation:
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentAction:
    tool: str
    arguments: dict[str, Any] = field(default_factory=dict)
    rationale: str = ""


@dataclass
class AgentResult:
    state: AgentState
    objective: str
    iterations: int
    observations: list[AgentObservation] = field(default_factory=list)
    error: str | None = None


class IntelligenceProvider(Protocol):
    """Adapter implemented by an LLM/agent provider."""

    def plan(self, goal: AgentGoal, context: Sequence[AgentObservation]) -> list[AgentAction]: ...
    def evaluate(self, goal: AgentGoal, context: Sequence[AgentObservation]) -> bool: ...
    def reflect(self, goal: AgentGoal, context: Sequence[AgentObservation]) -> AgentObservation: ...


class ToolRuntime(Protocol):
    """Scoped tool execution supplied by the sandbox runtime."""

    def execute(self, action: AgentAction) -> AgentObservation: ...


class MemoryStore(Protocol):
    def remember(self, goal: AgentGoal, observation: AgentObservation) -> None: ...


@dataclass
class AutonomousAgent:
    name: str
    intelligence: IntelligenceProvider
    tools: ToolRuntime
    memory: MemoryStore
    state: AgentState = AgentState.IDLE

    def run(self, goal: AgentGoal, *, max_iterations: int | None = None) -> AgentResult:
        """Run continuously until completion or a configured hard boundary.

        ``max_iterations`` is optional intentionally. Production orchestration
        should normally enforce resource/time/policy budgets at the runtime layer.
        """
        observations: list[AgentObservation] = []
        iterations = 0

        while max_iterations is None or iterations < max_iterations:
            iterations += 1
            try:
                self.state = AgentState.PLANNING
                actions = self.intelligence.plan(goal, observations)
                if not actions:
                    self.state = AgentState.EVALUATING
                    if self.intelligence.evaluate(goal, observations):
                        self.state = AgentState.COMPLETED
                        return AgentResult(self.state, goal.objective, iterations, observations)
                    self.state = AgentState.REFLECTING
                    reflection = self.intelligence.reflect(goal, observations)
                    observations.append(reflection)
                    self.memory.remember(goal, reflection)
                    continue

                self.state = AgentState.EXECUTING
                for action in actions:
                    observation = self.tools.execute(action)
                    observations.append(observation)
                    self.memory.remember(goal, observation)

                self.state = AgentState.EVALUATING
                if self.intelligence.evaluate(goal, observations):
                    self.state = AgentState.COMPLETED
                    return AgentResult(self.state, goal.objective, iterations, observations)

                self.state = AgentState.REFLECTING
                reflection = self.intelligence.reflect(goal, observations)
                observations.append(reflection)
                self.memory.remember(goal, reflection)
            except PermissionError as exc:
                self.state = AgentState.BLOCKED
                return AgentResult(self.state, goal.objective, iterations, observations, str(exc))
            except Exception as exc:
                self.state = AgentState.FAILED
                return AgentResult(self.state, goal.objective, iterations, observations, str(exc))

        self.state = AgentState.BLOCKED
        return AgentResult(
            self.state,
            goal.objective,
            iterations,
            observations,
            "Execution budget reached before objective completion",
        )
