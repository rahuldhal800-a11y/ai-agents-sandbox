"""Web server for the Digital World and Genesis interaction surface."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import threading
import time

from .bootstrap import create_genesis
from .monitor import Monitor

ROOT = Path(__file__).resolve().parent.parent
genesis = create_genesis()
monitor = Monitor(genesis)


def autonomous_loop() -> None:
    while genesis.alive:
        genesis.autonomous_step()
        time.sleep(0.35)




class Handler(BaseHTTPRequestHandler):
    def _send(self, body: bytes, content_type: str, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json_body(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        try:
            return json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            return {}

    def do_GET(self) -> None:
        if self.path == "/api/world":
            self._send(json.dumps(monitor.snapshot()).encode(), "application/json")
            return
        if self.path == "/api/health":
            self._send(b'{"status":"ok","world":"genesis"}', "application/json")
            return
        files = {
            "/": ("web/index.html", "text/html; charset=utf-8"),
            "/index.html": ("web/index.html", "text/html; charset=utf-8"),
            "/app.js": ("web/app.js", "text/javascript; charset=utf-8"),
            "/style.css": ("web/style.css", "text/css; charset=utf-8"),
            "/world3d.js": ("web/world3d.js", "text/javascript; charset=utf-8"),
            "/world2d.js": ("web/world2d.js", "text/javascript; charset=utf-8"),
        }
        if self.path in files:
            filename, content_type = files[self.path]
            body = (ROOT / filename).read_bytes()
            self._send(body, content_type)
            return
        self.send_error(404)

    def do_POST(self) -> None:
        if self.path == "/api/kill":
            payload = self._json_body()
            monitor.kill(str(payload.get("reason", "Operator emergency stop")))
            self._send(b'{"status":"killed"}', "application/json")
            return
        if self.path == "/api/talk":
            payload = self._json_body()
            message = str(payload.get("message", "")).strip()
            if not message:
                self._send(b'{"error":"message is required"}', "application/json", 400)
                return
            reply = genesis.talk(message)
            self._send(json.dumps({"reply": reply}).encode(), "application/json")
            return
        self.send_error(404)

    def log_message(self, *_args) -> None:
        return


def serve(host: str = "0.0.0.0", port: int = 8765) -> None:
    ThreadingHTTPServer((host, port), Handler).serve_forever()


def start_autonomy() -> None:
    threading.Thread(target=autonomous_loop, daemon=True, name="genesis-autonomy").start()


if __name__ == "__main__":
    start_autonomy()
    serve()
