"""Polling: fetch a source on an interval and yield only new items."""
from __future__ import annotations

import time
from typing import Callable, Iterable

from .dedupe import SeenStore

Item = dict


class Poller:
    """Polls a source function and yields items the dedupe store hasn't seen."""

    def __init__(self, fetch: Callable[[], Iterable[Item]], seen: SeenStore):
        self.fetch = fetch
        self.seen = seen

    def poll_once(self) -> list[Item]:
        fresh: list[Item] = []
        for item in self.fetch():
            item_id = str(item.get("id", ""))
            if item_id and self.seen.is_new(item_id):
                fresh.append(item)
        return fresh

    def run(self, interval_seconds: int, on_items: Callable[[list[Item]], None],
            stop_after: int | None = None) -> None:
        cycles = 0
        while True:
            fresh = self.poll_once()
            if fresh:
                on_items(fresh)
            cycles += 1
            if stop_after is not None and cycles >= stop_after:
                return
            time.sleep(interval_seconds)
