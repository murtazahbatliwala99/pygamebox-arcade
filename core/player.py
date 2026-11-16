
"""Player identity management for PyGameBox."""

import json
from pathlib import Path

PLAYER_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "player.json"
)


class PlayerManager:
    """Stores and retrieves the current player's name."""

    def __init__(self, path=None):
        self.path = Path(path) if path else PLAYER_FILE
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def get_player(self):
        """Return the saved player name, or None if not configured."""
        if not self.path.exists():
            return None

        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            name = data.get("name")

            if isinstance(name, str) and name.strip():
                return name.strip()

        except (OSError, json.JSONDecodeError, AttributeError):
            return None

        return None

    def save_player(self, name):
        """Save a player's name."""
        name = name.strip()

        if not name:
            raise ValueError("Player name cannot be empty.")

        if len(name) > 20:
            raise ValueError("Player name must be 20 characters or fewer.")

        data = {"name": name}
        self.path.write_text(
            json.dumps(data, indent=4),
            encoding="utf-8"
        )

        return name
