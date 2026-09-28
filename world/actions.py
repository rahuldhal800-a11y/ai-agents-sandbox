"""Actions available to a digital being inside the world."""

from __future__ import annotations

from dataclasses import dataclass

from .model import Entity, WorldState


@dataclass(frozen=True)
class Observation:
    tick: int
    entity_id: str
    position: tuple[int, int]
    terrain: str
    temperature: float
    water: float
    resources: dict[str, float]
    energy: float


def observe(world: WorldState, entity_id: str) -> Observation:
    entity = world.entities[entity_id]
    cell = world.cell_at(entity.x, entity.y)
    return Observation(
        tick=world.tick,
        entity_id=entity_id,
        position=(entity.x, entity.y),
        terrain=cell.terrain,
        temperature=cell.temperature,
        water=cell.water,
        resources=dict(cell.resources),
        energy=entity.energy,
    )


def move(world: WorldState, entity_id: str, dx: int, dy: int) -> Observation:
    """Move one cell. Invalid/ocean moves are rejected without mutating state."""
    entity: Entity = world.entities[entity_id]
    nx, ny = entity.x + max(-1, min(1, dx)), entity.y + max(-1, min(1, dy))
    if not (0 <= nx < world.width and 0 <= ny < world.height):
        raise ValueError("move would leave world bounds")
    destination = world.cell_at(nx, ny)
    if destination.terrain == "ocean":
        raise ValueError("cannot move into ocean")
    entity.x, entity.y = nx, ny
    entity.energy -= 1.0
    return observe(world, entity_id)


def remember(world: WorldState, entity_id: str, observation: Observation) -> None:
    world.entities[entity_id].memory.append(
        {
            "tick": observation.tick,
            "position": observation.position,
            "terrain": observation.terrain,
            "resources": observation.resources,
        }
    )
