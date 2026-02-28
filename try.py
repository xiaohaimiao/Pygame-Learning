#pgzrun try.py
WIDTH = 720
HEIGHT = 1080

import pygame

# 在代码开头添加
chinese_font = pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', 30)

def draw():
    screen.clear()
    # 渲染文本
    text_surface = chinese_font.render("按下空格开始！", True, "white")
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    screen.blit(text_surface, text_rect)

