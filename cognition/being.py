"""First autonomous digital being runtime."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from cognition.core import CognitiveKernel, Experience, Thought
from world.model import WorldState


@dataclass
class DigitalBeing:
    being_id: str
    kernel: CognitiveKernel = field(default_factory=CognitiveKernel)
    goals: list[str] = field(default_factory=lambda: ["understand_world"])
    alive: bool = True

    def perceive(self, world: WorldState) -> dict[str, Any]:
        entity = world.entities[self.being_id]
        cell = world.cell_at(entity.x, entity.y)
        return {
            "tick": world.tick,
            "position": [entity.x, entity.y],
            "terrain": cell.terrain,
            "temperature": cell.temperature,
            "water": cell.water,
            "resources": dict(cell.resources),
            "energy": entity.energy,
            "age": entity.age,
            "population": len(world.entities),
        }

    def think(self, observation: dict[str, Any]) -> Thought:
        generators = [
            lambda o: Thought("observe", "inspect environment", 0.50),
            lambda o: Thought("explore", "move toward information or resources", 0.55),
            lambda o: Thought("learn", "record and compare the current experience", 0.60),
            lambda o: Thought("develop", "create a capability when useful", 0.52),
        ]
        candidates = self.kernel.generate_thoughts(observation, generators)
        return self.kernel.choose(candidates)

    def cycle(self, world: WorldState) -> Thought:
        if not self.alive:
            raise RuntimeError("digital being is inactive")
        observation = self.perceive(world)
        thought = self.think(observation)
        outcome = {"selected": thought.kind, "confidence": thought.confidence}
        self.kernel.learn(
            Experience(
                observation=observation,
                action=thought.kind,
                outcome=outcome,
                reward=thought.confidence,
            )
        )
        world.entities[self.being_id].memory.append(outcome)
        return thought

    def snapshot(self) -> dict[str, Any]:
        return {
            "id": self.being_id,
            "goals": list(self.goals),
            "alive": self.alive,
            "cognition": self.kernel.snapshot(),
        }
