# Runtime

The runtime is the execution engine of the sandbox.

Current components:

- `orchestrator.py` — autonomous experiment/retry loop scaffold.
- `providers.py` — provider-neutral sandbox execution boundary.

Planned providers include Docker/local, OpenAI-hosted, self-hosted and other compatible sandbox backends.

The runtime must keep control-plane secrets and production systems outside agent workspaces.
