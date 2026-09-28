"""Six specialized agents that develop the deterministic digital world.

All mutations go through explicit world primitives. No host filesystem, shell,
credentials, production systems, or arbitrary network access are exposed.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import copy


@dataclass(frozen=True)
class CouncilAgent:
    agent_id: str
    name: str
    mission: str
    priorities: tuple[str, ...]


@dataclass
class Proposal:
    agent_id: str
    action: str
    args: dict[str, Any]
    reason: str
    priority: float = 0.5


@dataclass
class CouncilResult:
    tick: int
    proposals: list[Proposal] = field(default_factory=list)
    executed: list[dict[str, Any]] = field(default_factory=list)
    rejected: list[dict[str, Any]] = field(default_factory=list)
    insights: list[str] = field(default_factory=list)


AGENTS = (
    CouncilAgent("architect", "World Architect", "Expand the world's structure without breaking foundational laws.", ("territory", "infrastructure", "planning")),
    CouncilAgent("builder", "Builder", "Turn resources into useful infrastructure and capabilities.", ("construction", "resources", "development")),
    CouncilAgent("scientist", "Scientist", "Run experiments, learn what works, and convert discoveries into improvements.", ("experiments", "learning", "optimization")),
    CouncilAgent("economist", "Economist", "Balance production, consumption and resilience.", ("resources", "energy", "efficiency")),
    CouncilAgent("society", "Society & Culture", "Develop cooperation, populations, communication and culture.", ("population", "communication", "culture")),
    CouncilAgent("guardian", "Guardian", "Protect invariants and keep autonomous growth bounded.", ("safety", "invariants", "rollback")),
)


class WorldCouncil:
    def __init__(self, world: Any, *, max_actions_per_tick: int = 12):
        self.world = world
        self.max_actions_per_tick = max(1, max_actions_per_tick)
        self.history: list[CouncilResult] = []

    def observe(self) -> dict[str, Any]:
        return self.world.snapshot()

    def _proposals(self, state: dict[str, Any]) -> list[Proposal]:
        entities = state.get("entities", {})
        population = len(entities)
        avg_energy = sum(float(e.get("energy", 0)) for e in entities.values()) / population if population else 0
        proposals: list[Proposal] = []

        if population < 2:
            proposals.append(Proposal("architect", "spawn", {"entity_id": f"citizen-{state['tick'] + 1}"}, "A civilization needs more than one independent entity.", 0.95))

        if population >= 2 and not getattr(self.world, "_council_development", None):
            proposals.append(Proposal("builder", "develop", {
                "name": "civilization-core", "cpu_cores": 2, "memory_gb": 4,
                "storage_tb": 1, "accelerator_units": 0, "data_center_nodes": 1,
            }, "Create an internal development capability for world research.", 0.80))

        proposals.append(Proposal("scientist", "event", {
            "type": "experiment", "message": "Measure survival and resource efficiency for the next cycle."
        }, "Turn observed behavior into a measurable experiment.", 0.65))

        proposals.append(Proposal("economist", "event", {
            "type": "economic_review", "message": f"Average entity energy is {avg_energy:.1f}; review resource efficiency."
        }, "Resource health should be evaluated continuously.", 0.60))

        if population >= 2:
            proposals.append(Proposal("society", "event", {
                "type": "social", "message": "Independent digital beings can form cooperative culture."
            }, "Enable social emergence without forcing behavior.", 0.55))

        proposals.append(Proposal("guardian", "audit", {}, "Audit autonomous changes.", 1.0))
        return sorted(proposals, key=lambda p: p.priority, reverse=True)

    def _allowed(self, proposal: Proposal) -> tuple[bool, str]:
        allowed = {
            "architect": {"spawn", "event"}, "builder": {"develop", "event"},
            "scientist": {"event"}, "economist": {"event"},
            "society": {"event"}, "guardian": {"audit"},
        }
        if proposal.action not in allowed.get(proposal.agent_id, set()):
            return False, "agent is not authorized for this action"
        if proposal.action == "spawn":
            entity_id = str(proposal.args.get("entity_id", ""))
            if not entity_id or len(entity_id) > 64:
                return False, "invalid entity id"
            if entity_id in self.world.entities:
                return False, "entity already exists"
        return True, ""

    def _execute(self, proposal: Proposal) -> dict[str, Any]:
        if proposal.action == "spawn":
            from .sim import spawn_entity
            entity = spawn_entity(self.world, proposal.args["entity_id"], kind="digital_being")
            return {"action": "spawn", "entity_id": entity.entity_id}

        if proposal.action == "develop":
            from .development import DevelopmentInfrastructure
            infra = DevelopmentInfrastructure()
            stack = infra.provision_for_model(
                proposal.args["name"],
                cpu_cores=int(proposal.args["cpu_cores"]),
                memory_gb=int(proposal.args["memory_gb"]),
                storage_tb=int(proposal.args["storage_tb"]),
                accelerator_units=int(proposal.args["accelerator_units"]),
                data_center_nodes=int(proposal.args["data_center_nodes"]),
            )
            self.world._council_development = stack
            return {"action": "develop", "name": proposal.args["name"], "stack": repr(stack)}

        if proposal.action == "event":
            event = {"tick": self.world.tick, **proposal.args}
            events = getattr(self.world, "events", None)
            if events is None:
                self.world.events = []
                events = self.world.events
            events.append(event)
            return {"action": "event", "event": event}

        if proposal.action == "audit":
            return {"action": "audit", "status": "checked"}

        raise ValueError(f"unsupported world action: {proposal.action}")

    def tick(self) -> CouncilResult:
        before = copy.deepcopy(self.observe())
        result = CouncilResult(tick=self.world.tick)
        for proposal in self._proposals(before)[:self.max_actions_per_tick]:
            result.proposals.append(proposal)
            ok, reason = self._allowed(proposal)
            if not ok:
                result.rejected.append({"agent": proposal.agent_id, "action": proposal.action, "reason": reason})
                continue
            try:
                result.executed.append(self._execute(proposal))
            except Exception as exc:
                result.rejected.append({"agent": proposal.agent_id, "action": proposal.action, "reason": str(exc)})
        self.world.step()
        after = self.observe()
        if len(after.get("entities", {})) > len(before.get("entities", {})):
            result.insights.append("Population increased; a new digital being now exists inside the world.")
        self.history.append(result)
        return result

    def run(self, ticks: int = 10) -> list[CouncilResult]:
        if ticks < 1 or ticks > 1000:
            raise ValueError("ticks must be between 1 and 1000")
        return [self.tick() for _ in range(ticks)]

    def report(self) -> dict[str, Any]:
        return {"agents": [a.__dict__ for a in AGENTS], "ticks": len(self.history), "last": self.history[-1].__dict__ if self.history else None}
