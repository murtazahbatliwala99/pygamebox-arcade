
"""Player registration screen for PyGameBox."""

import pygame
from . import config as C
from .ui import background, text, panel


def register_player(screen, clock, player_manager):
    """Ask for a player name and save it."""

    name = ""
    active = True
    input_box = pygame.Rect(300, 300, 400, 55)
    error_message = ""

    title_font = pygame.font.SysFont("segoeui", 48, bold=True)

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    cleaned_name = name.strip()

                    if cleaned_name:
                        try:
                            player_manager.save_player(cleaned_name)
                            return cleaned_name
                        except ValueError as error:
                            error_message = str(error)
                    else:
                        error_message = "Please enter a player name."

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                elif event.unicode.isprintable() and len(name) < 20:
                    name += event.unicode
                    error_message = ""

        background(screen)

        panel(
            screen,
            (200, 180, 600, 330),
            C.PANEL,
            24,
            C.CYAN
        )

        heading = title_font.render(
            "WELCOME PLAYER",
            True,
            C.WHITE
        )
        screen.blit(
            heading,
            heading.get_rect(center=(C.WIDTH // 2, 225))
        )

        text(
            screen,
            "Choose your arcade name",
            C.WIDTH // 2,
            270,
            21,
            C.MUTED,
            center=True
        )

        pygame.draw.rect(
            screen,
            (35, 47, 72),
            input_box,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            C.CYAN,
            input_box,
            2,
            border_radius=10
        )

        displayed_name = name if name else "Enter your name..."
        name_color = C.WHITE if name else C.MUTED

        text(
            screen,
            displayed_name,
            input_box.x + 15,
            input_box.y + 15,
            22,
            name_color
        )

        text(
            screen,
            f"{len(name)}/20 characters",
            C.WIDTH // 2,
            375,
            15,
            C.MUTED,
            center=True
        )

        if error_message:
            text(
                screen,
                error_message,
                C.WIDTH // 2,
                410,
                17,
                C.RED,
                center=True
            )

        text(
            screen,
            "PRESS ENTER TO CONTINUE",
            C.WIDTH // 2,
            455,
            19,
            C.CYAN,
            center=True,
            bold=True
        )

        pygame.display.flip()
        clock.tick(C.FPS)

    return None
