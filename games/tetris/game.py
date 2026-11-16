import random
import pygame
from core import config as C
from core.ui import (
    background, text, panel, game_over, arrow_key, keycap, game_header
)

SHAPES = [
    [[1,1,1,1]], [[1,1],[1,1]], [[0,1,0],[1,1,1]],
    [[1,0,0],[1,1,1]], [[0,0,1],[1,1,1]],
    [[1,1,0],[0,1,1]], [[0,1,1],[1,1,0]],
]
COLORS = [C.CYAN, C.YELLOW, C.PURPLE, C.PINK, C.GREEN, C.RED, (255,150,75)]
W, H, CELL = 10, 20, 25

def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]

def run(screen, clock, store):
    board = [[None for _ in range(W)] for _ in range(H)]
    shape, color = random.choice(SHAPES), random.choice(COLORS)
    x, y = 3, 0
    score, dead, timer = 0, False, 0
    best = store.high_score("tetris")

    def valid(candidate, ox, oy):
        for ry, row in enumerate(candidate):
            for rx, value in enumerate(row):
                if value:
                    nx, ny = ox+rx, oy+ry
                    if nx < 0 or nx >= W or ny >= H: return False
                    if ny >= 0 and board[ny][nx] is not None: return False
        return True

    def spawn():
        return random.choice(SHAPES), random.choice(COLORS), 3, 0

    while True:
        dt = clock.tick(C.FPS)
        timer += dt
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE: return
                if e.key == pygame.K_r and dead: return run(screen, clock, store)
                if not dead:
                    if e.key == pygame.K_LEFT and valid(shape, x-1, y): x -= 1
                    elif e.key == pygame.K_RIGHT and valid(shape, x+1, y): x += 1
                    elif e.key == pygame.K_UP:
                        turned = rotate(shape)
                        if valid(turned, x, y): shape = turned
                    elif e.key == pygame.K_DOWN and valid(shape, x, y+1):
                        y += 1
                        score += 1
                    elif e.key == pygame.K_SPACE:
                        while valid(shape, x, y+1): y += 1
                        timer = 1000

        if not dead and timer > max(100, 550-score//20):
            timer = 0
            if valid(shape, x, y+1):
                y += 1
            else:
                for ry, row in enumerate(shape):
                    for rx, value in enumerate(row):
                        if value and y+ry >= 0: board[y+ry][x+rx] = color
                board = [row for row in board if any(v is None for v in row)]
                cleared = H-len(board)
                if cleared:
                    score += [0,100,300,500,800][min(cleared,4)]
                    board = [[None for _ in range(W)] for _ in range(cleared)] + board
                shape, color, x, y = spawn()
                if not valid(shape, x, y):
                    dead = True
                    best = store.record("tetris", score)

        background(screen)
        game_header(screen, "TETRIS", score, best, C.YELLOW)

        # Left control panel: real vector arrows in key-shaped buttons.
        panel(screen, (45, 115, 270, 420), C.PANEL, 18)
        text(screen, "HOW TO PLAY", 180, 145, 24, C.CYAN, center=True, bold=True)
        controls = [
            ("up", "ROTATE", 205),
            ("left", "MOVE LEFT", 270),
            ("right", "MOVE RIGHT", 335),
            ("down", "SOFT DROP", 400),
        ]
        for direction, label, cy in controls:
            arrow_key(screen, (85, cy-19, 48, 38), direction, C.CYAN)
            text(screen, label, 160, cy, 18, C.WHITE, center=False)
        keycap(screen, (85, 465, 85, 38), "SPACE", C.YELLOW)
        text(screen, "HARD DROP", 190, 484, 17, C.WHITE, center=False)

        # Board
        ox, oy = 385, 115
        panel(screen, (ox-12, oy-12, W*CELL+24, H*CELL+24), (8,12,22), 14, C.PURPLE)
        for yy in range(H):
            for xx in range(W):
                value = board[yy][xx]
                rect = (ox+xx*CELL+1, oy+yy*CELL+1, CELL-2, CELL-2)
                if value:
                    pygame.draw.rect(screen, value, rect, border_radius=5)
                    pygame.draw.line(screen, tuple(min(255,c+45) for c in value),
                                     (rect[0]+4, rect[1]+3), (rect[0]+CELL-6, rect[1]+3), 2)
                else:
                    pygame.draw.rect(screen, (28,35,54), rect, 1, border_radius=4)
        for ry, row in enumerate(shape):
            for rx, value in enumerate(row):
                if value:
                    rect = (ox+(x+rx)*CELL+1, oy+(y+ry)*CELL+1, CELL-2, CELL-2)
                    pygame.draw.rect(screen, color, rect, border_radius=5)

        panel(screen, (690, 145, 255, 170), C.PANEL, 16)
        text(screen, "THE GOAL", 817, 177, 23, C.YELLOW, center=True, bold=True)
        text(screen, "Complete full rows", 817, 225, 18, C.WHITE, center=True)
        text(screen, "to clear them and score.", 817, 253, 17, C.MUTED, center=True)
        panel(screen, (690, 345, 255, 150), C.PANEL, 16)
        text(screen, "QUICK TIPS", 817, 376, 21, C.CYAN, center=True, bold=True)
        text(screen, "Plan your stack.", 817, 420, 17, C.WHITE, center=True)
        text(screen, "Avoid gaps.", 817, 450, 17, C.WHITE, center=True)
        text(screen, "ESC  MAIN MENU", 817, 545, 17, C.MUTED, center=True)
        if dead:
            game_over(screen, score, best)
        pygame.display.flip()
