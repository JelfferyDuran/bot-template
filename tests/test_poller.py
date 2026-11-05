import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from bot.dedupe import SeenStore
from bot.poller import Poller


class TestPoller(unittest.TestCase):
    def test_only_new_items_yielded(self):
        with tempfile.TemporaryDirectory() as d:
            seen = SeenStore(os.path.join(d, "seen.json"))
            items = [{"id": "1", "title": "a"}, {"id": "2", "title": "b"}]
            poller = Poller(lambda: items, seen)
            self.assertEqual(len(poller.poll_once()), 2)
            self.assertEqual(len(poller.poll_once()), 0)

    def test_items_without_id_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            seen = SeenStore(os.path.join(d, "seen.json"))
            poller = Poller(lambda: [{"title": "no id"}], seen)
            self.assertEqual(poller.poll_once(), [])


if __name__ == "__main__":
    unittest.main()
