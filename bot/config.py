"""Multi-server configuration.

Config comes from a JSON file (default: config/servers.json) or the
SERVERS_JSON environment variable. Copy config/servers.example.json to
config/servers.json and fill in your own servers — never commit real tokens.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field


@dataclass
class ServerConfig:
    """One server (Discord guild, Telegram group, etc.) the bot watches."""

    name: str
    source_url: str
    poll_interval_seconds: int = 60
    alert_webhook_url: str = ""
    channel: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "ServerConfig":
        return cls(
            name=data["name"],
            source_url=data.get("source_url", ""),
            poll_interval_seconds=int(data.get("poll_interval_seconds", 60)),
            alert_webhook_url=os.path.expandvars(data.get("alert_webhook_url", "")),
            channel=data.get("channel", ""),
        )


@dataclass
class BotConfig:
    servers: list[ServerConfig] = field(default_factory=list)

    @classmethod
    def load(cls, path: str | None = None) -> "BotConfig":
        raw = os.environ.get("SERVERS_JSON")
        if raw:
            data = json.loads(raw)
        else:
            base = os.path.join(os.path.dirname(__file__), "..", "config")
            path = path or os.path.join(base, "servers.json")
            if not os.path.exists(path):
                path = os.path.join(base, "servers.example.json")
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        return cls(servers=[ServerConfig.from_dict(s) for s in data.get("servers", [])])
