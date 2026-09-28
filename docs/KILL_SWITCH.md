# Agent Kill Switch

Every agent has an independent operator-controlled kill switch.

- Armed: normal execution.
- Killed: new executions are refused immediately.
- Reset: explicit operator action restores execution.
- Reason: the kill reason is retained for auditability.

The switch is part of the runtime rather than the model prompt, so an agent cannot override its own killed state.

For the future process/container/microVM backend, the supervisor must also terminate active work when the switch is triggered; blocking only future tasks is insufficient for a true emergency stop.