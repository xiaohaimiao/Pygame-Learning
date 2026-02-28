# pgzrun 05_flower.py
import random
import pgzrun
import os
import pygame
import math
from pgzero.builtins import Actor
os.environ["SDL_VIDEO_CENTERED"] = "1"

grid_x_count = 44
grid_y_count = 33
cell_size = 18
HEIGHT = cell_size * grid_y_count
WIDTH = cell_size * grid_x_count

def reset():

    """
    重置游戏网格状态
    初始化一个新的游戏网格，随机放置花朵
    """
    global grids  # 声明全局变量grids，以便在函数内部修改它
    grids = []
    for y in range(grid_y_count):
        grids.append([])
        for x in range(grid_x_count):
            grids[y].append({
                'flower': False,
                'state': 'covered', # 'covered', 'uncovered'
            })

    possible_flower_positions = []

    for y in range(grid_y_count):
        for x in range(grid_x_count):
            possible_flower_positions.append({'x': x, 'y': y})

    for flower_index in range(200):
        position = possible_flower_positions.pop(random.randrange(len(possible_flower_positions)))
        grids[position['y']][position['x']]['flower'] = True
    return

reset()
def draw():
    """
    绘制游戏主界面的函数
    负责渲染整个游戏网格，包括单元格的状态、覆盖情况、花朵数量等信息
    """
    screen.fill((0, 0, 0))
    for y in range(grid_y_count):
        for x in range(grid_x_count):
            def draw_cell(image, x, y):
                screen.blit(image, (x * cell_size, y * cell_size))
            
            # 如果格子已经被消除，跳过绘制
            if grids[y][x]['state'] == 'eliminated':
                draw_cell('uncovered', x, y)
                
            # 如果格子是未覆盖状态
            if grids[y][x]['state'] == 'uncovered':
                draw_cell('uncovered', x, y)
            else:
                # 处理选中的格子
                if x == selected_x and y == selected_y:
                    if pygame.mouse.get_pressed()[0] == 1:
                        draw_cell('uncovered', x, y)
                        grids[y][x]['state'] == 'eliminated'
                    else:
                        draw_cell('covered_highlighted', x, y)
                else:
                    draw_cell('covered', x, y)

            # 绘制花朵（如果存在）
            if grids[y][x]['flower']:
                draw_cell('flower', x, y)

            # 计算并显示周围花朵数量
            surrounding_flower_count = 0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if not (dy == 0 and dx == 0):
                        if (0 <= (y + dy) < len(grids) and 
                            0 <= (x + dx) < len(grids[y + dy]) and 
                            grids[y + dy][x + dx]['flower']):
                            surrounding_flower_count += 1

            if not grids[y][x]['flower'] and surrounding_flower_count > 0:
                draw_cell(str(surrounding_flower_count), x, y)

def on_mouse_up(button):
    if button == mouse.LEFT:
        grids[selected_y][selected_x]['state'] = 'uncovered'


def update():

    """
    更新选中单元格的坐标函数
    该函数获取鼠标位置，将其转换为网格坐标，并进行边界检查
    """
    global selected_x  # 声明全局变量selected_x
    global selected_y  # 声明全局变量selected_y

    mouse_x, mouse_y = pygame.mouse.get_pos()  # 获取鼠标在屏幕上的坐标位置
    # 将鼠标坐标转换为网格坐标，使用地板除法确保得到整数索引
    selected_x = math.floor(mouse_x / cell_size)
    selected_y = math.floor(mouse_y / cell_size)
    # 检查并修正selected_x是否超出网格边界
    if selected_x > grid_x_count - 1:
        selected_x = grid_x_count - 1
    # 检查并修正selected_y是否超出网格边界
    if selected_y > grid_y_count - 1:
        selected_y = grid_y_count - 1
    return  # 函数结束，无返回值



def on_key_down(key):
    reset()
