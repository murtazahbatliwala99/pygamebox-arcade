"""Per-game player leaderboards for PyGameBox."""

import json
from datetime import date
from pathlib import Path

LEADERBOARD_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "leaderboard.json"
)

VALID_GAMES = {
    "snake_classic",
    "snake_wrap",
    "pong",
    "shooter",
    "tetris",
}


class Leaderboard:
    """Stores each player's highest single score per game."""

    def __init__(self, path=None):
        self.path = Path(path) if path else LEADERBOARD_FILE
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.scores = self._load()

    def _load(self):
        if not self.path.exists():
            return []

        try:
            data = json.loads(
                self.path.read_text(encoding="utf-8")
            )

            # Support both the old list format and the
            # current dictionary format.
            if isinstance(data, dict):
                data = data.get("scores", [])

            if not isinstance(data, list):
                return []

            valid_scores = []

            for entry in data:
                if not isinstance(entry, dict):
                    continue

                player = entry.get("player")
                game = entry.get("game")
                score = entry.get("score")

                if (
                    isinstance(player, str)
                    and player.strip()
                    and game in VALID_GAMES
                    and isinstance(score, int)
                    and not isinstance(score, bool)
                    and score >= 0
                ):
                    valid_scores.append(entry)

            return valid_scores

        except (OSError, json.JSONDecodeError):
            return []

    def _save(self):
        data = {"scores": self.scores}

        self.path.write_text(
            json.dumps(data, indent=4),
            encoding="utf-8"
        )

    def record_score(self, player, game, score):
        """Save a score only when it beats the player's record."""

        player = str(player).strip()
        score = int(score)

        if not player:
            raise ValueError("Player name cannot be empty.")

        if game not in VALID_GAMES:
            raise ValueError("Unknown game.")

        if score < 0:
            raise ValueError("Score cannot be negative.")

        existing = next(
            (
                entry for entry in self.scores
                if (
                    entry["player"].casefold() == player.casefold()
                    and entry["game"] == game
                )
            ),
            None
        )

        if existing and score <= existing["score"]:
            return False

        if existing:
            existing["score"] = score
            existing["date"] = date.today().isoformat()
        else:
            self.scores.append({
                "player": player,
                "game": game,
                "score": score,
                "date": date.today().isoformat()
            })

        self._save()
        return True

    def get_top_scores(self, game, limit=10):
        """Return the top scores for a particular game."""

        if game not in VALID_GAMES:
            raise ValueError("Unknown game.")

        results = [
            entry.copy()
            for entry in self.scores
            if entry["game"] == game
        ]

        results.sort(
            key=lambda entry: (
                -entry["score"],
                entry["player"].casefold()
            )
        )

        return results[:max(0, int(limit))]

    def get_player_best(self, player, game):
        """Return a player's best score in a particular game."""

        if game not in VALID_GAMES:
            raise ValueError("Unknown game.")

        for entry in self.scores:
            if (
                entry["player"].casefold() == player.strip().casefold()
                and entry["game"] == game
            ):
                return entry["score"]

        return 0