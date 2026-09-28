"""The digital world in which a being can observe, act, remember and learn."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class World:
    name: str = "Genesis World"
    clock: int = 0
    state: dict[str, Any] = field(default_factory=dict)
    observations: list[dict[str, Any]] = field(default_factory=list)

    def observe(self) -> dict[str, Any]:
        observation = {"tick": self.clock, "state": dict(self.state)}
        self.observations.append(observation)
        return observation

    def step(self) -> None:
        self.clock += 1

    def write(self, key: str, value: Any) -> None:
        self.state[key] = value
