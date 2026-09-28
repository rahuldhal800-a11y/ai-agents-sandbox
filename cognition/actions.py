"""Primitive actions available to a digital being inside the world."""

from __future__ import annotations

from dataclasses import dataclass

from world.model import WorldState


@dataclass(frozen=True)
class ActionResult:
    action: str
    success: bool
    reward: float
    details: dict


def move(world: WorldState, being_id: str, dx: int, dy: int) -> ActionResult:
    entity = world.entities[being_id]
    nx, ny = entity.x + dx, entity.y + dy
    if not (0 <= nx < world.width and 0 <= ny < world.height):
        return ActionResult("move", False, -0.2, {"reason": "boundary"})
    target = world.cell_at(nx, ny)
    if target.terrain == "ocean":
        return ActionResult("move", False, -0.1, {"reason": "ocean"})
    entity.x, entity.y = nx, ny
    return ActionResult("move", True, 0.3, {"position": [nx, ny]})


def gather(world: WorldState, being_id: str, resource: str) -> ActionResult:
    entity = world.entities[being_id]
    cell = world.cell_at(entity.x, entity.y)
    available = cell.resources.get(resource, 0.0)
    if available <= 0:
        return ActionResult("gather", False, -0.2, {"resource": resource})
    amount = min(1.0, available)
    cell.resources[resource] = available - amount
    entity.inventory[resource] = entity.inventory.get(resource, 0.0) + amount
    return ActionResult("gather", True, 0.5, {"resource": resource, "amount": amount})
