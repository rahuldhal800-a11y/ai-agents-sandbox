"""Core state model for a small Earth-like digital world.

The world is intentionally deterministic and dependency-light. It is not a
visual game engine; it is the substrate in which digital beings can act,
observe, learn, and experiment.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Terrain = Literal["ocean", "plains", "forest", "mountain", "desert"]


@dataclass
class Cell:
    x: int
    y: int
    terrain: Terrain
    elevation: float
    temperature: float
    water: float
    resources: dict[str, float] = field(default_factory=dict)


@dataclass
class Entity:
    entity_id: str
    kind: str
    x: int
    y: int
    energy: float = 100.0
    age: int = 0
    inventory: dict[str, float] = field(default_factory=dict)
    memory: list[dict] = field(default_factory=list)


@dataclass
class WorldState:
    width: int
    height: int
    tick: int = 0
    cells: list[Cell] = field(default_factory=list)
    entities: dict[str, Entity] = field(default_factory=dict)

    def cell_at(self, x: int, y: int) -> Cell:
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("world coordinate outside bounds")
        return self.cells[y * self.width + x]

    def snapshot(self) -> dict:
        return {
            "tick": self.tick,
            "size": [self.width, self.height],
            "entities": {
                entity_id: {
                    "kind": entity.kind,
                    "position": [entity.x, entity.y],
                    "energy": entity.energy,
                    "age": entity.age,
                }
                for entity_id, entity in self.entities.items()
            },
        }
