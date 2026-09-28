"""Controlled creation and lifecycle management of sandbox sub-agents."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from agents.core import AutonomousAgent, IntelligenceProvider, MemoryStore
from runtime.tool_registry import ToolRegistry


@dataclass(frozen=True)
class AgentSpec:
    name: str
    role: str
    capabilities: frozenset[str] = frozenset()


class AgentSpawner:
    def __init__(
        self,
        intelligence_factory: Callable[[AgentSpec], IntelligenceProvider],
        memory_factory: Callable[[AgentSpec], MemoryStore],
    ) -> None:
        self._intelligence_factory = intelligence_factory
        self._memory_factory = memory_factory
        self._agents: dict[str, AutonomousAgent] = {}

    def spawn(self, spec: AgentSpec, tools: ToolRegistry) -> AutonomousAgent:
        if spec.name in self._agents:
            raise ValueError(f"Agent already exists: {spec.name}")
        tools.allowed_capabilities = set(spec.capabilities)
        agent = AutonomousAgent(
            name=spec.name,
            intelligence=self._intelligence_factory(spec),
            tools=tools,
            memory=self._memory_factory(spec),
        )
        self._agents[spec.name] = agent
        return agent

    def get(self, name: str) -> AutonomousAgent:
        return self._agents[name]

    def list_agents(self) -> list[str]:
        return sorted(self._agents)
