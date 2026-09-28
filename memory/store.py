"""Persistent-memory abstraction for autonomous agents."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Any

from agents.core import AgentGoal, AgentObservation


@dataclass
class MemoryRecord:
    objective: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class InMemoryStore:
    """Deterministic runtime store; production persistence can implement the same API."""

    def __init__(self) -> None:
        self._records: list[MemoryRecord] = []
        self._lock = Lock()

    def remember(self, goal: AgentGoal, observation: AgentObservation) -> None:
        with self._lock:
            self._records.append(
                MemoryRecord(goal.objective, observation.content, dict(observation.metadata))
            )

    def recall(self, objective: str, limit: int = 20) -> list[MemoryRecord]:
        with self._lock:
            matches = [r for r in self._records if r.objective == objective]
            return matches[-limit:]

    def export(self) -> list[dict[str, Any]]:
        with self._lock:
            return [asdict(record) for record in self._records]
