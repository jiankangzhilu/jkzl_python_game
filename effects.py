# 视觉效果: 闪烁拖影与消散粒子
import random
import pygame

from settings import (TRAIL_LIFE, TRAIL_COLOR, PARTICLE_LIFE, PARTICLE_COUNT,
                      PARTICLE_COLORS, RADIUS)


def make_blink_trail(start, end):
    """沿闪烁路径生成拖影"""
    return [[start.lerp(end, i / 7), TRAIL_LIFE] for i in range(8)]


def make_dissolve_particles(pos):
    """玩家消散时向四周飞溅的粒子"""
    return [[pos.copy(),
             pygame.Vector2(1, 0).rotate(random.uniform(0, 360)) * random.uniform(50, 220),
             PARTICLE_LIFE,
             random.choice(PARTICLE_COLORS)]
            for _ in range(PARTICLE_COUNT)]


def update_trail(trail, dt):
    """拖影生命递减并移除消亡项"""
    for ghost in trail:
        ghost[1] -= dt
    return [g for g in trail if g[1] > 0]


def update_particles(particles, dt):
    """粒子移动、生命递减并移除消亡项"""
    for p in particles:
        p[0] += p[1] * dt
        p[2] -= dt
    return [p for p in particles if p[2] > 0]


def _fade_surface(screen, items, draw_item):
    """在透明图层上绘制一组渐隐元素并合成到屏幕"""
    if not items:
        return
    surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    for item in items:
        draw_item(surf, item)
    screen.blit(surf, (0, 0))


def draw_trail(screen, trail):
    def draw(surf, item):
        pos, life = item
        ratio = life / TRAIL_LIFE
        pygame.draw.circle(surf, (*TRAIL_COLOR, int(160 * ratio)),
                           pos, max(1, int(RADIUS * ratio)))
    _fade_surface(screen, trail, draw)


def draw_particles(screen, particles):
    def draw(surf, item):
        pos, _, life, color = item
        ratio = life / PARTICLE_LIFE
        pygame.draw.circle(surf, (*color, int(220 * ratio)),
                           pos, max(1, int(3 * ratio)))
    _fade_surface(screen, particles, draw)
