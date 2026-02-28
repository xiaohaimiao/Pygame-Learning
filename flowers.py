import pygame
import math
import random

cell_size = 18

grid_x_count = 19
grid_y_count = 14

def reset():
    global grid
    global game_over
    global first_click

    grid = []

    for y in range(grid_y_count):
        grid.append([])
        for x in range(grid_x_count):
            grid[y].append({
                'flower': False,
                'state': 'covered', # 'covered', 'uncovered', 'flag', 'question'
            })

    game_over = False
    first_click = True

reset()

def get_surrounding_flower_count(x, y):
    surrounding_flower_count = 0

    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if (
                not (dy == 0 and dx == 0)
                and 0 <= (y + dy) < len(grid)
                and 0 <= (x + dx) < len(grid[y + dy])
                and grid[y + dy][x + dx]['flower']
            ):
                surrounding_flower_count += 1

    return surrounding_flower_count

def update():
    global selected_x
    global selected_y

    mouse_x, mouse_y = pygame.mouse.get_pos()
    selected_x = math.floor(mouse_x / cell_size)
    selected_y = math.floor(mouse_y / cell_size)

    if selected_x > grid_x_count - 1:
        selected_x = grid_x_count - 1
    if selected_y > grid_y_count - 1:
        selected_y = grid_y_count - 1

def on_key_down(key):
    reset()

def on_mouse_up(button):
    global game_over
    global first_click

    if not game_over:
        if button == mouse.LEFT and grid[selected_y][selected_x]['state'] != 'flag':
            if first_click:
                first_click = False

                possible_flower_positions = []

                for y in range(grid_y_count):
                    for x in range(grid_x_count):
                        if not (x == selected_x and y == selected_y):
                            possible_flower_positions.append({'x': x, 'y': y})

                for flower_index in range(40):
                    position = possible_flower_positions.pop(random.randrange(len(possible_flower_positions)))
                    grid[position['y']][position['x']]['flower'] = True

            if grid[selected_y][selected_x]['flower']:
                grid[selected_y][selected_x]['state'] = 'uncovered'
                game_over = True
            else:
                stack = [
                    {
                        'x': selected_x,
                        'y': selected_y,
                    }
                ]

                while len(stack) > 0:
                    current = stack.pop()
                    x = current['x']
                    y = current['y']

                    grid[y][x]['state'] = 'uncovered'

                    if get_surrounding_flower_count(x, y) == 0:
                        for dy in range(-1, 2):
                            for dx in range(-1, 2):
                                if (
                                    not (dy == 0 and dx == 0)
                                    and 0 <= (y + dy) < len(grid)
                                    and 0 <= (x + dx) < len(grid[y + dy])
                                    and grid[y + dy][x + dx]['state'] in ('covered', 'question')
                                ):
                                    stack.append({
                                        'x': x + dx,
                                        'y': y + dy,
                                    })

                complete = True

                for y in range(grid_y_count):
                    for x in range(grid_x_count):
                        if grid[y][x]['state'] != 'uncovered' and not grid[y][x]['flower']:
                            complete = False

                if complete:
                    game_over = True

        elif button == mouse.RIGHT:
            if grid[selected_y][selected_x]['state'] == 'covered':
                grid[selected_y][selected_x]['state'] = 'flag'
            elif grid[selected_y][selected_x]['state'] == 'flag':
                grid[selected_y][selected_x]['state'] = 'question'
            elif grid[selected_y][selected_x]['state'] == 'question':
                grid[selected_y][selected_x]['state'] = 'covered'

    else:
        reset()

def draw():
    screen.fill((0, 0, 0))

    for y in range(grid_y_count):
        for x in range(grid_x_count):

            def draw_cell(image, x, y):
                screen.blit(image, (x * cell_size, y * cell_size))

            if grid[y][x]['state'] == 'uncovered':
                draw_cell('uncovered', x, y)
            else:
                if x == selected_x and y == selected_y and not game_over:
                    if pygame.mouse.get_pressed()[0] == 1:
                        if grid[y][x]['state'] == 'flag':
                            draw_cell('covered', x, y)
                        else:
                            draw_cell('uncovered', x, y)
                    else:
                        draw_cell('covered_highlighted', x, y)
                else:
                    draw_cell('covered', x, y)

            surrounding_flower_count = 0

            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if (
                        not (dy == 0 and dx == 0)
                        and 0 <= (y + dy) < len(grid)
                        and 0 <= (x + dx) < len(grid[y + dy])
                        and grid[y + dy][x + dx]['flower']
                    ):
                        surrounding_flower_count += 1

            if grid[y][x]['flower'] and game_over:
                draw_cell('flower', x, y)
            elif get_surrounding_flower_count(x, y) > 0 and grid[y][x]['state'] == 'uncovered':
                draw_cell(str(get_surrounding_flower_count(x, y)), x, y)

            if grid[y][x]['state'] == 'flag':
                draw_cell('flag', x, y)
            elif grid[y][x]['state'] == 'question':
                draw_cell('question', x, y)

WIDTH = 18 * 19
HEIGHT = 18 * 14
