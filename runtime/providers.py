"""Provider-neutral sandbox execution boundary.

Concrete providers can implement this protocol for Docker, OpenAI-hosted,
self-hosted, or other sandbox backends without changing agent logic.
"""

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class SandboxSession:
    session_id: str
    provider: str
    workspace: str
    metadata: dict = field(default_factory=dict)


class SandboxProvider(Protocol):
    name: str

    def create(self, workspace: str) -> SandboxSession: ...
    def execute(self, session: SandboxSession, command: str) -> str: ...
    def destroy(self, session: SandboxSession) -> None: ...


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, SandboxProvider] = {}

    def register(self, provider: SandboxProvider) -> None:
        self._providers[provider.name] = provider

    def get(self, name: str) -> SandboxProvider:
        try:
            return self._providers[name]
        except KeyError as exc:
            raise ValueError(f"Unknown sandbox provider: {name}") from exc

    def names(self) -> list[str]:
        return sorted(self._providers)
