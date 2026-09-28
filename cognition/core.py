"""Model-independent cognitive kernel for a digital being."""

from __future__ import annotations

from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Any


@dataclass
class Thought:
    kind: str
    content: str
    confidence: float = 0.5
    evidence: list[str] = field(default_factory=list)


@dataclass
class Experience:
    observation: dict[str, Any]
    action: str
    outcome: dict[str, Any]
    reward: float


@dataclass
class CognitiveKernel:
    """A small non-LLM cognitive substrate.

    It provides parallel hypothesis generation, bounded evaluation, persistent
    experiences, and adaptive strategy scores. A language model may be attached
    later, but is not required for the kernel to operate.
    """

    memory: list[Experience] = field(default_factory=list)
    strategy_scores: dict[str, float] = field(default_factory=dict)
    cycle: int = 0

    def observe(self, world_snapshot: dict[str, Any]) -> dict[str, Any]:
        return dict(world_snapshot)

    def generate_thoughts(
        self,
        observation: dict[str, Any],
        generators: list[Callable[[dict[str, Any]], Thought]],
    ) -> list[Thought]:
        if not generators:
            return [Thought("baseline", "inspect current state")]
        with ThreadPoolExecutor(max_workers=len(generators)) as pool:
            futures = [pool.submit(generator, observation) for generator in generators]
            return [future.result() for future in futures]

    def choose(self, thoughts: list[Thought]) -> Thought:
        if not thoughts:
            raise ValueError("no candidate thoughts")
        return max(
            thoughts,
            key=lambda thought: thought.confidence
            + self.strategy_scores.get(thought.kind, 0.0),
        )

    def learn(self, experience: Experience) -> None:
        self.memory.append(experience)
        self.strategy_scores[experience.action] = (
            self.strategy_scores.get(experience.action, 0.0) * 0.9
            + experience.reward * 0.1
        )
        self.cycle += 1

    def snapshot(self) -> dict[str, Any]:
        return {
            "cycle": self.cycle,
            "memory_size": len(self.memory),
            "strategies": dict(self.strategy_scores),
        }
