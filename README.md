# PyGameBox 🎮

A lightweight desktop arcade collection made with **Python 3** and **Pygame**. It includes a launcher and four playable games: Snake, Pong, Space Shooter, and Tetris.

## Features

- Arcade-style launcher with keyboard and mouse navigation
- Four self-contained games
- Persistent high scores in a local JSON file
- Shared drawing helpers, colors, and game configuration
- No external assets required
- Small automated tests for score storage

## Requirements

- Python 3.10 or newer (tested with Python 3.13)
- Pygame 2.6.1 or newer

## Run on Windows 11

Open this folder in VS Code. In the integrated terminal, run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

If PowerShell blocks activation, you can avoid activation and install/run through the environment directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

If you already created a virtual environment and installed Pygame, simply run:

```powershell
python main.py
```

## Controls

| Game | Controls |
|---|---|
| Launcher | Mouse click or ↑ / ↓, Enter; Esc quits |
| Snake | Choose Classic (walls end the run) or Wraparound (edges connect); arrow keys/WASD move; P pauses; Esc returns |
| Pong | Player 1: W/S; Player 2: Up/Down arrows; first to 5 points wins; Esc returns |
| Space Shooter | A/D or Left/Right to move; shooting is automatic; Esc returns |
| Tetris | Left/Right move, Up rotate, Down soft drop, Space hard drop; Esc returns |
| All games | R restarts after game over |

## Project structure

```text
PyGameBox/
├── assets/                 # Optional images, sounds and fonts
├── core/
│   ├── config.py           # Window settings and color palette
│   ├── launcher.py         # Main menu and game loop
│   ├── storage.py          # JSON high-score persistence
│   └── ui.py               # Shared drawing helpers
├── games/
│   ├── snake/game.py
│   ├── pong/game.py
│   ├── shooter/game.py
│   └── tetris/game.py
├── tests/
│   └── test_storage.py
├── data/                   # Created automatically for local scores
├── main.py
├── requirements.txt
└── LICENSE
```

## Run tests

```powershell
python -m unittest discover -s tests -v
```

## Notes

- Scores are stored locally in `data/scores.json`; this file is intentionally ignored by Git.
- This is an initial open-source release. Contributions, bug reports, and feature suggestions are welcome.
- The project is provided under the MIT License.

## Roadmap

- [ ] Add sound effects and music controls
- [ ] Add difficulty settings
- [ ] Add gamepad support
- [ ] Add more arcade games
- [ ] Add screenshots and release builds


## High scores

High scores are stored separately for each game in `data/scores.json`.
Snake has independent records for `snake_classic` and `snake_wrap`, so the
two modes never overwrite each other's best score. Pong records the winning
score for each match; the other games record the highest run score.
