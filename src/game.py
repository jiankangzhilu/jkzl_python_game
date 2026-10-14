# Example file showing a circle moving on screen
# 主入口: 游戏状态、事件循环与绘制编排
# 依赖同目录下的 settings / effects / bullet / ui 模块, 复制整个文件夹即可运行
import random
import pygame

import bullet
import effects
import ui
from settings import (SCREEN_SIZE, FPS, RADIUS, SPEED_FAST, SPEED_SLOW,
                      BLINK_DIST, BLINK_CD, SPAWN_INTERVAL, SPAWN_DELAY,
                      FIRE_CD, BULLET_RADIUS, BULLET_COLOR, SHOT_RADIUS,
                      SHOT_COLOR, PLAYER_FILL, PLAYER_BORDER)

# pygame setup
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
running = True
dt = 0

font_big = ui.load_font(56)
font_small = ui.load_font(28)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
last_dir = pygame.Vector2(1, 0)     # 最近一次移动方向, 闪烁沿此方向
blink_timer = 0                     # 闪烁剩余冷却时间
fire_timer = 0                      # 开火剩余冷却时间
trail = []                          # 拖影列表: [位置, 剩余生命]
bullets = []                        # 弹幕列表: [位置, 速度]
shots = []                          # 子弹列表: [位置, 速度]
particles = []                      # 消散粒子: [位置, 速度, 剩余生命, 颜色]
spawn_timer = SPAWN_DELAY           # 距下一波弹幕的时间
game_over = False


def clamp_to_screen(pos):
    """将位置限制在屏幕边界内"""
    pos.x = max(RADIUS, min(pos.x, screen.get_width() - RADIUS))
    pos.y = max(RADIUS, min(pos.y, screen.get_height() - RADIUS))


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # 鼠标右键: 沿当前/最近移动方向闪烁一小段距离
        elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3
              and not game_over and blink_timer <= 0):
            start = player_pos.copy()
            player_pos += last_dir * BLINK_DIST
            clamp_to_screen(player_pos)
            trail += effects.make_blink_trail(start, player_pos)
            blink_timer = BLINK_CD

    keys = pygame.key.get_pressed()
    if game_over:
        # 按下 R 键重新开始
        if keys[pygame.K_r]:
            player_pos.update(screen.get_width() / 2, screen.get_height() / 2)
            last_dir.update(1, 0)
            blink_timer = 0
            fire_timer = 0
            spawn_timer = SPAWN_DELAY
            trail.clear()
            bullets.clear()
            shots.clear()
            particles.clear()
            game_over = False
    else:
        # WASD 移动, 按住 Shift 减速; 斜向归一化保证各方向速度一致
        direction = pygame.Vector2(keys[pygame.K_d] - keys[pygame.K_a],
                                   keys[pygame.K_s] - keys[pygame.K_w])
        if direction:
            direction.normalize_ip()
            last_dir = direction.copy()
            speed = SPEED_SLOW if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else SPEED_FAST
            player_pos += direction * speed * dt
            clamp_to_screen(player_pos)
        # 按住鼠标左键: 朝鼠标位置发射绿色子弹
        if fire_timer <= 0 and pygame.mouse.get_pressed()[0]:
            bullet.spawn_shot(shots, player_pos, pygame.Vector2(pygame.mouse.get_pos()))
            fire_timer = FIRE_CD

    # 更新冷却、生成并移动弹幕与子弹
    blink_timer -= dt
    fire_timer -= dt
    spawn_timer -= dt
    if spawn_timer <= 0:
        bullet.spawn(bullets, screen.get_size())
        spawn_timer = random.uniform(*SPAWN_INTERVAL)
    bullets = bullet.update(bullets, screen.get_size(), dt)
    shots = bullet.update(shots, screen.get_size(), dt)
    # 子弹与弹幕相互抵消 (先于玩家碰撞判定, 允许拦截救场)
    shots, bullets = bullet.collide(shots, bullets)

    # 更新拖影与消散粒子生命
    trail = effects.update_trail(trail, dt)
    particles = effects.update_particles(particles, dt)

    # 玩家与弹幕碰撞: 消散为粒子并弹出游戏结束
    if not game_over and bullet.hits_player(bullets, player_pos):
        game_over = True
        particles = effects.make_dissolve_particles(player_pos)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    bullet.draw(screen, bullets, BULLET_COLOR, BULLET_RADIUS)
    bullet.draw(screen, shots, SHOT_COLOR, SHOT_RADIUS)
    effects.draw_trail(screen, trail)
    effects.draw_particles(screen, particles)

    # 玩家: 白色带蓝色边框
    if not game_over:
        pygame.draw.circle(screen, PLAYER_FILL, player_pos, RADIUS)
        pygame.draw.circle(screen, PLAYER_BORDER, player_pos, RADIUS, 2)

    # 游戏结束弹窗
    if game_over:
        ui.draw_game_over(screen, font_big, font_small)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(FPS) / 1000

pygame.quit()
