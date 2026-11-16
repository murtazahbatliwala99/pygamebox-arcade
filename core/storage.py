"""Tiny JSON-backed high-score store."""
import json
from pathlib import Path

DEFAULT_PATH = Path(__file__).resolve().parent.parent / "data" / "scores.json"

class ScoreStore:
    def __init__(self, path=None):
        self.path = Path(path) if path else DEFAULT_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._scores = self._load()

    def _load(self):
        if not self.path.exists():
            return {}
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except (OSError, json.JSONDecodeError):
            return {}

    def high_score(self, game):
        return int(self._scores.get(game, 0))

    def record(self, game, score):
        score = int(score)
        best = max(score, self.high_score(game))
        self._scores[game] = best
        self.path.write_text(json.dumps(self._scores, indent=2), encoding="utf-8")
        return best
