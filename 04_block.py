#pgzrun block.py
# V1.0 基本功能
# V1.1 结束语
# V1.2 分数，关卡
# V1.3 预展
# TODO:
#       V1.4 音效
#       V1.5 预瞄
#       V1.6 网格

import random
import pgzrun
import os
import pygame
from pgzero.builtins import Actor
os.environ["SDL_VIDEO_CENTERED"] = "1"

piece_structures = [
    [
        [
            [" ", " ", " ", " "],
            ["i", "i", "i", "i"],
            [" ", " ", " ", " "],
            [" ", " ", " ", " "],
        ],
        [
            [" ", "i", " ", " "],
            [" ", "i", " ", " "],
            [" ", "i", " ", " "],
            [" ", "i", " ", " "],
        ],
    ],
    [
        [
            [" ", " ", " ", " "],
            [" ", "o", "o", " "],
            [" ", "o", "o", " "],
            [" ", " ", " ", " "],
        ],
    ],
    [
        [
            [" ", " ", " ", " "],
            ["j", "j", "j", " "],
            [" ", " ", "j", " "],
            [" ", " ", " ", " "],
        ],
        [
            [" ", "j", " ", " "],
            [" ", "j", " ", " "],
            ["j", "j", " ", " "],
            [" ", " ", " ", " "],
        ],
        [
            ["j", " ", " ", " "],
            ["j", "j", "j", " "],
            [" ", " ", " ", " "],
            [" ", " ", " ", " "],
        ],
        [
            [" ", "j", "j", " "],
            [" ", "j", " ", " "],
            [" ", "j", " ", " "],
            [" ", " ", " ", " "],
        ],
    ],
    [
        [
            [" ", " ", " ", " "],
            ["l", "l", "l", " "],
            ["l", " ", " ", " "],
            [" ", " ", " ", " "],
        ],
        [
            [" ", "l", " ", " "],
            [" ", "l", " ", " "],
            [" ", "l", "l", " "],
            [" ", " ", " ", " "],
        ],
        [
            [" ", " ", "l", " "],
            ["l", "l", "l", " "],
            [" ", " ", " ", " "],
            [" ", " ", " ", " "],
        ],
        [
            ["l", "l", " ", " "],
            [" ", "l", " ", " "],
            [" ", "l", " ", " "],
            [" ", " ", " ", " "],
        ],
    ],
    [
        [
            [" ", " ", " ", " "],
            ["t", "t", "t", " "],
            [" ", "t", " ", " "],
            [" ", " ", " ", " "],
        ],
        [
            [" ", "t", " ", " "],
            [" ", "t", "t", " "],
            [" ", "t", " ", " "],
            [" ", " ", " ", " "],
        ],
        [
            [" ", "t", " ", " "],
            ["t", "t", "t", " "],
            [" ", " ", " ", " "],
            [" ", " ", " ", " "],
        ],
        [
            [" ", "t", " ", " "],
            ["t", "t", " ", " "],
            [" ", "t", " ", " "],
            [" ", " ", " ", " "],
        ],
    ],
    [
        [
            [" ", " ", " ", " "],
            [" ", "s", "s", " "],
            ["s", "s", " ", " "],
            [" ", " ", " ", " "],
        ],
        [
            ["s", " ", " ", " "],
            ["s", "s", " ", " "],
            [" ", "s", " ", " "],
            [" ", " ", " ", " "],
        ],
    ],
    [
        [
            [" ", " ", " ", " "],
            ["z", "z", " ", " "],
            [" ", "z", "z", " "],
            [" ", " ", " ", " "],
        ],
        [
            [" ", "z", " ", " "],
            ["z", "z", " ", " "],
            ["z", " ", " ", " "],
            [" ", " ", " ", " "],
        ],
    ],
]
def new_sequence():
    global sequence

    sequence = list(range(len(piece_structures)))
    random.shuffle(sequence)

def new_pieces():
    global sequence, Piece_x, Piece_y, Piece_type, Piece_rotation, next_piece_type
    Piece_x = 3
    Piece_y = -1
    if len(sequence) == 0:
        new_sequence()
    Piece_type = next_piece_type if next_piece_type is not None else sequence.pop()
    next_piece_type = sequence.pop() if sequence else sequence[0]
    Piece_rotation = 0
    return

def reset():
    global inert, timer, score, level, lines_cleared, next_piece_type
    inert = []
    for y in range(Grid_y_count):
        inert.append([" "] * Grid_x_count)
    timer = 0
    score = 0
    level = 1
    lines_cleared = 0
    next_piece_type = None
    new_sequence()
    new_pieces()
    return


score = 0
level = 1
lines_cleared = 0
Block_size = 20
Grid_x_count = 10
Grid_y_count = 18
WIDTH = 1950
HEIGHT = 1000
Piece_type = 2
Piece_rotation = 0      
Piece_x = 3
Piece_y = -1
Piece_count_x = 4
Piece_count_y = 4
timer = 0
timer_limit = 0.5
sequence = []
is_game_over = False
is_player_ready = False
next_piece_type = None

reset()
pygame.font.init()
chinese_font = pygame.font.SysFont("kaiti", 40)
chinese_font2 = pygame.font.SysFont("kaiti", 100)

def draw_block(block, x, y):
    colors = {
        " ": (222, 222, 222),
        "i": (120, 195, 239),
        "j": (236, 231, 108),
        "l": (124, 218, 193),
        "o": (234, 177, 121),
        "s": (211, 136, 236),
        "t": (248, 147, 196),
        "z": (169, 221, 118),
        "preview": (255, 255, 255),
    }
    block_draw_size = Block_size - 1
    colour = colors[block]
    screen.draw.filled_rect(
        Rect(
            x * Block_size + 800, y * Block_size + 350,
            block_draw_size, block_draw_size
        ),
        color=colour
    )
    return


def draw():
    text_red = chinese_font.render("按下空格重开！", True, "red")
    text_red2 = chinese_font2.render("你突破了人类第一伦理!", True, "red")
    text_red3 = chinese_font2.render("恶 魔 立 方", True, "red")
    text_green = chinese_font.render("按下空格开始！", True, "green")
    text_rext1 = text_red.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    text_rext2 = text_green.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    text_rext3 = text_red2.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    text_rext4 = text_red3.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    screen.fill((0, 0, 0))
    if not is_player_ready:
        screen.blit(text_green, text_rext2)
        screen.blit(text_red3, text_rext4)
        return
    if is_game_over:
        screen.blit(text_red2, text_rext3)
        screen.blit(text_red, text_rext1)
        return
    
    
    score_text = chinese_font.render(f"分数: {score}", True, "white")
    level_text = chinese_font.render(f"关卡: {level}", True, "white")
    screen.blit(score_text, (50, 50))
    screen.blit(level_text, (50, 100))
    
    for y in range(Grid_y_count):
        for x in range(Grid_x_count):
            draw_block(inert[y][x], x, y)  # 不再传递 y2

    # 计算预览位置 y2
    y2 = Piece_y
    while can_piece_move(Piece_x, y2 + 1, Piece_rotation):
        y2 += 1

    # 绘制预览边框（绿色）
    for y in range(4):
        for x in range(4):
            block = piece_structures[Piece_type][Piece_rotation][y][x]
            if block != " ":
                # 绘制预览位置的边框
                pygame.draw.rect(
                    screen.surface,
                    (250, 0, 0),  # 绿色
                    (
                        (x + Piece_x) * Block_size + 800,
                        (y + y2) * Block_size + 350,  # 使用 y2 作为预览位置
                        Block_size - 1,
                        Block_size - 1
                    ),
                    3  # 边框宽度
                )

    # 绘制当前方块（填充矩形）
    for y in range(4):
        for x in range(4):
            block = piece_structures[Piece_type][Piece_rotation][y][x]
            if block != " ":
                draw_block(block, x + Piece_x, y + Piece_y)  # 不再传递 y2
    if next_piece_type is not None:
        for y in range(Piece_count_y):
            for x in range(Piece_count_x):
                block = piece_structures[next_piece_type][0][y][x]
                if block != " ":
                    draw_block("preview", x + 15, y + 2) 
                #draw_block("preview", x + 3, y - 6)
    return

def can_piece_move(test_x, test_y, test_rotation):
    for y in range(Piece_count_y):
        for x in range(Piece_count_x):
            test_block_x = test_x + x
            test_block_y = test_y + y

            if (
                piece_structures[Piece_type][test_rotation][y][x] != " " and (
                    test_block_x < 0
                    or test_block_x >= Grid_x_count
                    or test_block_y >= Grid_y_count
                    or inert[test_block_y][test_block_x] != " "
                )
            ):
                return False

    return True

def update(dt):
    global timer, timer_limit, Piece_x, Piece_y, Piece_rotation, Piece_type, is_game_over, score, level, lines_cleared
    if not is_player_ready or is_game_over:
        return
    timer += dt
    if timer >= timer_limit:
        timer = 0
        test_y = Piece_y + 1
        if can_piece_move(Piece_x, test_y, Piece_rotation):
            Piece_y = test_y
        else:
            for y in range(Piece_count_y):
                for x in range(Piece_count_x):
                    block = piece_structures[Piece_type][Piece_rotation][y][x]
                    if block != " ":
                        inert[Piece_y + y][Piece_x + x] = block

            for y in range(Grid_y_count):
                complete = True
                for x in range(Grid_x_count):
                    if inert[y][x] == " ":
                        complete = False
                        break

                if complete:
                    lines_cleared += 1
                    score += 100 * level
                    if lines_cleared % 5 == 0:
                        level += 1
                        timer_limit = max(0.1, 0.5 - (level - 1) * 0.05)
                    for ry in range(y, 1, -1):
                        for rx in range(Grid_x_count):
                            inert[ry][rx] = inert[ry - 1][rx]

                    for rx in range(Grid_x_count):
                        inert[0][rx] = " "

            new_pieces()

            if not can_piece_move(Piece_x, Piece_y, Piece_rotation):
                is_game_over = True
    return

def on_key_down(key):
    global Piece_rotation, piece_structures, Piece_type, Piece_x, Piece_y, timer, is_game_over, is_player_ready, next_piece_type
    if key == keys.SPACE and (not is_player_ready or is_game_over):
        is_player_ready = True
        is_game_over = False
        next_piece_type = None
        reset()
    
    if is_game_over or not is_player_ready:
        return
    """
    if key == keys.X:
        #print("X key pressed")  # 调试用
        text_rotation = Piece_rotation + 1
        if text_rotation > len(piece_structures[Piece_type]) - 1:
            text_rotation = 0
        if can_piece_move(Piece_x, Piece_y, text_rotation):
            Piece_rotation = text_rotation
        #print(f"New rotation: {Piece_rotation}")  # 调试用
        
    elif key == keys.Z:
        #print("Z key pressed")  # 调试用
        text_rotation = Piece_rotation - 1
        if text_rotation < 0:
            text_rotation = len(piece_structures[Piece_type]) - 1
        if can_piece_move(Piece_x, Piece_y, text_rotation):
            Piece_rotation = text_rotation
        #print(f"New rotation: {Piece_rotation}")  # 调试用

    elif key == keys.C:
        while can_piece_move(Piece_x, Piece_y + 1, Piece_rotation):
            Piece_y += 1
            timer = timer_limit
    """
    if key == keys.UP:
        text_rotation = Piece_rotation + 1
        if text_rotation > len(piece_structures[Piece_type]) - 1:
            text_rotation = 0
        if can_piece_move(Piece_x, Piece_y, text_rotation):
            Piece_rotation = text_rotation
    elif key == keys.DOWN:
        while can_piece_move(Piece_x, Piece_y + 1, Piece_rotation):
            Piece_y += 1
            timer = timer_limit
    elif key == keys.LEFT:
        text_x = Piece_x - 1
        if can_piece_move(text_x, Piece_y, Piece_rotation):
            Piece_x = text_x
    elif key == keys.RIGHT:
        text_x = Piece_x + 1
        if can_piece_move(text_x, Piece_y, Piece_rotation):
            Piece_x = text_x
    

def main():
    pygame.init()
    pgzrun.go()
    return

if __name__ == "__main__":
    main()