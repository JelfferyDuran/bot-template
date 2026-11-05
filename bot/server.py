"""Tiny stdlib health server so the template proves it runs: GET /health."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer


def make_handler(status: dict):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            if self.path == "/health":
                body = json.dumps(status).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            else:
                self.send_response(404)
                self.end_headers()

        def log_message(self, *args):  # keep the console quiet
            pass

    return Handler


def serve(status: dict, host: str = "127.0.0.1", port: int = 8000) -> None:
    HTTPServer((host, port), make_handler(status)).serve_forever()
