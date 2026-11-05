"""Alert sinks: console + webhook. Add your own sink by matching send_alert."""
from __future__ import annotations

import json
import urllib.request

from .config import ServerConfig


def send_console(server: ServerConfig, item: dict) -> None:
    print(f"[{server.name}] NEW: {item.get('title', item.get('id'))} — {item.get('url', '')}")


def send_webhook(server: ServerConfig, item: dict) -> None:
    if not server.alert_webhook_url:
        return
    payload = json.dumps({"server": server.name, "item": item}).encode("utf-8")
    req = urllib.request.Request(
        server.alert_webhook_url, data=payload,
        headers={"Content-Type": "application/json"}, method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        resp.read()


def send_alert(server: ServerConfig, item: dict) -> None:
    send_console(server, item)
    if server.alert_webhook_url:
        send_webhook(server, item)
