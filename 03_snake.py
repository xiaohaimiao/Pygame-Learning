# -*- coding: utf-8 -*-
# pgzrun snake.py
# V1.0 完成基本功能
    # TODO:
    # V1.1 死亡提示
    # V1.2 得分
    # V1.3 边界死亡开关
    # V1.4 颜色优化
    # V2.0 双人！

import random
import pgzrun
import os
import pygame
from pgzero.builtins import Actor
os.environ['SDL_VIDEO_CENTERED'] = '1'
Cell_size = 50
Grid_x_count = 40
Grid_y_count = 20
WIDTH = Grid_x_count * Cell_size
HEIGHT = Grid_y_count * Cell_size
Timer = 0
Interval = 0.1

direction_queue = ["right"]
snake_segments = [
        {"x": 2, "y": 0},
        {"x": 1, "y": 0},
        {"x": 0, "y": 0},
    ]
Score = 0
Is_snake_dead = False
player_is_ready = False
food_position = {
    "x": random.randint(0, Grid_x_count - 1),
    "y": random.randint(0, Grid_y_count - 1),
}
pygame.font.init()
chinese_font = pygame.font.SysFont('kaiti', 40)
chinese_font2 = pygame.font.SysFont('kaiti', 150)
def draw():
    screen.fill((0, 0, 0))
    screen.draw.filled_rect(
        Rect(
            0, 0,
            Grid_x_count * Cell_size, Grid_y_count * Cell_size
        ),
        color=(70, 70, 70)
    )
    for segment in snake_segments:
        screen.draw.filled_rect(
            Rect(
                segment["x"] * Cell_size, segment["y"] * Cell_size,
                Cell_size - 1, Cell_size - 1
            ),
            color=(165, 255, 81)
        )
    screen.draw.filled_rect(
        Rect(
            food_position["x"] * Cell_size, food_position["y"] * Cell_size,
            Cell_size - 1, Cell_size - 1
        ),
        color=(255, 76, 76)
    )
    text_red = chinese_font.render("按下空格开始！", True, 'red')
    text_red2 = chinese_font2.render("蛇被你创死了！", True, 'red')
    text_white = chinese_font.render("按下空格开始！", True, 'white')
    text_rext1 = text_red.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    text_rext2 = text_white.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    text_rext3 = text_red2.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.draw.text(f"Score: {Score}", center=(WIDTH // 2, 50), fontsize=40, color="white")
    
    if Is_snake_dead:
        screen.blit(text_red2, text_rext3)
        screen.blit(text_red, text_rext1)
        for segment in snake_segments:
            screen.draw.filled_rect(
                Rect(
                    segment["x"] * Cell_size, segment["y"] * Cell_size,
                    Cell_size - 1, Cell_size - 1
                ),
                color=(10, 10, 10)
            )
        return
    if not player_is_ready:
        screen.blit(text_white, text_rext2)
    return

def move_food():
    global food_position
    possible_food_positions = []
    for food_x in range(Grid_x_count):
        for food_y in range(Grid_y_count):
            possible = True
            for segment in snake_segments:
                if food_x == segment["x"] and food_y == segment["y"]:
                    possible = False
            if possible:
                possible_food_positions.append({"x": food_x, "y": food_y})
    food_position = random.choice(possible_food_positions)
    return

def update(dt):
    global Timer, Interval, food_position, Is_snake_dead
    if Is_snake_dead or not player_is_ready:
        return

    next_x_position = snake_segments[0]["x"]
    next_y_position = snake_segments[0]["y"]
    Timer += dt
    if Timer >= Interval:
        Timer = 0
        if len(direction_queue) > 1:
            direction_queue.pop(0)
            
        # 更新位置
        if direction_queue[0] == "right":
            next_x_position += 1
            if next_x_position >= Grid_x_count:
                next_x_position = 0
        elif direction_queue[0] == "left":
            next_x_position -= 1
            if next_x_position < 0:
                next_x_position = Grid_x_count - 1
        elif direction_queue[0] == "down":
            next_y_position += 1
            if next_y_position >= Grid_y_count:
                next_y_position = 0
        elif direction_queue[0] == "up":
            next_y_position -= 1
            if next_y_position < 0:
                next_y_position = Grid_y_count - 1
            
        # 检查碰撞
        for segment in snake_segments[:-1]:
            if next_x_position == segment["x"] and next_y_position == segment["y"]:
                Is_snake_dead = True
                return
                
        if not Is_snake_dead:
            snake_segments.insert(0, {"x": next_x_position, "y": next_y_position})
            if (snake_segments[0]["x"] == food_position["x"]
            and snake_segments[0]["y"] == food_position["y"]):
                global Score
                Score += 1
                move_food()
            else:
                snake_segments.pop()


def on_key_down(key):
    global player_is_ready, Is_snake_dead
    if (not player_is_ready or Is_snake_dead) and keyboard.space:
        global direction_queue, snake_segments, Score
        direction_queue = ["right"]
        snake_segments = [
        {"x": 2, "y": 0},
        {"x": 1, "y": 0},
        {"x": 0, "y": 0},
        ]
        Score = 0
        Is_snake_dead = False
        player_is_ready = True
    if (key == keys.RIGHT
    and direction_queue[-1] != "right"
    and direction_queue[-1] != "left"):
        direction_queue.append("right")

    elif (key == keys.LEFT
    and direction_queue[-1] != "left"
    and direction_queue[-1] != "right"):
        direction_queue.append("left")

    elif (key == keys.DOWN
    and direction_queue[-1] != "down"
    and direction_queue[-1] != "up"):
        direction_queue.append("down")

    elif (key == keys.UP
    and direction_queue[-1] != "up"
    and direction_queue[-1] != "down"):
        direction_queue.append("up")

def main():
    pgzrun.go()
    return

if __name__ == "__main__":
    main()