# pgzrun 05_flower.py
# V1.0 基础功能
# V1.1 地雷数量
# V1.2 中键
# V1.3 计时
import random
import pgzrun
import os
import pygame
import math
import time
from pgzero.builtins import Actor
os.environ["SDL_VIDEO_CENTERED"] = "1"  # 移除了多余的 ]

grid_x_count = 44
grid_y_count = 33
cell_size = 18
is_game_over = False
is_player_ready = False
HEIGHT = cell_size * grid_y_count
WIDTH = cell_size * grid_x_count

# 初始化选中的格子坐标
selected_x = 0
selected_y = 0

# 计时器相关变量
start_time = 0
elapsed_time = 0
timer_started = False

def reset():
    """
    重置游戏网格状态，随机放置花朵
    """
    global grids, start_time, elapsed_time, timer_started, is_game_over, flowers_number  # 声明使用全局变量
    # 重置计时器
    start_time = 0
    elapsed_time = 0
    timer_started = False
    is_game_over = False
    flowers_number = 200
    
    # 初始化空网格
    grids = []
    for y in range(grid_y_count):
        grids.append([])  # 为每一行创建一个空列表
        for x in range(grid_x_count):
            # 为每个格子添加初始状态
            grids[y].append({
                'flower': False,  # 是否有花朵
                'state': 'covered',  # 格子状态（初始为未翻开）
            })

    # 创建所有可能的花朵位置列表
    possible_flower_positions = []
    for y in range(grid_y_count):
        for x in range(grid_x_count):
            possible_flower_positions.append({'x': x, 'y': y})

    # 随机在170个位置放置花朵
    for flower_index in range(flowers_number):
        # 从剩余位置中随机选择一个位置
        position = possible_flower_positions.pop(random.randrange(len(possible_flower_positions)))
        # 在选定位置放置花朵
        grids[position['y']][position['x']]['flower'] = True

reset()

def check_victory():
    """
    检查是否所有非地雷格子都被揭开
    Returns:
        bool: 如果所有非地雷格子都被揭开返回True，否则返回False
    """
    for y in range(grid_y_count):
        for x in range(grid_x_count):
            if not grids[y][x]['flower'] and grids[y][x]['state'] != 'uncovered':
                return False
    return True

def draw():
    global elapsed_time, flowers_number
    screen.fill((0, 0, 0))
    for y in range(grid_y_count):
        for x in range(grid_x_count):
            def draw_cell(image, x, y):
                screen.blit(image, (x * cell_size, y * cell_size))

            # 绘制基础格子状态
            if grids[y][x]['state'] == 'uncovered':
                draw_cell('uncovered', x, y)
            else:
                if x == selected_x and y == selected_y:
                    if pygame.mouse.get_pressed()[0] == 1:
                        if grids[y][x]['state'] == 'flag':
                            draw_cell('covered', x, y)
                        else:
                            draw_cell('uncovered', x, y)
                    else:
                        draw_cell('covered_highlighted', x, y)
                else:
                    draw_cell('covered', x, y)

            # 绘制花朵和数字（只在uncovered状态下）
            if grids[y][x]['state'] == 'uncovered':
                if grids[y][x]['flower']:
                    draw_cell('flower', x, y)
                else:
                    count = get_surrounding_flower_count(x, y)
                    if count > 0:
                        draw_cell(str(count), x, y)

            # 绘制标记
            if grids[y][x]['state'] == 'flag':
                draw_cell('flag', x, y)
            elif grids[y][x]['state'] == 'question':
                draw_cell('question', x, y)

    # 显示计时器
    if timer_started and not is_game_over:
        elapsed_time = int(time.time() - start_time)
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    screen.draw.text(f"{minutes:02d}:{seconds:02d}", 
                    (WIDTH - 100, 10), 
                    fontsize=30, 
                    color="red")

    screen.draw.text(f"Flowers: {flowers_number}", 
                    (WIDTH - 125, 30),  # 增加了垂直间距
                    fontsize=30, 
                    color="red")


    # 显示游戏状态信息
    if is_game_over:
        # 检查是否胜利
        if check_victory():
            screen.draw.text("Victory!", center=(WIDTH/2, HEIGHT/2), fontsize=60, color="green")
        else:
            screen.draw.text("Game Over!", center=(WIDTH/2, HEIGHT/2), fontsize=60, color="red")

def get_surrounding_flower_count(x, y):
    count = 0
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if (not (dy == 0 and dx == 0) and
                0 <= (y + dy) < len(grids) and
                0 <= (x + dx) < len(grids[y + dy]) and
                grids[y + dy][x + dx]['flower']):
                count += 1
    return count

def on_mouse_up(button):
    """
    处理鼠标释放事件，处理游戏中的点击操作
    Args:
        button: 鼠标按键类型（左键、中键或右键）
    """
    global is_game_over, start_time, timer_started, flowers_number# 声明使用全局变量

    if not is_game_over:
        # 第一次点击时启动计时器
        if not timer_started:
            timer_started = True
            start_time = time.time()

        if button == mouse.LEFT and grids[selected_y][selected_x]['state'] != 'flag':
            if grids[selected_y][selected_x]['flower']:
                # 当点击到雷时，显示所有雷（但保留旗子标记）
                for y in range(grid_y_count):
                    for x in range(grid_x_count):
                        if grids[y][x]['flower']:
                            # 只有未插旗的雷才显示
                            if grids[y][x]['state'] != 'flag':
                                grids[y][x]['state'] = 'uncovered'
                is_game_over = True
            else:
                stack = [{'x': selected_x, 'y': selected_y}]
                while len(stack) > 0:
                    current = stack.pop()
                    x = current['x']
                    y = current['y']
                    if grids[y][x]['state'] != 'uncovered':
                        grids[y][x]['state'] = 'uncovered'
                        if get_surrounding_flower_count(x, y) == 0:
                            for dy in range(-1, 2):
                                for dx in range(-1, 2):
                                    if (not (dy == 0 and dx == 0) and
                                        0 <= (y + dy) < len(grids) and
                                        0 <= (x + dx) < len(grids[y + dy]) and
                                        grids[y + dy][x + dx]['state'] in ('covered', 'question')):
                                        stack.append({'x': x + dx, 'y': y + dy})
                
                # 检查是否获胜
                if check_victory():
                    is_game_over = True

        # 右键点击处理
        if button == mouse.RIGHT:
            if grids[selected_y][selected_x]['state'] == 'covered':
                grids[selected_y][selected_x]['state'] = 'flag'
                flowers_number -= 1
            elif grids[selected_y][selected_x]['state'] == 'flag':
                grids[selected_y][selected_x]['state'] = 'question'
                flowers_number += 1
            elif grids[selected_y][selected_x]['state'] == 'question':
                grids[selected_y][selected_x]['state'] = 'covered'
        
        # 中键点击处理
        if button == mouse.MIDDLE:
            if grids[selected_y][selected_x]['state'] == 'covered':
                grids[selected_y][selected_x]['state'] = 'question'
            elif grids[selected_y][selected_x]['state'] == 'question':
                grids[selected_y][selected_x]['state'] = 'flag'
                flowers_number -= 1
            elif grids[selected_y][selected_x]['state'] == 'flag':
                grids[selected_y][selected_x]['state'] = 'covered'
                flowers_number += 1
def update():
    global selected_x, selected_y
    mouse_x, mouse_y = pygame.mouse.get_pos()
    selected_x = math.floor(mouse_x / cell_size)
    selected_y = math.floor(mouse_y / cell_size)
    
    # 边界检查
    selected_x = max(0, min(selected_x, grid_x_count - 1))
    selected_y = max(0, min(selected_y, grid_y_count - 1))

def on_key_down(key):
    if is_game_over:
        reset()
