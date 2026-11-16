import random
import pygame
from core import config as C
from core.ui import background, text, panel, game_over, arrow_key, keycap, game_header

def run(screen, clock, store):
    player = pygame.Rect(C.WIDTH//2-22, 535, 44, 34)
    bullets, enemies, particles = [], [], []
    spawn_timer = fire_timer = 0
    score, dead = 0, False
    best = store.high_score("shooter")
    fire_interval = 245

    while True:
        dt = clock.tick(C.FPS)
        spawn_timer += dt
        fire_timer += dt
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE: return
                if e.key == pygame.K_r and dead: return run(screen, clock, store)

        keys = pygame.key.get_pressed()
        if not dead:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: player.x -= 7
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: player.x += 7
            player.x = max(25, min(C.WIDTH-69, player.x))
            if fire_timer >= fire_interval:
                fire_timer = 0
                bullets.append(pygame.Rect(player.centerx-3, player.top-18, 6, 22))
            if spawn_timer > max(300, 950-score*2):
                spawn_timer = 0
                enemies.append(pygame.Rect(random.randint(35, C.WIDTH-70), -40, 34, 30))

            for bullet in bullets[:]:
                bullet.y -= 12
                if bullet.bottom < 95: bullets.remove(bullet)
            for enemy in enemies[:]:
                enemy.y += 3 + score//120
                if enemy.top > 555 or enemy.colliderect(player):
                    dead = True
                    best = store.record("shooter", score)
                    break
            for bullet in bullets[:]:
                hit = next((enemy for enemy in enemies if bullet.colliderect(enemy)), None)
                if hit:
                    enemies.remove(hit)
                    if bullet in bullets: bullets.remove(bullet)
                    score += 10
                    particles.append([hit.centerx, hit.centery, 10])

        background(screen)
        game_header(screen, "SPACE SHOOTER", score, best, C.PINK)
        arena = pygame.Rect(35, 105, 930, 450)
        panel(screen, arena, (8, 13, 25), 16)
        # Stars
        for i in range(34):
            sx = (i*137 + 31) % 920 + 40
            sy = (i*83 + 112) % 425 + 110
            pygame.draw.circle(screen, (70, 91, 132), (sx, sy), 1)
        # Ship glow and ship
        pygame.draw.circle(screen, (25, 91, 112), player.center, 30, 2)
        pygame.draw.polygon(screen, C.CYAN, [(player.centerx, player.top), (player.left, player.bottom), (player.right, player.bottom)])
        pygame.draw.polygon(screen, C.WHITE, [(player.centerx, player.top+8), (player.centerx-7, player.bottom-5), (player.centerx+7, player.bottom-5)])
        for bullet in bullets:
            pygame.draw.rect(screen, (255, 220, 110), bullet.inflate(5, 5), border_radius=4)
            pygame.draw.rect(screen, C.YELLOW, bullet, border_radius=3)
        for enemy in enemies:
            pygame.draw.rect(screen, C.PINK, enemy, border_radius=8)
            pygame.draw.rect(screen, (255, 180, 205), enemy, 2, border_radius=8)
            pygame.draw.circle(screen, C.BG, (enemy.centerx-8, enemy.centery), 3)
            pygame.draw.circle(screen, C.BG, (enemy.centerx+8, enemy.centery), 3)

        panel(screen, (120, 566, 760, 70), C.PANEL, 13)
        text(screen, "MOVE", 175, 600, 17, C.CYAN, center=True, bold=True)
        arrow_key(screen, (225, 583, 38, 34), "left", C.CYAN)
        arrow_key(screen, (268, 583, 38, 34), "right", C.CYAN)
        text(screen, "OR  A / D", 370, 600, 17, C.WHITE, center=True)
        panel(screen, (535, 580, 285, 42), (23, 66, 60), 10)
        text(screen, "AUTO-FIRE  •  ON", 677, 601, 18, C.GREEN, center=True, bold=True)
        if dead:
            game_over(screen, score, best)
        pygame.display.flip()
