"""A persistent, observable simulated world for autonomous digital beings."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class World:
    name: str = "Genesis World"
    clock: int = 0
    state: dict[str, Any] = field(default_factory=dict)
    observations: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.state:
            self.state = {
                "time": "00:00",
                "cycle": "dawn",
                "weather": "clear",
                "energy": 100,
                "entities": [
                    {"id": "genesis-core", "type": "being", "name": "Genesis", "status": "awake"},
                    {"id": "research-node", "type": "station", "name": "Research Node", "status": "idle"},
                    {"id": "lab-node", "type": "station", "name": "Experiment Lab", "status": "idle"},
                ],
                "events": [{"tick": 0, "type": "world_started", "message": "Genesis World initialized."}],
            }

    def observe(self) -> dict[str, Any]:
        observation = {"tick": self.clock, "state": self.state.copy()}
        self.observations.append(observation)
        return observation

    def step(self) -> None:
        self.clock += 1
        minute = self.clock % 1440
        hour, minute_of_hour = divmod(minute, 60)
        self.state["time"] = f"{hour:02d}:{minute_of_hour:02d}"
        self.state["cycle"] = (
            "night" if hour < 6 else
            "morning" if hour < 12 else
            "afternoon" if hour < 18 else
            "evening"
        )
        self.state["energy"] = max(0, 100 - (self.clock // 60) % 101)
        if self.clock % 10 == 0:
            events = self.state.setdefault("events", [])
            events.append({
                "tick": self.clock,
                "type": "world_tick",
                "message": f"World advanced to {self.state['time']} ({self.state['cycle']}).",
            })
            del events[:-30]

    def write(self, key: str, value: Any) -> None:
        self.state[key] = value
        events = self.state.setdefault("events", [])
        events.append({"tick": self.clock, "type": "world_write", "message": f"{key} changed."})
        del events[:-30]
