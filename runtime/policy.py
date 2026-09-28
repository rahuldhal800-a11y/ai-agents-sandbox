"""Capability policy for sandboxed agents.

This module intentionally models permissions rather than granting host-level
access. Real execution backends should enforce these decisions at the
container/VM boundary.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CapabilityPolicy:
    code_execution: bool = True
    filesystem: bool = True
    synthetic_databases: bool = True
    simulations: bool = True
    model_training: bool = True
    sub_agents: bool = True
    web_research: bool = True
    production_access: bool = False
    host_device_access: bool = False
    unrestricted_secrets: bool = False
    allowed_domains: tuple[str, ...] = field(default_factory=tuple)

    def allows(self, capability: str) -> bool:
        return bool(getattr(self, capability, False))
