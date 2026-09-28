# Live Digital World Monitoring

Run the prototype locally with:

python run_genesis.py

Then open http://127.0.0.1:8765

The dashboard refreshes every second and shows world state, tools, learning
values, memory count, and recent operator events. It also provides the
per-being kill switch.

For phone access, Genesis must run on a reachable machine/server or through a
private network/tunnel. Do not expose the monitor directly to the public
internet without authentication.

The monitor uses only the Python standard library; no AI provider or paid API
is required.
