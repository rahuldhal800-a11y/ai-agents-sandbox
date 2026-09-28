"""Evaluation primitives for autonomous experiments."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Evaluation:
    passed: bool
    score: float
    reasons: tuple[str, ...] = ()


def evaluate(observation: dict, *, minimum_score: float = 0.8) -> Evaluation:
    score = float(observation.get("score", 0.0))
    passed = score >= minimum_score
    reasons = () if passed else (f"score {score:.3f} is below {minimum_score:.3f}",)
    return Evaluation(passed=passed, score=score, reasons=reasons)
