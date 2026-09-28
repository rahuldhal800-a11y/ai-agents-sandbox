"""Persistent developmental memory for a digital being."""

from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import Any


@dataclass
class MemoryRecord:
    tick: int
    kind: str
    content: dict[str, Any]


class Memory:
    def __init__(self, path: str | Path = "data/memory.jsonl"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def remember(self, tick: int, kind: str, content: dict[str, Any]) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(MemoryRecord(tick, kind, content))) + "\n")

    def recall(self, limit: int = 20) -> list[MemoryRecord]:
        if not self.path.exists():
            return []
        lines = self.path.read_text(encoding="utf-8").splitlines()[-limit:]
        return [MemoryRecord(**json.loads(line)) for line in lines]
