import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from bot.dedupe import SeenStore


class TestSeenStore(unittest.TestCase):
    def test_first_seen_is_new_second_is_not(self):
        with tempfile.TemporaryDirectory() as d:
            store = SeenStore(os.path.join(d, "seen.json"))
            self.assertTrue(store.is_new("abc"))
            self.assertFalse(store.is_new("abc"))
            self.assertTrue(store.is_new("def"))

    def test_persists_across_restarts(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "seen.json")
            SeenStore(path).is_new("abc")
            self.assertFalse(SeenStore(path).is_new("abc"))


if __name__ == "__main__":
    unittest.main()
