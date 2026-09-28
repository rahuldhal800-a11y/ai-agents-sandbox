# OpenAI Sandbox Integration

## Purpose

The sandbox architecture follows the current OpenAI Agents model while keeping the project provider-neutral.

## Control plane vs execution plane

- **Control plane:** agent definitions, orchestration, model calls, handoffs, approvals, tracing, state, policy and audit.
- **Execution plane:** isolated sandbox sessions where agents can inspect and modify files, execute commands, install dependencies, expose ports, run experiments and persist/snapshot workspace state.

The control plane must never expose production credentials directly to agent-generated code.

## Provider strategy

The runtime uses a provider adapter so the same agent can run against:

1. Docker/local sandbox for development.
2. OpenAI-hosted sandbox when managed compute is useful.
3. Self-hosted environments when trusted/private compute is required.
4. Other supported sandbox providers through adapters.

Provider selection belongs to the run/session configuration, not to the agent's core definition.

## OpenAI capabilities to map into this project

- Shell / command execution
- Filesystem editing and inspection
- Skills and reusable instructions
- Memory artifacts
- Long-running/resumable sessions
- Snapshots and workspace state
- Ports/service previews
- Controlled external network access
- Multi-agent handoffs and nested sandbox agents

## Autonomous experiment loop

`Goal -> Plan -> Provision workspace -> Execute -> Observe -> Evaluate -> Diagnose -> Repair -> Re-run -> Record -> Spawn next experiment`

The loop may iterate without human interaction inside the sandbox. Production promotion remains a separate approval boundary.

## Credential boundary

OpenAI's application key, production database credentials, WhatsApp/Meta credentials, payment credentials and other master secrets remain outside sandbox workspaces. A scoped secret broker may issue short-lived, least-privilege credentials where required.

## References

- OpenAI Sandbox Agents: https://developers.openai.com/api/docs/guides/agents/sandboxes
- OpenAI Agents API: https://developers.openai.com/api/docs/guides/agents
- OpenAI-hosted sandboxes: https://developers.openai.com/api/docs/guides/agents-api/environments/openai-hosted
- OpenAI sandbox security: https://developers.openai.com/api/docs/guides/agents-api/environments/security
