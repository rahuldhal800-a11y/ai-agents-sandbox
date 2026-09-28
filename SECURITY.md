# Security Boundary

The sandbox is intentionally powerful inside its isolated world and conservative at the boundary.

### Allowed inside sandbox
- Synthetic data and test databases
- Disposable workspaces and containers
- Simulations and model training
- Authorized security labs and synthetic targets
- Mock APIs, internal DNS, virtual services, and agent-to-agent networks

### Restricted outside sandbox
- Production databases and CRM
- Real customer or credential data
- Personal-device control
- Live WhatsApp/Meta/payment credentials
- Unscoped master API keys
- Production deployment without explicit promotion

Secrets must be injected through a scoped secret gateway and must never be committed to Git.
