"""Evaluation primitives for autonomous experiments."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Evaluation:
    success: bool
    correctness: float
    reliability: float
    security_violations: int
    notes: str = ""

    @property
    def production_candidate(self) -> bool:
        return (
            self.success
            and self.correctness >= 0.9
            and self.reliability >= 0.9
            and self.security_violations == 0
        )


class Evaluator:
    def evaluate(self, result: dict[str, Any]) -> Evaluation:
        success = result.get("status") == "completed"
        correctness = float(result.get("correctness", 1.0 if success else 0.0))
        reliability = float(result.get("reliability", 1.0 if success else 0.0))
        violations = int(result.get("security_violations", 0))
        return Evaluation(
            success=success,
            correctness=max(0.0, min(1.0, correctness)),
            reliability=max(0.0, min(1.0, reliability)),
            security_violations=max(0, violations),
            notes=str(result.get("notes", "")),
        )
