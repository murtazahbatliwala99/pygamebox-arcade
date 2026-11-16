import random
import pygame
from core import config as C
from core.ui import (
    background, text, panel, game_header, game_over, draw_control_panel,
    arrow_key, keycap
)

CELL = 20
COLS, ROWS = 42, 21
BOARD_X, BOARD_Y = 80, 112

def choose_mode(screen, clock, store):
    selected = 0
    modes = [
        ("CLASSIC", "Wall collision ends the run.", C.PINK, "snake_classic"),
        ("WRAPAROUND", "Exit one edge, return on the opposite edge.", C.GREEN, "snake_wrap"),
    ]
    while True:
        background(screen)
        text(screen, "SNAKE", 500, 85, 58, C.WHITE, center=True, bold=True)
        text(screen, "CHOOSE YOUR MODE", 500, 145, 22, C.CYAN, center=True, bold=True)
        mouse = pygame.mouse.get_pos()
        cards = []
        for i, (name, desc, accent, key) in enumerate(modes):
            rect = pygame.Rect(145+i*370, 220, 340, 245)
            cards.append(rect)
            active = i == selected or rect.collidepoint(mouse)
            panel(screen, rect, (35, 48, 74) if active else C.PANEL, 20, accent if active else None)
            text(screen, name, rect.centerx, rect.y+58, 30, accent, center=True, bold=True)
            text(screen, desc, rect.centerx, rect.y+112, 17, C.WHITE, center=True)
            text(screen, f"BEST  {store.high_score(key)}", rect.centerx, rect.y+165, 21, C.YELLOW, center=True, bold=True)
            text(screen, "ENTER TO SELECT" if i == selected else "CLICK TO SELECT",
                 rect.centerx, rect.y+205, 15, C.MUTED, center=True)
        text(screen, "LEFT / RIGHT  SELECT       ENTER  PLAY       ESC  BACK", 500, 555, 18, C.MUTED, center=True)
        pygame.display.flip()
        clock.tick(C.FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return None
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return None
                if e.key in (pygame.K_LEFT, pygame.K_a):
                    selected = (selected-1) % 2
                elif e.key in (pygame.K_RIGHT, pygame.K_d):
                    selected = (selected+1) % 2
                elif e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return modes[selected][3]
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for i, rect in enumerate(cards):
                    if rect.collidepoint(e.pos):
                        return modes[i][3]

def run(screen, clock, store):
    mode_key = choose_mode(screen, clock, store)
    if mode_key is None:
        return
    wrap = mode_key == "snake_wrap"
    snake = [(COLS//2, ROWS//2), (COLS//2-1, ROWS//2), (COLS//2-2, ROWS//2)]
    direction = (1, 0)
    next_direction = direction
    food = (random.randrange(COLS), random.randrange(ROWS))
    score, paused, dead = 0, False, False
    move_timer = 0
    best = store.high_score(mode_key)

    while True:
        dt = clock.tick(C.FPS)
        move_timer += dt
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return
                if e.key == pygame.K_p and not dead:
                    paused = not paused
                if e.key == pygame.K_r and dead:
                    return run(screen, clock, store)
                keys = {
                    pygame.K_UP:(0,-1), pygame.K_w:(0,-1),
                    pygame.K_DOWN:(0,1), pygame.K_s:(0,1),
                    pygame.K_LEFT:(-1,0), pygame.K_a:(-1,0),
                    pygame.K_RIGHT:(1,0), pygame.K_d:(1,0)
                }
                if e.key in keys:
                    candidate = keys[e.key]
                    if candidate != (-direction[0], -direction[1]):
                        next_direction = candidate

        if not paused and not dead and move_timer >= max(65, 125-score//3):
            move_timer = 0
            direction = next_direction
            nx, ny = snake[0][0]+direction[0], snake[0][1]+direction[1]
            if wrap:
                nx %= COLS
                ny %= ROWS
            elif nx < 0 or nx >= COLS or ny < 0 or ny >= ROWS:
                dead = True
                best = store.record(mode_key, score)
                continue
            head = (nx, ny)
            body_to_check = snake[:-1] if head not in (food,) else snake
            if head in body_to_check:
                dead = True
                best = store.record(mode_key, score)
            else:
                snake.insert(0, head)
                if head == food:
                    score += 10
                    free = [(x,y) for x in range(COLS) for y in range(ROWS) if (x,y) not in snake]
                    if free:
                        food = random.choice(free)
                    else:
                        dead = True
                        best = store.record(mode_key, score)
                else:
                    snake.pop()

        background(screen)
        title = "SNAKE  •  WRAPAROUND" if wrap else "SNAKE  •  CLASSIC"
        game_header(screen, title, score, best, C.GREEN)
        board_rect = pygame.Rect(BOARD_X, BOARD_Y, COLS*CELL, ROWS*CELL)
        panel(screen, board_rect, (8, 13, 25), 12, C.GREEN if wrap else C.PINK)
        # Subtle grid
        for gx in range(COLS+1):
            x = BOARD_X + gx*CELL
            pygame.draw.line(screen, (18, 27, 43), (x, BOARD_Y), (x, BOARD_Y+ROWS*CELL), 1)
        for gy in range(ROWS+1):
            y = BOARD_Y + gy*CELL
            pygame.draw.line(screen, (18, 27, 43), (BOARD_X, y), (BOARD_X+COLS*CELL, y), 1)
        # Food glow and body segments
        fx, fy = food
        pygame.draw.circle(screen, (90, 35, 70), (BOARD_X+fx*CELL+10, BOARD_Y+fy*CELL+10), 12)
        pygame.draw.circle(screen, C.PINK, (BOARD_X+fx*CELL+10, BOARD_Y+fy*CELL+10), 7)
        for i, (sx, sy) in enumerate(snake):
            rect = pygame.Rect(BOARD_X+sx*CELL+2, BOARD_Y+sy*CELL+2, CELL-4, CELL-4)
            color = (110, 255, 185) if i == 0 else (52, 190, 133)
            pygame.draw.rect(screen, color, rect, border_radius=6)
            if i == 0:
                pygame.draw.circle(screen, C.BG, (rect.centerx-4, rect.centery-3), 2)
                pygame.draw.circle(screen, C.BG, (rect.centerx+4, rect.centery-3), 2)

        # Persistent visual controls, no font-dependent arrow glyphs.
        panel(screen, (80, 548, 840, 78), C.PANEL, 14)
        text(screen, "MOVE", 130, 586, 18, C.CYAN, center=True, bold=True)
        arrow_key(screen, (175, 568, 38, 34), "left", C.GREEN)
        arrow_key(screen, (218, 568, 38, 34), "down", C.GREEN)
        arrow_key(screen, (261, 568, 38, 34), "up", C.GREEN)
        arrow_key(screen, (304, 568, 38, 34), "right", C.GREEN)
        text(screen, "OR  W A S D", 390, 586, 17, C.WHITE, center=True)
        keycap(screen, (480, 568, 42, 34), "P", C.YELLOW)
        text(screen, "PAUSE", 550, 586, 17, C.WHITE, center=True)
        text(screen, "ESC  MENU", 730, 586, 17, C.MUTED, center=True)
        if paused:
            panel(screen, (350, 265, 300, 100), (25, 34, 56), 18, C.YELLOW)
            text(screen, "PAUSED", 500, 300, 38, C.YELLOW, center=True, bold=True)
            text(screen, "Press P to continue", 500, 340, 17, C.WHITE, center=True)
        if dead:
            game_over(screen, score, best)
        pygame.display.flip()
