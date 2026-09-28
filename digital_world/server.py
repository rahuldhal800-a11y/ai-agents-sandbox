"""Production-oriented local server for the Digital World UI."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from .bootstrap import create_genesis
from .monitor import Monitor

genesis = create_genesis()
monitor = Monitor(genesis)


class Handler(BaseHTTPRequestHandler):
    def _send(self, body: bytes, content_type: str, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/api/world":
            self._send(json.dumps(monitor.snapshot()).encode(), "application/json")
            return
        if self.path == "/api/health":
            self._send(b'{"status":"ok","world":"genesis"}', "application/json")
            return
        if self.path in ("/", "/index.html"):
            body = open("web/index.html", "rb").read()
            self._send(body, "text/html; charset=utf-8")
            return
        if self.path == "/app.js":
            body = open("web/app.js", "rb").read()
            self._send(body, "text/javascript; charset=utf-8")
            return
        if self.path == "/style.css":
            body = open("web/style.css", "rb").read()
            self._send(body, "text/css; charset=utf-8")
            return
        self.send_error(404)

    def do_POST(self) -> None:
        if self.path != "/api/kill":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        monitor.kill(str(payload.get("reason", "Operator emergency stop")))
        self._send(b'{"status":"killed"}', "application/json")

    def log_message(self, *_args) -> None:
        return


def serve(host: str = "0.0.0.0", port: int = 8765) -> None:
    ThreadingHTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    serve()
