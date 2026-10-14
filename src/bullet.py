# 弹幕: 生成、移动、绘制与碰撞检测
import random
import pygame

from settings import (BULLET_RADIUS, BULLET_SPEED, SPAWN_COUNT, CULL_MARGIN,
                      RADIUS, SHOT_RADIUS, SHOT_SPEED)


def spawn(bullets, size):
    """从屏幕外随机边缘生成随机数量、随机路径的弹幕"""
    w, h = size
    for _ in range(random.randint(*SPAWN_COUNT)):
        edge = random.randint(0, 3)  # 0上 1下 2左 3右
        if edge == 0:
            pos = pygame.Vector2(random.uniform(0, w), -BULLET_RADIUS)
        elif edge == 1:
            pos = pygame.Vector2(random.uniform(0, w), h + BULLET_RADIUS)
        elif edge == 2:
            pos = pygame.Vector2(-BULLET_RADIUS, random.uniform(0, h))
        else:
            pos = pygame.Vector2(w + BULLET_RADIUS, random.uniform(0, h))
        # 随机选取屏幕内目标点, 形成随机穿越路径
        target = pygame.Vector2(random.uniform(0, w), random.uniform(0, h))
        vel = (target - pos).normalize() * random.uniform(*BULLET_SPEED)
        bullets.append([pos, vel])


def spawn_shot(shots, start, target):
    """从 start 朝 target 方向发射一颗子弹"""
    direction = target - start
    if direction:
        direction.normalize_ip()
        shots.append([start.copy(), direction * SHOT_SPEED])


def update(projs, size, dt):
    """移动飞行物并移除飞出屏幕的, 返回存活列表 (弹幕与子弹共用)"""
    w, h = size
    for pos, vel in projs:
        pos += vel * dt
    return [p for p in projs
            if -CULL_MARGIN < p[0].x < w + CULL_MARGIN
            and -CULL_MARGIN < p[0].y < h + CULL_MARGIN]


def draw(screen, projs, color, radius):
    for pos, _ in projs:
        pygame.draw.circle(screen, color, pos, radius)


def collide(shots, bullets):
    """子弹与弹幕相互抵消: 一颗子弹最多消除一颗弹幕, 返回 (存活子弹, 存活弹幕)"""
    remaining = bullets[:]
    kept = []
    for shot in shots:
        hit = next((b for b in remaining
                    if (b[0] - shot[0]).length_squared() < (SHOT_RADIUS + BULLET_RADIUS) ** 2),
                   None)
        if hit is None:
            kept.append(shot)
        else:
            remaining.remove(hit)
    return kept, remaining


def hits_player(bullets, player_pos):
    """检测是否有弹幕碰到玩家 (圆-圆碰撞)"""
    return any((b[0] - player_pos).length_squared() < (RADIUS + BULLET_RADIUS) ** 2
               for b in bullets)
