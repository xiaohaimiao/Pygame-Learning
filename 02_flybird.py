# -*- coding: utf-8 -*-
#pgzrun flybird.py
# V1.0 完成基本功能
# V1.1 设置大小、初始位置在屏幕居中
# V1.2 空格开始，空格重启
# V1.3 计分、关卡：达到分数后提速
# V1.4 中文提示、显示分数
# TODO: V1.5
import random
import pgzrun
import os
import pygame
from pgzero.builtins import Actor
os.environ['SDL_VIDEO_CENTERED'] = '1'

WIDTH = 720
HEIGHT = 1000
GAP = 350
SPEED = 3
GRAVITY = 0.3
FLAP_VELOCITY = -5
SCORE = 0
bird_x = 100
bird_y = HEIGHT // 2
bird = Actor('bird', pos = (bird_x, bird_y))
stage = Actor("stage")
pipe_top = Actor("pipe", pos=(WIDTH, 0))
pipe_top.anchor = ('center','top')
pipe_top.angle = 180
pipe_top._surf = pygame.transform.scale(pipe_top._surf, (pipe_top.width, HEIGHT))
pipe_top.height = HEIGHT
print(pipe_top.height)
pipe_bottom = Actor("pipe", pos=(WIDTH, HEIGHT))
pipe_bottom.anchor = ('center', 'top')
pipe_bottom._surf = pygame.transform.scale(pipe_bottom._surf, (pipe_bottom.width, HEIGHT))
bird.vy = 0
bird.dead = False
player_is_ready = False
pygame.font.init()
chinese_font = pygame.font.SysFont('kaiti', 40)
def reset_pipes():
    gap_half_height = GAP // 2
    gap_y = random.randint(gap_half_height, HEIGHT - gap_half_height)

    pipe_top.pos = (WIDTH, 0)
    top_height = gap_y - gap_half_height
    pipe_top.height = top_height

    bottom_y = gap_y + gap_half_height
    bottom_height = HEIGHT - bottom_y 
    pipe_bottom.pos = (WIDTH, bottom_y)
    pipe_bottom.height = bottom_height 
    #print(pipe_top.height, pipe_bottom.height, gap_y)
    #print("pos", top_height, gap_y, bottom_y)
    print("pos", pipe_top.height, gap_y, bottom_y, pipe_bottom.height)
    return

# 立即初始化管道位置
#reset_pipes()

def draw():
    screen.clear()
    screen.fill("skyblue")
    text_red = chinese_font.render("按下空格开始！", True, 'red')
    text_white = chinese_font.render("按下空格开始！", True, 'white')
    text_rext1 = text_red.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    text_rext2 = text_white.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.draw.text(f"Score: {SCORE}", center=(WIDTH // 2, 50), fontsize=40, color="white")
    
    if bird.dead:
        screen.draw.text("U R Dead!", center=(WIDTH // 2, HEIGHT // 2), fontsize=200, color="red")
        screen.blit(text_red, text_rext1)
        return
    if not player_is_ready:
        screen.blit(text_white, text_rext2)
    bird.draw()
    pipe_top.draw()
    pipe_bottom.draw()
    return

def update_pipes():
    pipe_top.left -= SPEED
    pipe_bottom.left -= SPEED
    if pipe_top.right < 0:
        global SCORE
        SCORE += 10
        reset_pipes() 
    return SCORE
def update_bird():
    bird.vy += GRAVITY
    bird.y += bird.vy
    if bird.colliderect(pipe_top) or bird.colliderect(pipe_bottom):
        bird.dead = True
        print(bird.pos, pipe_top.pos, pipe_bottom.pos)
        return
    if bird.y > HEIGHT or bird.y < 0:
        bird.dead = True
        print(bird.pos, pipe_top.pos, pipe_bottom.pos)
        return
    #print(bird.pos)
    return

def on_key_down():
    if keyboard.space:
        global SCORE, player_is_ready
        SCORE = 0
        bird.vy = 0
        bird.dead = False
        player_is_ready = True
        bird.y = HEIGHT // 2
        reset_pipes()
    elif not bird.dead:
        bird.vy = FLAP_VELOCITY
    return

def update():
    global player_is_ready, SCORE, SPEED
    if bird.dead or not player_is_ready:
        return
    if bird.dead:
        return
    SPEED = SCORE // 30 + 3
    update_pipes()
    update_bird()
    return

def main():
    pgzrun.go()
    return

if __name__ == "__main__":
    main()
    