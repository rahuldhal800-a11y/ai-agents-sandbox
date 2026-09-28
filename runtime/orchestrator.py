"""Minimal autonomous sandbox orchestrator scaffold.

The production implementation should plug isolated runtimes, tools, memory,
experiments, evaluators, and a scoped secret gateway into this loop.
"""

from dataclasses import dataclass, field
from typing import Callable


@dataclass
class ExperimentResult:
    success: bool
    observations: dict = field(default_factory=dict)
    error: str | None = None


@dataclass
class AgentTask:
    goal: str
    max_iterations: int = 10
    iteration: int = 0


class AutonomousLoop:
    def __init__(self, executor: Callable[[AgentTask], ExperimentResult]):
        self.executor = executor

    def run(self, task: AgentTask) -> ExperimentResult:
        last = ExperimentResult(False, error="No execution attempted")
        while task.iteration < task.max_iterations:
            task.iteration += 1
            last = self.executor(task)
            if last.success:
                return last
            # Future implementation: diagnose, generate a repair plan,
            # apply it in an isolated workspace, then retry.
        return last


if __name__ == "__main__":
    def demo(task: AgentTask) -> ExperimentResult:
        return ExperimentResult(
            success=True,
            observations={"goal": task.goal, "iteration": task.iteration},
        )

    result = AutonomousLoop(demo).run(AgentTask("bootstrap sandbox"))
    print(result)
