"""Simple model-free learning primitives."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Experience:
    goal: str
    action: str
    result: Any
    reward: float


@dataclass
class Learner:
    values: dict[str, float] = field(default_factory=dict)
    history: list[Experience] = field(default_factory=list)

    def learn(self, experience: Experience) -> None:
        self.history.append(experience)
        old = self.values.get(experience.action, 0.0)
        self.values[experience.action] = old + 0.1 * (experience.reward - old)

    def best_action(self, actions: list[str]) -> str | None:
        return max(actions, key=lambda action: self.values.get(action, 0.0), default=None)
