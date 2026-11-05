"""Dedupe: remember which item ids have already been seen.

Backed by a small JSON file so a restart doesn't re-alert on old items.
"""
from __future__ import annotations

import json
import os


class SeenStore:
    """A persistent set of seen item ids."""

    def __init__(self, path: str = "seen.json"):
        self.path = path
        self._seen: set[str] = set()
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.path):
            with open(self.path, encoding="utf-8") as f:
                self._seen = set(json.load(f))

    def _save(self) -> None:
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(sorted(self._seen), f)
        os.replace(tmp, self.path)

    def is_new(self, item_id: str) -> bool:
        """Return True the first time an id is seen, False afterwards."""
        if item_id in self._seen:
            return False
        self._seen.add(item_id)
        self._save()
        return True

    def __len__(self) -> int:
        return len(self._seen)
