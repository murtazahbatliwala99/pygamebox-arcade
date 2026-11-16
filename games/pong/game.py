import pygame
from core import config as C
from core.ui import background, text, panel, game_over, arrow_key, keycap, game_header

def run(screen, clock, store):
    paddle_l = pygame.Rect(65, 245, 18, 112)
    paddle_r = pygame.Rect(C.WIDTH-83, 245, 18, 112)
    ball = pygame.Rect(C.WIDTH//2-10, 315, 20, 20)
    vx, vy = 6, 4
    scores = [0, 0]
    dead = False
    best = store.high_score("pong")
    while True:
        clock.tick(C.FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE: return
                if e.key == pygame.K_r and dead: return run(screen, clock, store)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: paddle_l.y -= 7
        if keys[pygame.K_s]: paddle_l.y += 7
        if keys[pygame.K_UP]: paddle_r.y -= 7
        if keys[pygame.K_DOWN]: paddle_r.y += 7
        paddle_l.y = max(112, min(485, paddle_l.y))
        paddle_r.y = max(112, min(485, paddle_r.y))
        if not dead:
            ball.x += vx
            ball.y += vy
            if ball.top <= 112 or ball.bottom >= 545: vy *= -1
            if ball.colliderect(paddle_l) and vx < 0:
                vx = abs(vx) + 0.25
                vy += (ball.centery-paddle_l.centery)*0.045
            if ball.colliderect(paddle_r) and vx > 0:
                vx = -abs(vx) - 0.25
                vy += (ball.centery-paddle_r.centery)*0.045
            if ball.left < 0:
                scores[1] += 1; ball.center = (C.WIDTH//2, 315); vx = -6; vy = 4
            if ball.right > C.WIDTH:
                scores[0] += 1; ball.center = (C.WIDTH//2, 315); vx = 6; vy = -4
            if max(scores) >= 5:
                dead = True
                best = store.record("pong", max(scores))

        background(screen)
        game_header(screen, "PONG  •  TWO PLAYER", f"{scores[0]} : {scores[1]}", best, C.CYAN)
        arena = pygame.Rect(35, 108, 930, 445)
        panel(screen, arena, (8, 13, 25), 16)
        for y in range(120, 545, 28):
            pygame.draw.rect(screen, (62, 78, 110), (C.WIDTH//2-2, y, 4, 15), border_radius=2)
        pygame.draw.rect(screen, C.CYAN, paddle_l, border_radius=9)
        pygame.draw.rect(screen, C.PINK, paddle_r, border_radius=9)
        pygame.draw.ellipse(screen, C.WHITE, ball)
        pygame.draw.circle(screen, (75, 205, 230), ball.center, 18, 1)

        # Two separate illustrated control panels
        panel(screen, (90, 566, 350, 70), C.PANEL, 13)
        text(screen, "PLAYER 1", 150, 582, 16, C.CYAN, center=True, bold=True)
        keycap(screen, (220, 574, 42, 26), "W", C.CYAN)
        text(screen, "UP", 285, 587, 15, C.WHITE, center=True)
        keycap(screen, (220, 606, 42, 26), "S", C.CYAN)
        text(screen, "DOWN", 285, 619, 15, C.WHITE, center=True)

        panel(screen, (560, 566, 350, 70), C.PANEL, 13)
        text(screen, "PLAYER 2", 620, 582, 16, C.PINK, center=True, bold=True)
        arrow_key(screen, (690, 574, 38, 26), "up", C.PINK)
        text(screen, "UP", 755, 587, 15, C.WHITE, center=True)
        arrow_key(screen, (690, 606, 38, 26), "down", C.PINK)
        text(screen, "DOWN", 755, 619, 15, C.WHITE, center=True)
        if dead:
            game_over(screen, max(scores), best)
        pygame.display.flip()
