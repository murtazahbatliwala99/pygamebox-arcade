
"""In-game leaderboard screen for PyGameBox."""

import pygame

GAMES = [
    ("SNAKE CLASSIC", "snake_classic"),
    ("SNAKE WRAP", "snake_wrap"),
    ("PONG", "pong"),
    ("SPACE SHOOTER", "shooter"),
    ("TETRIS", "tetris"),
]

BG = (13, 17, 30)
PANEL = (25, 34, 55)
WHITE = (240, 244, 255)
MUTED = (125, 139, 165)
CYAN = (55, 215, 230)
GREEN = (75, 225, 155)
GOLD = (255, 205, 95)


def draw_text(surface, value, x, y, size, color,
              center=False, bold=False):
    font = pygame.font.SysFont(
        "segoeui", size, bold=bold
    )
    rendered = font.render(str(value), True, color)
    rect = rendered.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    surface.blit(rendered, rect)


def run_leaderboard(screen, clock, leaderboard, player_name):
    """Display separate Top 10 rankings for every game."""

    selected = 0
    running = True

    width, height = screen.get_size()

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return "back"

                elif event.key in (
                    pygame.K_RIGHT,
                    pygame.K_DOWN
                ):
                    selected = (selected + 1) % len(GAMES)

                elif event.key in (
                    pygame.K_LEFT,
                    pygame.K_UP
                ):
                    selected = (selected - 1) % len(GAMES)

        screen.fill(BG)

        # Header
        draw_text(
            screen,
            "WORLD RANKINGS",
            width // 2,
            65,
            38,
            WHITE,
            center=True,
            bold=True
        )

        draw_text(
            screen,
            f"PLAYER: {player_name}",
            width // 2,
            110,
            17,
            GREEN,
            center=True,
            bold=True
        )

        # Game category tabs
        tab_width = min(190, (width - 60) // len(GAMES))
        total_width = tab_width * len(GAMES)
        start_x = (width - total_width) // 2

        for i, (label, game_key) in enumerate(GAMES):
            rect = pygame.Rect(
                start_x + i * tab_width + 3,
                155,
                tab_width - 6,
                48
            )

            active = i == selected

            pygame.draw.rect(
                screen,
                PANEL if not active else (38, 67, 83),
                rect,
                border_radius=10
            )

            pygame.draw.rect(
                screen,
                CYAN if active else PANEL,
                rect,
                width=2 if active else 0,
                border_radius=10
            )

            draw_text(
                screen,
                label,
                rect.centerx,
                rect.centery,
                14,
                CYAN if active else MUTED,
                center=True,
                bold=True
            )

        # Leaderboard panel
        panel_rect = pygame.Rect(
            width * 0.13,
            225,
            width * 0.74,
            height - 310
        )

        pygame.draw.rect(
            screen,
            PANEL,
            panel_rect,
            border_radius=16
        )

        game_key = GAMES[selected][1]
        results = leaderboard.get_top_scores(
            game_key,
            limit=10
        )

        draw_text(
            screen,
            GAMES[selected][0],
            width // 2,
            255,
            22,
            CYAN,
            center=True,
            bold=True
        )

        # Column headings
        left = panel_rect.x + 35
        right = panel_rect.right - 35

        draw_text(
            screen,
            "RANK",
            left,
            295,
            14,
            MUTED,
            bold=True
        )

        draw_text(
            screen,
            "PLAYER",
            left + 120,
            295,
            14,
            MUTED,
            bold=True
        )

        draw_text(
            screen,
            "BEST SCORE",
            right - 130,
            295,
            14,
            MUTED,
            bold=True
        )

        pygame.draw.line(
            screen,
            (55, 70, 95),
            (left, 320),
            (right, 320),
            2
        )

        # Ranking entries
        if not results:

            draw_text(
                screen,
                "NO SCORES YET",
                width // 2,
                height // 2,
                24,
                MUTED,
                center=True,
                bold=True
            )

            draw_text(
                screen,
                "Play this game to claim the first position!",
                width // 2,
                height // 2 + 40,
                15,
                MUTED,
                center=True
            )

        else:

            row_height = min(
                43,
                max(28, (height - 400) // 10)
            )

            for rank, entry in enumerate(results, start=1):

                y = 335 + (rank - 1) * row_height

                if y + row_height > panel_rect.bottom - 10:
                    break

                is_current = (
                    entry["player"].casefold()
                    == player_name.casefold()
                )

                color = (
                    GREEN if is_current
                    else WHITE
                )

                if rank == 1:
                    rank_color = GOLD
                elif rank == 2:
                    rank_color = (190, 205, 225)
                elif rank == 3:
                    rank_color = (210, 150, 110)
                else:
                    rank_color = MUTED

                if is_current:
                    highlight = pygame.Rect(
                        left - 10,
                        y - 3,
                        right - left + 20,
                        row_height - 2
                    )

                    pygame.draw.rect(
                        screen,
                        (35, 65, 65),
                        highlight,
                        border_radius=7
                    )

                draw_text(
                    screen,
                    f"#{rank}",
                    left,
                    y,
                    17,
                    rank_color,
                    bold=True
                )

                draw_text(
                    screen,
                    entry["player"],
                    left + 120,
                    y,
                    17,
                    color,
                    bold=is_current
                )

                draw_text(
                    screen,
                    entry["score"],
                    right - 130,
                    y,
                    17,
                    color,
                    bold=True
                )

        # Footer
        draw_text(
            screen,
            "LEFT / RIGHT  CHANGE GAME     ESC  BACK",
            width // 2,
            height - 45,
            15,
            MUTED,
            center=True
        )

        pygame.display.flip()
        clock.tick(60)
