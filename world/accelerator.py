"""Accelerated simulation clock for the digital world.

Simulation time is deliberately independent from wall-clock time. A single
wall-clock step may execute many deterministic world ticks, allowing research
agents and civilizations to develop at much higher simulated speed.
"""

from __future__ import annotations

from dataclasses import dataclass

from .model import WorldState
from .sim import step


@dataclass
class SimulationClock:
    ticks_per_wall_step: int = 100
    wall_steps: int = 0
    simulated_ticks: int = 0

    def advance(self, world: WorldState, wall_steps: int = 1) -> int:
        if wall_steps < 0:
            raise ValueError("wall_steps must be non-negative")
        ticks = wall_steps * self.ticks_per_wall_step
        for _ in range(ticks):
            step(world)
        self.wall_steps += wall_steps
        self.simulated_ticks += ticks
        return ticks

    @property
    def acceleration(self) -> int:
        return self.ticks_per_wall_step
