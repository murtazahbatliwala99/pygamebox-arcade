import tempfile
import unittest
from pathlib import Path
from core.storage import ScoreStore

class ScoreStoreTests(unittest.TestCase):
    def test_records_and_keeps_high_score(self):
        with tempfile.TemporaryDirectory() as folder:
            store = ScoreStore(Path(folder) / "scores.json")
            self.assertEqual(store.high_score("snake"), 0)
            self.assertEqual(store.record("snake", 20), 20)
            self.assertEqual(store.record("snake", 10), 20)
            reloaded = ScoreStore(Path(folder) / "scores.json")
            self.assertEqual(reloaded.high_score("snake"), 20)

if __name__ == "__main__":
    unittest.main()
