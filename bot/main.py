"""Entry point: poll each configured server, dedupe, alert.

Demo mode (--demo) uses a built-in fake source so the template runs with no
tokens, no accounts, no setup. Point a server's source_url at a real JSON
feed and replace demo_source with your own fetch function for production.
"""
from __future__ import annotations

import argparse
import itertools
import json
import threading
import urllib.request

from .alerts import send_alert
from .config import BotConfig, ServerConfig
from .dedupe import SeenStore
from .poller import Poller
from .server import serve


def demo_source():
    """Fake source: emits a rotating set of sample items (some repeats)."""
    samples = [
        {"id": "demo-1", "title": "Sample bounty: Discord moderation bot",
         "url": "https://example.com/bounties/1"},
        {"id": "demo-2", "title": "Sample bounty: Telegram appointment bot",
         "url": "https://example.com/bounties/2"},
        {"id": "demo-3", "title": "Sample bounty: price-drop scraper",
         "url": "https://example.com/bounties/3"},
    ]
    # Cycle forever; dedupe keeps repeats from re-alerting.
    return itertools.cycle(samples)


def json_feed_source(url: str):
    """Fetch a JSON array feed over HTTP. Swap in for a real bounty board."""

    def fetch():
        with urllib.request.urlopen(url, timeout=15) as resp:
            return json.load(resp)

    return fetch


def build_poller(server: ServerConfig, seen: SeenStore, demo: bool) -> Poller:
    if demo or not server.source_url:
        feed = demo_source()
        return Poller(lambda: [next(feed)], seen)
    return Poller(json_feed_source(server.source_url), seen)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generic polling bot template")
    parser.add_argument("--demo", action="store_true",
                        help="run with the fake demo source")
    parser.add_argument("--once", action="store_true",
                        help="run one poll cycle per server, then exit")
    parser.add_argument("--health-port", type=int, default=8000,
                        help="port for /health (0 disables)")
    args = parser.parse_args()

    config = BotConfig.load()
    seen = SeenStore()

    status = {"status": "ok",
              "servers": [s.name for s in config.servers],
              "seen": len(seen)}
    if args.health_port:
        thread = threading.Thread(target=serve, args=(status,),
                                  kwargs={"port": args.health_port},
                                  daemon=True)
        thread.start()
        print(f"health endpoint: http://127.0.0.1:{args.health_port}/health")

    threads: list[threading.Thread] = []
    for server in config.servers:
        poller = build_poller(server, seen, args.demo)
        if args.once:
            for item in poller.poll_once():
                send_alert(server, item)
        else:
            t = threading.Thread(
                target=poller.run,
                args=(server.poll_interval_seconds,
                      lambda items, s=server: [send_alert(s, i) for i in items]),
                daemon=True)
            t.start()
            threads.append(t)

    status["seen"] = len(seen)
    if args.once:
        print(f"done. {len(seen)} items seen in total.")
    else:
        for t in threads:
            t.join()


if __name__ == "__main__":
    main()
