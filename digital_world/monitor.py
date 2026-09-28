"""Live monitor for the Digital World using only Python standard library."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from .being import Genesis


class Monitor:
    def __init__(self, being: Genesis):
        self.being = being
        self.events: list[dict] = []

    def snapshot(self) -> dict:
        return {
            "name": self.being.name,
            "alive": self.being.alive,
            "tick": self.being.world.clock,
            "world": self.being.world.state,
            "tools": self.being.discover_tools(),
            "learning": self.being.learner.values,
            "memory_count": len(self.being.memory.recall(100000)),
            "experiences": len(self.being.learner.history),
            "mutations": self.being.mutations,
            "events": self.events[-20:],
        }

    def kill(self, reason: str) -> None:
        self.being.kill(reason)
        self.events.append({"type": "kill", "reason": reason})


def serve(being: Genesis, host: str = "127.0.0.1", port: int = 8765) -> None:
    monitor = Monitor(being)

    class Handler(BaseHTTPRequestHandler):
        def send_json(self, payload: dict, status: int = 200) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:
            if self.path == "/api/state":
                self.send_json(monitor.snapshot())
                return
            if self.path == "/":
                html = """<!doctype html><meta name=viewport content='width=device-width,initial-scale=1'>
<title>Genesis Monitor</title><style>body{font-family:system-ui;max-width:900px;margin:24px auto;padding:0 16px}pre{background:#111;color:#eee;padding:16px;border-radius:10px;overflow:auto}button{padding:12px 18px}</style>
<h1>Genesis — Digital World</h1><button onclick='kill()'>KILL SWITCH</button><pre id=x>Loading...</pre>
<script>
async function refresh(){document.querySelector('#x').textContent=JSON.stringify(await (await fetch('/api/state')).json(),null,2)}
async function kill(){await fetch('/api/kill',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({reason:'Operator emergency stop'})});refresh()}
refresh();setInterval(refresh,1000)
</script>"""
                body = html.encode()
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            self.send_error(404)

        def do_POST(self) -> None:
            if self.path != "/api/kill":
                self.send_error(404)
                return
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length) or b"{}")
            monitor.kill(str(data.get("reason", "Operator emergency stop")))
            self.send_json({"status": "killed"})

        def log_message(self, *_args) -> None:
            return

    ThreadingHTTPServer((host, port), Handler).serve_forever()
