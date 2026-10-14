# UI: 字体加载与游戏结束弹窗
import pygame


def load_font(size):
    """按优先级加载可用的中文字体"""
    for name in ("microsoftyahei", "simhei", "simsun"):
        path = pygame.font.match_font(name)
        if path:
            return pygame.font.Font(path, size)
    return pygame.font.Font(None, size)


def draw_game_over(screen, font_big, font_small):
    """游戏结束弹窗: 半透明遮罩 + 圆角面板 + 提示文字"""
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    panel = pygame.Rect(0, 0, 420, 200)
    panel.center = (screen.get_width() // 2, screen.get_height() // 2)
    pygame.draw.rect(screen, (30, 30, 40), panel, border_radius=12)
    pygame.draw.rect(screen, (100, 140, 255), panel, 2, border_radius=12)
    title = font_big.render("游戏结束", True, (255, 90, 90))
    hint = font_small.render("按 R 重新开始", True, "white")
    screen.blit(title, title.get_rect(center=(panel.centerx, panel.centery - 35)))
    screen.blit(hint, hint.get_rect(center=(panel.centerx, panel.centery + 35)))
