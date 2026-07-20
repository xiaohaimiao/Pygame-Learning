import sys
import os

# ====== Pyinstaller 打包 pgzero 修复代码 (必须放在最顶部) ======
import pgzero.game
pgzero.game.show_default_icon = lambda: None

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    font_path = os.path.join(base_path, 'pgzero', 'data', 'font', 'SourceSansPro-Regular.otf')
    if os.path.exists(font_path):
        pgzero.game.font_name = font_path

import random
import pgzrun
import pygame
import math
from pgzero.builtins import Actor
from pgzero.keyboard import keys

os.environ["SDL_VIDEO_CENTERED"] = "1"
WIDTH = 1960
HEIGHT = 1080

# 初始化 Pygame 字体模块并加载支持中文的楷体字体
pygame.font.init()
chinese_font = pygame.font.SysFont("kaiti", 40)
num_font = pygame.font.SysFont("kaiti", 36)

# 统一棋盘数据结构：[颜色, 种类, 状态, 编号, 血量(第5), 近战伤害(第6), 远程伤害(第7)]
board = [
    [['w', 'N', 'n', 1, 500, 100, 60], ['w', 'B', 'n', 1, 100, 70, 60], ['w', 'R', 'n', 1, 70, 70, 120], ['w', 'K', 'n', 1, 400, 300, 200], ['w', 'Q', 'n', 1, 130, 100, 60], ['w', 'R', 'n', 2, 70, 70, 120], ['w', 'B', 'n', 2, 100, 70, 60], ['w', 'N', 'n', 2, 500, 100, 60]], 
    [['w', 'P', 'n', 1, 80, 60, 40], ['w', 'P', 'n', 2, 80, 60, 40], ['w', 'P', 'n', 3, 80, 60, 40], ['w', 'P', 'n', 4, 80, 60, 40], ['w', 'P', 'n', 5, 80, 60, 40], ['w', 'P', 'n', 6, 80, 60, 40], ['w', 'P', 'n', 7, 80, 60, 40], ['w', 'P', 'n', 8, 80, 60, 40]], 
    [['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0]], 
    [['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0]], 
    [['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0]], 
    [['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0], ['n', 'N', 'n', 0, 0, 0, 0]], 
    [['b', 'P', 'n', 1, 80, 60, 40], ['b', 'P', 'n', 2, 80, 60, 40], ['b', 'P', 'n', 3, 80, 60, 40], ['b', 'P', 'n', 4, 80, 60, 40], ['b', 'P', 'n', 5, 80, 60, 40], ['b', 'P', 'n', 6, 80, 60, 40], ['b', 'P', 'n', 7, 80, 60, 40], ['b', 'P', 'n', 8, 80, 60, 40]],
    [['b', 'N', 'n', 1, 500, 100, 60], ['b', 'B', 'n', 1, 100, 70, 60], ['b', 'R', 'n', 1, 70, 70, 120], ['b', 'K', 'n', 1, 400, 300, 200], ['b', 'Q', 'n', 1, 130, 100, 60], ['b', 'R', 'n', 2, 70, 70, 120], ['b', 'B', 'n', 2, 100, 70, 60], ['b', 'N', 'n', 2, 500, 100, 60]]
]

pieces_draw_size = 120
chess_draw_size = 50

selected_pos = None
current_turn = 'w'

# 棋子种类代码到中文名的映射表
piece_names = {
    'K': '王',
    'Q': '后',
    'N': '车',
    'R': '象',
    'B': '马',
    'P': '兵'
}

# 定义兵种显示的优先级顺序
piece_order = {'K': 0, 'Q': 1, 'N': 2, 'R': 3, 'B': 4, 'P': 5}

# ================= 属性更新逻辑 =================

def update_piece_stats():
    """实时更新所有存活棋子的伤害属性"""
    for row in range(8):
        for col in range(8):
            cell = board[row][col]
            color = cell[0]
            kind = cell[1]
            
            if color == 'n':
                continue
                
            health = cell[4]
            
            # 根据不同兵种和血量实时修改伤害
            if kind == "Q":
                if health <= 80:
                    cell[5], cell[6] = 60, 40
                elif health <= 160:
                    cell[5], cell[6] = 120, 80
                elif health <= 240:
                    cell[5], cell[6] = 180, 120
                else:
                    cell[5], cell[6] = 240, 160
            # 如果以后需要给其他兵种加类似判定，可以在这里加 elif kind == "K": ...

# ================= 棋子移动与攻击规则提取函数 =================

def get_king_moves(row, col, color):
    moves = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0: continue
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_color = board[r][c][0]
                if target_color == 'n' or target_color != color:
                    moves.append((r, c, [(r, c)]))
    return moves

def get_queen_moves(row, col, color):
    """后的移动与攻击逻辑（已移除伤害修改逻辑）"""
    moves = []
    for dr, dc in [[-1,0],[1,0],[0,-1],[0,1],[-1,-1],[-1,1],[1,-1],[1,1]]:
        path = []
        for i in range(1, 8):
            r, c = row + dr*i, col + dc*i
            if 0 <= r < 8 and 0 <= c < 8:
                target_color = board[r][c][0]
                path.append((r, c))
                if target_color == 'n':
                    moves.append((r, c, list(path)))
                elif target_color != color:
                    moves.append((r, c, list(path)))
                    break
                else:
                    break
            else:
                break
    return moves

def get_rook_moves(row, col, color):
    moves = []
    for dr, dc in [[-1,0],[1,0],[0,-1],[0,1]]:
        path = []
        for i in range(1, 8):
            r, c = row + dr*i, col + dc*i
            if 0 <= r < 8 and 0 <= c < 8:
                target_color = board[r][c][0]
                path.append((r, c))
                if target_color == 'n':
                    moves.append((r, c, list(path)))
                elif target_color != color:
                    moves.append((r, c, list(path)))
                    break
                else:
                    break
            else:
                break
    return moves

def get_bishop_moves(row, col, color):
    moves = []
    for dr, dc in [[-1,-1],[-1,1],[1,-1],[1,1]]:
        path = []
        for i in range(1, 8):
            r, c = row + dr*i, col + dc*i
            if 0 <= r < 8 and 0 <= c < 8:
                target_color = board[r][c][0]
                path.append((r, c))
                if target_color == 'n':
                    moves.append((r, c, list(path)))
                elif target_color != color:
                    moves.append((r, c, list(path)))
                    break
                else:
                    break
            else:
                break
    return moves

def get_knight_moves(row, col, color):
    moves = []
    for dr, dc in [[-2,-1],[-2,1],[-1,-2],[-1,2],[1,-2],[1,2],[2,-1],[2,1]]:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            if board[r][c][0] == 'n':
                moves.append((r, c, [(r, c)]))
    return moves

def get_pawn_moves(row, col, color):
    moves = []
    direction = 1 if color == 'w' else -1
    start_row = 1 if color == 'w' else 6
    
    r1 = row + direction
    if 0 <= r1 < 8 and board[r1][col][0] == 'n':
        moves.append((r1, col, [(r1, col)]))
        r2 = row + direction * 2
        if row == start_row and 0 <= r2 < 8 and board[r2][col][0] == 'n':
            moves.append((r2, col, [(r1, col), (r2, col)]))
            
    for dc in [-1, 1]:
        r_attack = row + direction
        c_attack = col + dc
        if 0 <= r_attack < 8 and 0 <= c_attack < 8:
            target_color = board[r_attack][c_attack][0]
            if target_color != 'n' and target_color != color:
                moves.append((r_attack, c_attack, [(r_attack, c_attack)]))
    return moves

def get_valid_moves(row, col):
    cell = board[row][col]
    color = cell[0]
    kind = cell[1]

    if color == 'n':
        return []

    if kind == "K": return get_king_moves(row, col, color)
    elif kind == "Q": return get_queen_moves(row, col, color)
    elif kind == "R": return get_bishop_moves(row, col, color)
    elif kind == "B": return get_knight_moves(row, col, color)
    elif kind == "N": return get_rook_moves(row, col, color)
    elif kind == "P": return get_pawn_moves(row, col, color)
    
    return []

# ================= 绘图与交互逻辑 =================

def draw_board(x, y, offset_x, offset_y, cell_data):
    n = 0
    if y % 2 != 0:
        n += 1
    if (x + n) % 2 == 1:
        bg_color = (255, 255, 255)
    else:
        bg_color = (0, 0, 0)
        
    rect = Rect(
        x * pieces_draw_size + offset_x, 
        y * pieces_draw_size + offset_y, 
        pieces_draw_size, 
        pieces_draw_size
    )
    screen.draw.filled_rect(rect, color=bg_color)
    
    if cell_data[2] == 'y':
        pygame.draw.rect(screen.surface, (255, 255, 0), rect, 4) 
    elif cell_data[2] == 'r':
        pygame.draw.rect(screen.surface, (0, 255, 0), rect, 4)

def draw_polygon_shape(pos, num_sides, radius, border_width, colour1, colour2, start_angle=-90):
    points = []
    for i in range(num_sides):
        angle = math.radians(start_angle + i * 360 / num_sides)
        points.append((pos[0] + radius * math.cos(angle), pos[1] + radius * math.sin(angle)))
    pygame.draw.polygon(screen.surface, colour2, points, border_width)
    
    fill_points = []
    fill_radius = radius - border_width
    for i in range(num_sides):
        angle = math.radians(start_angle + i * 360 / num_sides)
        fill_points.append((pos[0] + fill_radius * math.cos(angle), pos[1] + fill_radius * math.sin(angle)))
    pygame.draw.polygon(screen.surface, colour1, fill_points)

def draw_chess(pos, color, chess_kind, piece_num):
    border_width = 5
    if color == 'n':
        return
    elif color == 'w':
        colour1 = (255, 255, 255) 
        colour2 = (0, 0, 0)       
    elif color == 'b':
        colour2 = (255, 255, 255) 
        colour1 = (0, 0, 0)       

    chess_size = chess_draw_size - 10

    if chess_kind == "Q":
        inner_r = chess_size / math.sqrt(3)
        points = []
        for i in range(6):
            angle_outer = math.radians(-90 + i * 60)
            points.append((pos[0] + chess_size * math.cos(angle_outer), pos[1] + chess_size * math.sin(angle_outer)))
            angle_inner = math.radians(-90 + i * 60 + 60)
            points.append((pos[0] + inner_r * math.cos(angle_inner), pos[1] + inner_r * math.sin(angle_inner)))
        pygame.draw.polygon(screen.surface, colour2, points, border_width)
        fill_inner_r = inner_r - 1
        fill_outer_r = chess_size - 1
        fill_points = []
        for i in range(6):
            angle_outer = math.radians(-90 + i * 60)
            fill_points.append((pos[0] + fill_outer_r * math.cos(angle_outer), pos[1] + fill_outer_r * math.sin(angle_outer)))
            angle_inner = math.radians(-90 + i * 60 + 60)
            fill_points.append((pos[0] + fill_inner_r * math.cos(angle_inner), pos[1] + fill_inner_r * math.sin(angle_inner)))
        pygame.draw.polygon(screen.surface, colour1, fill_points)

    elif chess_kind == "K":
        points = []
        outer_r = chess_size
        inner_r = chess_size * 0.382 
        for i in range(5):
            angle_outer = math.radians(-90 + i * 72)
            points.append((pos[0] + outer_r * math.cos(angle_outer), pos[1] + outer_r * math.sin(angle_outer)))
            angle_inner = math.radians(-90 + i * 72 + 36)
            points.append((pos[0] + inner_r * math.cos(angle_inner), pos[1] + inner_r * math.sin(angle_inner)))
        pygame.draw.polygon(screen.surface, colour2, points, border_width)
        fill_points = []
        fill_outer_r = outer_r - 1
        fill_inner_r = inner_r - 1
        for i in range(5):
            angle_outer = math.radians(-90 + i * 72)
            fill_points.append((pos[0] + fill_outer_r * math.cos(angle_outer), pos[1] + fill_outer_r * math.sin(angle_outer)))
            angle_inner = math.radians(-90 + i * 72 + 36)
            fill_points.append((pos[0] + fill_inner_r * math.cos(angle_inner), pos[1] + fill_inner_r * math.sin(angle_inner)))
        pygame.draw.polygon(screen.surface, colour1, fill_points)

    elif chess_kind == "R":
        draw_polygon_shape(pos, 4, chess_size, border_width, colour1, colour2, start_angle=-45)

    elif chess_kind == "B":
        pygame.draw.circle(screen.surface, colour2, (int(pos[0]), int(pos[1])), chess_size, border_width)
        pygame.draw.circle(screen.surface, colour1, (int(pos[0]), int(pos[1])), chess_size - border_width)

    elif chess_kind == "N":
        draw_polygon_shape(pos, 6, chess_size, border_width, colour1, colour2, start_angle=-90)

    elif chess_kind == "P":
        if color == 'w':
            start_angle = 90
        else:
            start_angle = -90
        draw_polygon_shape(pos, 3, chess_size, border_width, colour1, colour2, start_angle=start_angle)

    if chess_kind not in ("Q", "K"):
        num_surf = num_font.render(str(piece_num), True, colour2)
        num_rect = num_surf.get_rect(center=(int(pos[0]), int(pos[1])))
        screen.surface.blit(num_surf, num_rect)

def draw_info_panel():
    board_size = 8 * pieces_draw_size
    offset_x = (WIDTH - board_size) / 2
    
    white_x = offset_x / 2
    title_surf_w = chinese_font.render("白方阵容", True, (255, 255, 255))
    title_rect_w = title_surf_w.get_rect(center=(white_x, 40))
    screen.surface.blit(title_surf_w, title_rect_w)
    
    black_x = offset_x + board_size + (WIDTH - offset_x - board_size) / 2
    title_surf_b = chinese_font.render("黑方阵容", True, (0, 0, 0))
    title_rect_b = title_surf_b.get_rect(center=(black_x, 40))
    screen.surface.blit(title_surf_b, title_rect_b)
    
    white_pieces = []
    black_pieces = []
    for row in range(8):
        for col in range(8):
            cell = board[row][col]
            color = cell[0]
            if color == 'n':
                continue
            if color == 'w':
                white_pieces.append(cell)
            elif color == 'b':
                black_pieces.append(cell)
                
    white_pieces.sort(key=lambda x: (piece_order.get(x[1], 99), x[3]))
    black_pieces.sort(key=lambda x: (piece_order.get(x[1], 99), x[3]))
    
    white_y = 90
    black_y = 90
    line_height = 45
    
    last_kind_w = None
    for cell in white_pieces:
        kind = cell[1]
        if kind != last_kind_w:
            category_text = f"【{piece_names.get(kind, '未知')}】"
            cat_surf = chinese_font.render(category_text, True, (255, 215, 0))
            screen.surface.blit(cat_surf, (20, white_y))
            white_y += line_height
            last_kind_w = kind
            
        num = cell[3]
        hp = cell[4]
        melee_dmg = cell[5]
        ranged_dmg = cell[6]
        info_text = f"  {num}：{hp}，{melee_dmg}，{ranged_dmg}"
        info_surf = chinese_font.render(info_text, True, (220, 220, 220))
        screen.surface.blit(info_surf, (20, white_y))
        white_y += line_height
        
    last_kind_b = None
    for cell in black_pieces:
        kind = cell[1]
        if kind != last_kind_b:
            category_text = f"【{piece_names.get(kind, '未知')}】"
            cat_surf = chinese_font.render(category_text, True, (255, 215, 0))
            screen.surface.blit(cat_surf, (offset_x + board_size + 20, black_y))
            black_y += line_height
            last_kind_b = kind
            
        num = cell[3]
        hp = cell[4]
        melee_dmg = cell[5]
        ranged_dmg = cell[6]
        info_text = f"  {num}：{hp}，{melee_dmg}，{ranged_dmg}"
        info_surf = chinese_font.render(info_text, True, (220, 220, 220))
        screen.surface.blit(info_surf, (offset_x + board_size + 20, black_y))
        black_y += line_height

def on_mouse_down(pos, button):
    global selected_pos, current_turn
    if button == mouse.LEFT:
        board_size = 8 * pieces_draw_size
        offset_x = (WIDTH - board_size) / 2
        offset_y = (HEIGHT - board_size) / 2
        
        col = int((pos[0] - offset_x) // pieces_draw_size)
        row = int((pos[1] - offset_y) // pieces_draw_size)
        
        if 0 <= row < 8 and 0 <= col < 8:
            cell_data = board[row][col]
            
            if selected_pos is not None and cell_data[2] == 'point':
                s_row, s_col = selected_pos
                attacker = board[s_row][s_col]
                target = board[row][col]
                
                valid_moves = get_valid_moves(s_row, s_col)
                move_path = None
                for r, c, path in valid_moves:
                    if r == row and c == col:
                        move_path = path
                        break
                
                if target[0] != 'n':
                    target[4] -= attacker[5]
                    
                    if target[4] <= 0:
                        board[row][col] = attacker
                        board[s_row][s_col] = ['n', 0, 'n', 0, 0, 0, 0]
                    else:
                        board[s_row][s_col] = ['n', 0, 'n', 0, 0, 0, 0]
                        if move_path and len(move_path) >= 2:
                            retreat_r, retreat_c = move_path[-2]
                            board[retreat_r][retreat_c] = attacker
                        else:
                            board[s_row][s_col] = attacker
                else:
                    board[row][col] = attacker
                    board[s_row][s_col] = ['n', 0, 'n', 0, 0, 0, 0]
                
                if board[row][col][1] == 6:
                    if (board[row][col][0] == 'w' and row == 7) or (board[row][col][0] == 'b' and row == 0):
                        board[row][col][1] = 4
                        
                current_turn = 'b' if current_turn == 'w' else 'w'
                selected_pos = None
                
            elif cell_data[0] == current_turn and cell_data[0] != 'n':
                selected_pos = (row, col)
            else:
                selected_pos = None

def update():
    global selected_pos
    
    # 每帧实时更新所有棋子的伤害属性
    update_piece_stats()
    
    for row in range(8):
        for col in range(8):
            board[row][col][2] = 'n'
            
    board_size = 8 * pieces_draw_size
    offset_x = (WIDTH - board_size) / 2
    offset_y = (HEIGHT - board_size) / 2
    
    mx, my = pygame.mouse.get_pos()
    hover_col = int((mx - offset_x) // pieces_draw_size)
    hover_row = int((my - offset_y) // pieces_draw_size)
    
    if 0 <= hover_row < 8 and 0 <= hover_col < 8:
        board[hover_row][hover_col][2] = 'y'
        
    if selected_pos is not None:
        s_row, s_col = selected_pos
        board[s_row][s_col][2] = 'r'
        
        valid_moves = get_valid_moves(s_row, s_col)
        for r, c, path in valid_moves:
            board[r][c][2] = 'point'

def draw():
    board_size = 8 * pieces_draw_size
    offset_x = (WIDTH - board_size) / 2
    offset_y = (HEIGHT - board_size) / 2
    screen.fill((128, 128, 128))
    
    draw_info_panel()
    
    for row in range(8):
        for col in range(8):
            cell_data = board[row][col]
            draw_board(col, row, offset_x, offset_y, cell_data)
            
            center_x = offset_x + col * pieces_draw_size + pieces_draw_size / 2
            center_y = offset_y + row * pieces_draw_size + pieces_draw_size / 2
            pos = (center_x, center_y)
            
            draw_chess(pos, cell_data[0], cell_data[1], cell_data[3])
            
            if cell_data[2] == 'point':
                n = 0
                if row % 2 != 0:
                    n += 1
                if (col + n) % 2 == 1:
                    bg_color = (255, 255, 255)
                else:
                    bg_color = (0, 0, 0)
                
                if cell_data[0] != 'n':
                    s_row, s_col = selected_pos
                    selected_color = board[s_row][s_col][0]
                    if cell_data[0] != selected_color:
                        dot_color = (0, 0, 0) if cell_data[0] == 'w' else (255, 255, 255)
                    else:
                        dot_color = (255 - bg_color[0], 255 - bg_color[1], 255 - bg_color[2])
                else:
                    dot_color = (255 - bg_color[0], 255 - bg_color[1], 255 - bg_color[2])
                
                if cell_data[0] != 'n':
                    dot_bg_surf = pygame.Surface((30, 30), pygame.SRCALPHA)
                    pygame.draw.circle(dot_bg_surf, (0, 0, 0, 100), (15, 15), 15)
                    screen.surface.blit(dot_bg_surf, (center_x - 15, center_y - 15))
                pygame.draw.circle(screen.surface, dot_color, (int(center_x), int(center_y)), 10)
pgzrun.go()