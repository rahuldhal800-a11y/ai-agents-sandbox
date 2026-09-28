"""World generator and deterministic simulation rules."""

from __future__ import annotations

import random

from .model import Cell, Entity, WorldState


def create_world(width: int = 64, height: int = 32, seed: int = 42) -> WorldState:
    """Create an Earth-like toy planet from local procedural rules."""
    rng = random.Random(seed)
    cells: list[Cell] = []

    for y in range(height):
        latitude = abs((y / max(height - 1, 1)) * 2 - 1)
        for x in range(width):
            noise = rng.random()
            elevation = noise * 2 - 1
            temperature = 30.0 * (1.0 - latitude) - abs(elevation) * 12.0

            if elevation < -0.15:
                terrain = "ocean"
                water = 1.0
            elif elevation > 0.72:
                terrain = "mountain"
                water = 0.15
            elif temperature < 7:
                terrain = "desert"
                water = 0.08
            elif noise > 0.58:
                terrain = "forest"
                water = 0.70
            else:
                terrain = "plains"
                water = 0.45

            cells.append(
                Cell(
                    x=x,
                    y=y,
                    terrain=terrain,
                    elevation=elevation,
                    temperature=temperature,
                    water=water,
                    resources={
                        "food": 0.8 if terrain in {"forest", "plains"} else 0.05,
                        "stone": 0.7 if terrain == "mountain" else 0.15,
                        "wood": 0.9 if terrain == "forest" else 0.05,
                    },
                )
            )

    return WorldState(width=width, height=height, cells=cells)


def spawn_entity(world: WorldState, entity_id: str, kind: str = "being") -> Entity:
    """Place an entity on the first usable land cell."""
    for cell in world.cells:
        if cell.terrain != "ocean":
            entity = Entity(entity_id=entity_id, kind=kind, x=cell.x, y=cell.y)
            world.entities[entity_id] = entity
            return entity
    raise RuntimeError("world contains no land")


def step(world: WorldState) -> None:
    """Advance one simulation tick using intentionally simple local rules."""
    for entity in world.entities.values():
        cell = world.cell_at(entity.x, entity.y)
        entity.age += 1
        entity.energy -= 0.5

        # The being can survive by consuming locally available food.
        if entity.energy < 70 and cell.resources.get("food", 0) > 0.05:
            consumed = min(0.20, cell.resources["food"])
            cell.resources["food"] -= consumed
            entity.inventory["food"] = entity.inventory.get("food", 0) + consumed
            entity.energy = min(100.0, entity.energy + consumed * 80)

    world.tick += 1
