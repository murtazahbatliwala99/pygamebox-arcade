# 🎮 PyGameBox

**A little arcade. A lot of fun.**

PyGameBox is a desktop arcade collection built with Python and Pygame. It brings four classic arcade-style games together in one launcher, with player registration, persistent high scores, and a local player leaderboard.


## 🕹️ Games

| Game | Description |
|---|---|
| Snake | Classic and Wraparound modes |
| Pong | Two-player paddle challenge |
| Space Shooter | Space combat with automatic shooting |
| Tetris | Rotate, stack and clear blocks |

## ✨ Features

- Arcade-style launcher with keyboard and mouse navigation
- Four playable games in one application
- Player registration and remembered player names
- Separate high scores for individual games
- Local player leaderboard with rankings
- Snake Classic and Wraparound have independent records
- Persistent score storage using JSON
- Reusable UI components and shared configuration

## 🛠️ Technologies Used

- Python 3
- Pygame
- JSON for local data storage
- Git and GitHub
- Visual Studio Code

## 💻 Installation

### Requirements

- Python 3.10 or newer
- Pygame 2.6.1 or newer

### Windows Setup

Clone the repository:

```bash
git clone https://github.com/murtazahbatliwala99/pygamebox-arcade.git
```

Move into the project directory:

```bash
cd pygamebox-arcade
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Launch PyGameBox:

```bash
python main.py
```

## 🎮 Controls

| Game | Controls |
|---|---|
| Main Menu | Arrow keys to select, Enter to play, L for leaderboard, Esc to quit |
| Snake | Arrow keys / WASD to move, P to pause, Esc to return |
| Pong | Player 1: W/S, Player 2: Up/Down |
| Space Shooter | A/D or Left/Right to move |
| Tetris | Left/Right to move, Up to rotate, Down to soft drop, Space to hard drop |
| Game Over | R to restart |

## 📁 Project Structure

```text
PyGameBox/
├── assets/
│   ├── fonts/
│   ├── images/
│   └── sounds/
├── core/
│   ├── config.py
│   ├── launcher.py
│   ├── leaderboard.py
│   ├── leaderboard_screen.py
│   ├── player.py
│   ├── player_screen.py
│   ├── storage.py
│   └── ui.py
├── data/
├── games/
│   ├── snake/
│   ├── pong/
│   ├── shooter/
│   └── tetris/
├── tests/
├── main.py
├── requirements.txt
├── LICENSE
└── README.md
```

## 🏆 Leaderboard

PyGameBox currently includes a **local leaderboard** that stores each player's highest score separately for:

- Snake Classic
- Snake Wraparound
- Pong
- Space Shooter
- Tetris

Scores are stored locally on the player's computer. An online global leaderboard is a planned future enhancement.

## 🧪 Running Tests

Run the project's unit tests:

```bash
python -m unittest discover -s tests -v
```

## 🚀 Future Improvements

- [ ] Online global leaderboard
- [ ] Sound effects and music controls
- [ ] Difficulty settings
- [ ] Gamepad support
- [ ] Additional arcade games
- [ ] Standalone executable release

## 👨‍💻 Developer

**Murtaza Batliwala**

Created as a personal Python game development project to explore programming, game logic, user interfaces, data persistence, and software development workflows.

GitHub: [@murtazahbatliwala99](https://github.com/murtazahbatliwala99)

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
