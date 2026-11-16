
"""Main PyGameBox launcher."""

import pygame

from .player import PlayerManager
from .player_screen import register_player
from .leaderboard import Leaderboard
from .leaderboard_screen import run_leaderboard
from . import config as C
from .ui import background, text, panel
from .storage import ScoreStore

from games.snake.game import run as run_snake
from games.pong.game import run as run_pong
from games.shooter.game import run as run_shooter
from games.tetris.game import run as run_tetris


GAMES = [
    (
        "SNAKE",
        "Two modes: classic and wraparound.",
        C.GREEN,
        run_snake,
        "snake_classic"
    ),
    (
        "PONG",
        "A two-player paddle challenge.",
        C.CYAN,
        run_pong,
        "pong"
    ),
    (
        "SPACE SHOOTER",
        "Move your ship. Auto-fire does the rest.",
        C.PINK,
        run_shooter,
        "shooter"
    ),
    (
        "TETRIS",
        "Rotate, stack, and clear lines.",
        C.YELLOW,
        run_tetris,
        "tetris"
    ),
]


class PlayerScoreStore:
    """Connect existing game scores to player leaderboards."""

    def __init__(self, score_store, leaderboard, player_name):
        self.score_store = score_store
        self.leaderboard = leaderboard
        self.player_name = player_name

    def high_score(self, game):
        return self.score_store.high_score(game)

    def record(self, game, score):
        best = self.score_store.record(game, score)

        self.leaderboard.record_score(
            self.player_name,
            game,
            score
        )

        return best


def main():
    pygame.init()

    pygame.display.set_caption(C.TITLE)

    screen = pygame.display.set_mode(
        (C.WIDTH, C.HEIGHT)
    )

    clock = pygame.time.Clock()

    original_store = ScoreStore()
    player_manager = PlayerManager()

    player_name = player_manager.get_player()

    if not player_name:
        player_name = register_player(
            screen,
            clock,
            player_manager
        )

        if player_name is None:
            pygame.quit()
            return

    leaderboard = Leaderboard()

    store = PlayerScoreStore(
        original_store,
        leaderboard,
        player_name
    )

    selected = 0
    running = True

    title_font = pygame.font.SysFont(
        "segoeui",
        70,
        bold=True
    )

    leaderboard_button = pygame.Rect(
        C.WIDTH // 2 - 125,
        478,
        250,
        42
    )

    while running:
        mouse = pygame.mouse.get_pos()

        cards = [
            pygame.Rect(75 + i * 225, 245, 205, 220)
            for i in range(4)
        ]

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_l:
                    result = run_leaderboard(
                        screen,
                        clock,
                        leaderboard,
                        player_name
                    )

                    if result == "quit":
                        running = False

                elif event.key in (
                    pygame.K_DOWN,
                    pygame.K_RIGHT
                ):
                    selected = (selected + 1) % 4

                elif event.key in (
                    pygame.K_UP,
                    pygame.K_LEFT
                ):
                    selected = (selected - 1) % 4

                elif event.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE
                ):
                    GAMES[selected][3](
                        screen,
                        clock,
                        store
                    )

            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):

                if leaderboard_button.collidepoint(event.pos):
                    result = run_leaderboard(
                        screen,
                        clock,
                        leaderboard,
                        player_name
                    )

                    if result == "quit":
                        running = False

                else:
                    for i, rect in enumerate(cards):

                        if rect.collidepoint(event.pos):
                            selected = i

                            GAMES[i][3](
                                screen,
                                clock,
                                store
                            )

        if not running:
            break

        background(screen)

        # Main title
        screen.blit(
            title_font.render(
                "GAMEBOX",
                True,
                C.WHITE
            ),
            (76, 82)
        )

        text(
            screen,
            "A LITTLE ARCADE. A LOT OF FUN.",
            80,
            164,
            21,
            C.MUTED
        )

        # Remembered player name
        text(
            screen,
            f"PLAYER: {player_name}",
            820,
            164,
            18,
            C.GREEN,
            center=True,
            bold=True
        )

        text(
            screen,
            "SELECT A GAME",
            80,
            211,
            19,
            C.CYAN,
            bold=True
        )

        # Game cards
        for i, (
            name,
            description,
            accent,
            _,
            key
        ) in enumerate(GAMES):

            rect = cards[i]

            active = (
                i == selected
                or rect.collidepoint(mouse)
            )

            panel(
                screen,
                rect,
                (35, 47, 72) if active else C.PANEL,
                18,
                accent if active else None
            )

            pygame.draw.circle(
                screen,
                accent,
                (rect.centerx, rect.y + 58),
                29
            )

            text(
                screen,
                str(i + 1),
                rect.centerx,
                rect.y + 58,
                28,
                C.BG,
                center=True,
                bold=True
            )

            text(
                screen,
                name,
                rect.centerx,
                rect.y + 112,
                24,
                C.WHITE,
                center=True,
                bold=True
            )

            words = description.split()
            lines = []
            current = ""

            for word in words:
                if len(current) + len(word) + 1 > 24:
                    lines.append(current.strip())
                    current = ""

                current += word + " "

            if current:
                lines.append(current.strip())

            for line_no, line in enumerate(lines[:2]):
                text(
                    screen,
                    line,
                    rect.centerx,
                    rect.y + 151 + line_no * 22,
                    16,
                    C.MUTED,
                    center=True
                )

            if key == "snake_classic":

                best_label = (
                    f"CLASSIC {store.high_score('snake_classic')}"
                    f"  •  WRAP {store.high_score('snake_wrap')}"
                )

                text(
                    screen,
                    best_label,
                    rect.centerx,
                    rect.y + 198,
                    13,
                    accent,
                    center=True,
                    bold=True
                )

            else:

                text(
                    screen,
                    f"BEST  {store.high_score(key)}",
                    rect.centerx,
                    rect.y + 198,
                    16,
                    accent,
                    center=True,
                    bold=True
                )

        # Leaderboard button
        button_hover = leaderboard_button.collidepoint(mouse)

        pygame.draw.rect(
            screen,
            (35, 65, 83) if button_hover else C.PANEL,
            leaderboard_button,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            C.CYAN,
            leaderboard_button,
            width=2,
            border_radius=12
        )

        text(
            screen,
            "LEADERBOARD",
            leaderboard_button.centerx,
            leaderboard_button.centery,
            17,
            C.CYAN,
            center=True,
            bold=True
        )

        text(
            screen,
            "ARROWS SELECT    ENTER PLAY    L LEADERBOARD    ESC QUIT",
            C.WIDTH // 2,
            550,
            15,
            C.MUTED,
            center=True
        )

        pygame.display.flip()
        clock.tick(C.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
