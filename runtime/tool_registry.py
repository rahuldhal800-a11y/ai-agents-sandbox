"""Scoped tool registry and execution boundary for sandbox agents."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from agents.core import AgentAction, AgentObservation


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    capability: str
    handler: Callable[[dict[str, Any]], AgentObservation]


@dataclass
class ToolRegistry:
    allowed_capabilities: set[str] = field(default_factory=set)
    _tools: dict[str, ToolDefinition] = field(default_factory=dict)
    audit_log: list[dict[str, Any]] = field(default_factory=list)

    def register(self, tool: ToolDefinition) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def describe(self) -> list[dict[str, str]]:
        return [
            {"name": t.name, "description": t.description, "capability": t.capability}
            for t in self._tools.values()
        ]

    def execute(self, action: AgentAction) -> AgentObservation:
        tool = self._tools.get(action.tool)
        if tool is None:
            raise ValueError(f"Unknown tool: {action.tool}")
        if tool.capability not in self.allowed_capabilities:
            self.audit_log.append({"tool": action.tool, "allowed": False, "capability": tool.capability})
            raise PermissionError(f"Capability not granted: {tool.capability}")

        self.audit_log.append({"tool": action.tool, "allowed": True, "capability": tool.capability})
        return tool.handler(action.arguments)
