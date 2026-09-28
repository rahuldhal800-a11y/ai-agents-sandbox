# Agent Lifecycle

1. **Experimental** — new agent or capability is isolated and unconstrained by production concerns.
2. **Testing** — repeatable tests, failure injection, and tool validation.
3. **Evaluation** — benchmark quality, safety, reliability, cost, and resource usage.
4. **Verified** — passes defined acceptance criteria.
5. **Production Candidate** — packaged and ready for controlled deployment.
6. **Production** — only after explicit promotion authorization.

## Autonomous cycle

`goal -> plan -> build -> execute -> observe -> diagnose -> repair -> retry -> evaluate -> learn -> next experiment`

The orchestrator should continue until the objective is satisfied, the configured resource/time budget is exhausted, or a hard safety boundary is reached.
