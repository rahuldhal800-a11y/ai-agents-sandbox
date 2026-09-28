# Architecture

The sandbox is a digital laboratory composed of isolated agent runtimes, environments, tools, memory, experiments, evaluation, and governance.

```text
                    USER / CONTROL PLANE
                           |
                    Goal / Objective API
                           |
                    AUTONOMOUS ORCHESTRATOR
                           |
          +----------------+----------------+
          |                |                |
       PLANNER          MEMORY          REGISTRY
          |                |                |
          +----------------+----------------+
                           |
                    AGENT RUNTIME
                           |
        +------------------+------------------+
        |          |          |        |       |
      CODE      TOOLS      LABS     DATA   NETWORK
        |          |          |        |       |
        +----------+----------+--------+-------+
                           |
                    OBSERVE / EVALUATE
                           |
                    ERROR -> DIAGNOSE
                           |
                      FIX -> RETRY
                           |
                     LEARN / RECORD
                           |
                       NEXT RUN
```

## Labs
AI/ML, coding, research, data, simulation, automation, multi-agent systems, and authorized cybersecurity experiments.

## Agent capabilities
Agents can create files, programs, services, datasets, simulations, models, sub-agents, and experiment plans within their assigned sandbox.

## Self-improvement
Every experiment produces observations, metrics, failures, fixes, and evaluation records that become future context.
