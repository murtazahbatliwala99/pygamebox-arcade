"""Shared visual components for PyGameBox."""
import pygame
from . import config as C

_FONT_CACHE = {}

def font(size, bold=False):
    key = (size, bold)
    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = pygame.font.SysFont("segoeui", size, bold=bold)
    return _FONT_CACHE[key]

def text(surface, value, x, y, size=24, color=C.WHITE, font_obj=None, center=False, bold=False):
    chosen = font_obj or font(size, bold)
    image = chosen.render(str(value), True, color)
    rect = image.get_rect()
    rect.center = (x, y) if center else rect.topleft
    if not center:
        rect.topleft = (x, y)
    surface.blit(image, rect)
    return rect

def panel(surface, rect, color=C.PANEL, radius=18, border=None):
    rect = pygame.Rect(rect)
    shadow = rect.move(0, 5)
    pygame.draw.rect(surface, (5, 8, 16), shadow, border_radius=radius)
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border:
        pygame.draw.rect(surface, border, rect, 2, border_radius=radius)

def background(surface):
    surface.fill(C.BG)
    pygame.draw.circle(surface, (22, 34, 61), (0, 0), 260)
    pygame.draw.circle(surface, (29, 24, 58), (C.WIDTH, C.HEIGHT), 300)
    # Subtle arcade grid.
    for x in range(0, C.WIDTH, 50):
        pygame.draw.line(surface, (19, 25, 42), (x, 0), (x, C.HEIGHT), 1)
    for y in range(0, C.HEIGHT, 50):
        pygame.draw.line(surface, (19, 25, 42), (0, y), (C.WIDTH, y), 1)

def draw_arrow(surface, center, direction, color=C.WHITE, scale=1.0):
    cx, cy = center
    length = int(10 * scale)
    vectors = {
        "left": ((cx+length, cy), (cx-length, cy)),
        "right": ((cx-length, cy), (cx+length, cy)),
        "up": ((cx, cy+length), (cx, cy-length)),
        "down": ((cx, cy-length), (cx, cy+length)),
    }
    start, end = vectors[direction]
    pygame.draw.line(surface, color, start, end, max(2, int(3*scale)))
    ex, ey = end
    wing = int(8*scale)
    if direction == "left":
        points = [(ex-1,ey),(ex+wing,ey-wing),(ex+wing,ey+wing)]
    elif direction == "right":
        points = [(ex+1,ey),(ex-wing,ey-wing),(ex-wing,ey+wing)]
    elif direction == "up":
        points = [(ex,ey-1),(ex-wing,ey+wing),(ex+wing,ey+wing)]
    else:
        points = [(ex,ey+1),(ex-wing,ey-wing),(ex+wing,ey-wing)]
    pygame.draw.polygon(surface, color, points)

def arrow_key(surface, rect, direction, accent=C.CYAN, label=None):
    rect = pygame.Rect(rect)
    pygame.draw.rect(surface, (38, 49, 72), rect, border_radius=8)
    pygame.draw.rect(surface, accent, rect, 2, border_radius=8)
    if label:
        text(surface, label, rect.centerx, rect.centery, 17, C.WHITE, center=True, bold=True)
    else:
        draw_arrow(surface, rect.center, direction, C.WHITE, 0.9)

def keycap(surface, rect, label, accent=C.CYAN):
    rect = pygame.Rect(rect)
    pygame.draw.rect(surface, (38, 49, 72), rect, border_radius=8)
    pygame.draw.rect(surface, accent, rect, 2, border_radius=8)
    text(surface, label, rect.centerx, rect.centery, 16, C.WHITE, center=True, bold=True)

def game_header(surface, title, score, best, accent=C.CYAN):
    panel(surface, (25, 18, 950, 72), (20, 28, 47), 16)
    text(surface, title, 48, 31, 34, C.WHITE, bold=True)
    text(surface, f"SCORE  {score}", 650, 31, 22, accent, bold=True)
    text(surface, f"BEST  {best}", 825, 31, 20, C.MUTED, bold=True)

def control_footer(surface, message):
    panel(surface, (150, 586, 700, 42), (20, 28, 47), 12)
    text(surface, message, 500, 607, 18, C.MUTED, center=True)

def game_over(surface, score, best):
    overlay = pygame.Surface((C.WIDTH, C.HEIGHT), pygame.SRCALPHA)
    overlay.fill((5, 8, 16, 205))
    surface.blit(overlay, (0, 0))
    panel(surface, (275, 220, 450, 210), (25, 34, 56), 22, C.PINK)
    text(surface, "GAME OVER", C.WIDTH//2, 265, 52, C.PINK, center=True, bold=True)
    text(surface, f"Score: {score}     Best: {best}", C.WIDTH//2, 325, 25, C.WHITE, center=True)
    text(surface, "R  RESTART       ESC  MAIN MENU", C.WIDTH//2, 385, 18, C.MUTED, center=True)

def draw_control_panel(surface, rect, title, rows, accent=C.CYAN):
    """Rows are (kind, value, label); kind is arrow, key, or text."""
    panel(surface, rect, C.PANEL, 16)
    x, y, w, h = rect
    text(surface, title, x+w//2, y+24, 21, accent, center=True, bold=True)
    row_y = y+58
    for kind, value, label in rows:
        if kind == "arrow":
            arrow_key(surface, (x+18, row_y-17, 38, 34), value, accent)
        elif kind == "key":
            keycap(surface, (x+18, row_y-17, 58, 34), value, accent)
        else:
            pass
        text(surface, label, x+90, row_y, 17, C.WHITE, center=False)
        row_y += 43
