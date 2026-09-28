"""Civilization-scale primitives.

There is intentionally no population ceiling here. The simulation can spawn
additional digital beings when an agent chooses to do so; the experiment
measures what those beings actually do rather than imposing a design limit.
"""

from __future__ import annotations

from dataclasses import dataclass

from .model import Entity, WorldState
from .sim import spawn_entity


@dataclass
class Civilization:
    name: str
    founder_id: str
    generation: int = 0

    def create_being(self, world: WorldState, entity_id: str) -> Entity:
        return spawn_entity(world, entity_id=entity_id, kind="digital_being")

    def create_many(self, world: WorldState, prefix: str, count: int) -> list[Entity]:
        if count < 0:
            raise ValueError("count must be non-negative")
        return [self.create_being(world, f"{prefix}-{i}") for i in range(count)]
