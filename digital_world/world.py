"""A real, stateful 2-D simulated environment for Genesis.

This is a simulation: terrain, resources, needs, movement, actions and
consequences are computed by the world engine rather than animated as decoration.
"""

from dataclasses import dataclass, field
import random
from typing import Any


@dataclass
class World:
    name: str = "Genesis World"
    width: int = 32
    height: int = 20
    seed: int = 42
    clock: int = 0
    state: dict[str, Any] = field(default_factory=dict)
    observations: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.rng = random.Random(self.seed)
        if not self.state:
            terrain = []
            resources = []
            for y in range(self.height):
                row = []
                for x in range(self.width):
                    value = self.rng.random()
                    tile = "water" if value < .10 else "forest" if value < .32 else "plain"
                    row.append(tile)
                    if tile != "water" and self.rng.random() < .13:
                        resources.append({
                            "id": f"resource-{x}-{y}",
                            "x": x, "y": y,
                            "kind": self.rng.choice(["food", "food", "water", "crystal"]),
                            "amount": self.rng.randint(1, 5),
                        })
                terrain.append(row)
            cx, cy = self.width // 2, self.height // 2
            terrain[cy][cx] = "plain"
            self.state = {
                "terrain": terrain,
                "resources": resources,
                "entities": [{
                    "id": "genesis",
                    "type": "being",
                    "name": "Genesis",
                    "x": cx, "y": cy,
                    "energy": 100,
                    "hunger": 0,
                    "thirst": 0,
                    "age": 0,
                    "inventory": {},
                    "status": "awake",
                }],
                "events": [],
            }

    @property
    def genesis(self) -> dict[str, Any]:
        return self.state["entities"][0]

    def tile(self, x: int, y: int) -> str:
        if not (0 <= x < self.width and 0 <= y < self.height):
            return "void"
        return self.state["terrain"][y][x]

    def nearby_resources(self, radius: int = 2) -> list[dict[str, Any]]:
        g = self.genesis
        return [
            r for r in self.state["resources"]
            if r["amount"] > 0 and abs(r["x"] - g["x"]) <= radius and abs(r["y"] - g["y"]) <= radius
        ]

    def move(self, dx: int, dy: int) -> tuple[bool, float, str]:
        g = self.genesis
        nx, ny = g["x"] + dx, g["y"] + dy
        if self.tile(nx, ny) in ("void", "water"):
            g["energy"] = max(0, g["energy"] - 2)
            return False, -0.4, "Movement blocked by the environment."
        g["x"], g["y"] = nx, ny
        g["energy"] = max(0, g["energy"] - 1)
        return True, 0.15, f"Moved to ({nx}, {ny})."

    def gather(self) -> tuple[bool, float, str]:
        found = self.nearby_resources(0)
        if not found:
            return False, -0.25, "Nothing useful to gather here."
        resource = found[0]
        kind = resource["kind"]
        inv = g = self.genesis["inventory"]
        inv[kind] = inv.get(kind, 0) + 1
        resource["amount"] -= 1
        self.genesis["energy"] = max(0, self.genesis["energy"] - 2)
        return True, 1.2, f"Gathered 1 {kind}."

    def consume(self, kind: str) -> tuple[bool, float, str]:
        g = self.genesis
        amount = g["inventory"].get(kind, 0)
        if amount <= 0:
            return False, -0.2, f"No {kind} available."
        g["inventory"][kind] -= 1
        if kind == "food":
            g["hunger"] = max(0, g["hunger"] - 35)
        elif kind == "water":
            g["thirst"] = max(0, g["thirst"] - 45)
        else:
            g["energy"] = min(100, g["energy"] + 20)
        return True, 1.0, f"Consumed {kind}."

    def rest(self) -> tuple[bool, float, str]:
        g = self.genesis
        g["energy"] = min(100, g["energy"] + 12)
        return True, 0.4, "Rested and recovered energy."

    def step(self) -> None:
        self.clock += 1
        g = self.genesis
        g["age"] += 1
        g["hunger"] = min(100, g["hunger"] + 1)
        g["thirst"] = min(100, g["thirst"] + 1)
        g["energy"] = max(0, g["energy"] - 0.25)
        if g["energy"] <= 0:
            g["status"] = "exhausted"
        elif g["hunger"] >= 90 or g["thirst"] >= 90:
            g["status"] = "distressed"
        else:
            g["status"] = "awake"
        if self.clock % 20 == 0:
            self.state["events"].append({
                "tick": self.clock,
                "type": "world_tick",
                "message": f"Genesis is at ({g['x']},{g['y']}); energy {g['energy']:.0f}, hunger {g['hunger']}, thirst {g['thirst']}.",
            })
            self.state["events"] = self.state["events"][-40:]

    def observe(self) -> dict[str, Any]:
        g = self.genesis
        visible = {
            "tick": self.clock,
            "position": [g["x"], g["y"]],
            "tile": self.tile(g["x"], g["y"]),
            "needs": {"energy": g["energy"], "hunger": g["hunger"], "thirst": g["thirst"]},
            "nearby_resources": self.nearby_resources(3),
        }
        self.observations.append(visible)
        return visible

    def write(self, key: str, value: Any) -> None:
        self.state[key] = value
