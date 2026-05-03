# pgzrun 06_fifteen.py
import random
import pgzrun
import os
import pygame
import math
import time
from pgzero.builtins import Actor

os.environ["SDL_VIDEO_CENTERED"] = "1"

WIDTH = 400
HEIGHT = 400
grid_x_count = 4
grid_y_count = 4
pieces_size = 100

# 全局变量初始化
grid = []
is_win = False
start_time = 0
elapsed_time = 0
timer_started = False

def rest():
    global grid, is_win, start_time, elapsed_time, timer_started, is_break
    is_break = False
    start_time = 0
    elapsed_time = 0
    timer_started = False
    is_win = False
    grid = []
    for y in range(grid_y_count):
        grid.append([])
        for x in range(grid_x_count):
            grid[y].append(y * grid_x_count + x + 1)
    # 随机打乱
    for move_number in range(1000):
        move(random.choice(('down', 'up', 'right', 'left')))
    for move_number in range(grid_x_count - 1):
        move('left')
    for move_number in range(grid_y_count - 1):
        move('up')

def update():
    # 这个函数确保游戏循环持续运行，即使没有按键事件
    global is_break
    if is_break:
        rest()
    pass

def draw():
    global elapsed_time  # 声明使用全局变量
    screen.fill((0, 0, 0))

    for x in range(grid_x_count):
        for y in range(grid_y_count):
            if grid[y][x] == grid_x_count * grid_y_count:
                continue
            pieces_draw_size = pieces_size - 2
            screen.draw.filled_rect(
                Rect(
                    x * pieces_size, 
                    y * pieces_size,
                    pieces_draw_size, 
                    pieces_draw_size
                ),
                color=(100, 20, 150)
            )
            screen.draw.text(
                str(grid[y][x]),
                (x * pieces_size + 35, y * pieces_size + 20), # 调整文字位置使其居中
                fontsize=60
            )
            
    # 显示计时器
    if timer_started and not is_win:
        elapsed_time = int(time.time() - start_time)
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    screen.draw.text(f"{minutes:02d}:{seconds:02d}", 
                    (WIDTH - 100, 10), 
                    fontsize=30, 
                    color="red")
    # 检查是否胜利
    if is_win:
        screen.draw.text("YOU WIN!", (150, 180), fontsize=50, color="white")
        screen.draw.text("press 'space' to play again!", (270, 150), fontsize=20, color="red")
        return
    return

def move(direction):
    # 找到空白格的位置
    empty_x, empty_y = -1, -1
    for y in range(grid_y_count):
        for x in range(grid_x_count):
            if grid[y][x] == grid_x_count * grid_y_count:
                empty_x = x
                empty_y = y
                break
        if empty_x != -1:
            break

    new_empty_y = empty_y
    new_empty_x = empty_x

    if direction == 'down':
        new_empty_y += 1
    elif direction == 'up':
        new_empty_y -= 1
    elif direction == 'right':
        new_empty_x += 1
    elif direction == 'left':
        new_empty_x -= 1

    if (
        0 <= new_empty_y < grid_y_count and
        0 <= new_empty_x < grid_x_count
    ):
        # 交换空白格和目标格
        grid[empty_y][empty_x], grid[new_empty_y][new_empty_x] = grid[new_empty_y][new_empty_x], grid[empty_y][empty_x]
    return

def check_win():
    global is_win
    is_win = True
    for y in range(grid_y_count):
        for x in range(grid_x_count):
            if grid[y][x] != y * grid_x_count + x + 1:
                is_win = False
                return

def on_key_down(key):
    global timer_started, start_time, is_ready, is_break # 声明使用全局变量
    
    # 如果计时器还没开始，第一次移动时开始计时
    if not timer_started:
        timer_started = True
        start_time = time.time()

    if not is_break and is_win and key == keys.SPACE:
        is_break = True

    if key == keys.DOWN:
        move('down')
    elif key == keys.UP:
        move('up')
    elif key == keys.RIGHT:
        move('right')
    elif key == keys.LEFT:
        move('left')
    
    # 移动后检查胜利
    check_win()
    return

# 初始化游戏
rest()


# 启动游戏
pgzrun.go()
