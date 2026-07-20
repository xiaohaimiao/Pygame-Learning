# pgzrun 07_asteroids.py
import random
import pgzrun
import os
import pygame
import math
import time
from pgzero.builtins import Actor
from pgzero.keyboard import keys

os.environ["SDL_VIDEO_CENTERED"] = "1"
WIDTH = 2000
HEIGHT = 1000

score = 0
is_dead = False
asteroid_count = 5
arena_width = WIDTH
arena_height = HEIGHT
ship_stage = 1
ship_stages = [[10, 100], [5, 300], [2, 600], [1, 1000]]
ship_radius = 20
bullet_timer_limit = 0.3
bullet_radius = 5
ship_x = arena_width / 2
ship_y = arena_height / 2
ship_speed_x = 0
ship_speed_y = 0
ship_angle = 0
bullets = []
bullet_timer = bullet_timer_limit
last_score_update = time.time() 
bullet_safe_time = 0.2  # 子弹的安全时间，单位秒
asteroid_stages = [
    {
        "speed": 120,
        "radius": 15,
    },
    {
        "speed": 70,
        "radius": 30,
    },
    {
        "speed": 50,
        "radius": 50,
    },
    {
        "speed": 20,
        "radius": 80,
    },
]

def reset():
    global asteroids
    global asteroid_count
    # 初始化陨石列表
    asteroids = []
    for _ in range(asteroid_count):
        # 随机选择屏幕边缘（0=上，1=右，2=下，3=左）
        edge = random.randint(0, 3)
        if edge == 0:  # 上边缘
            x = random.uniform(0, arena_width)
            y = 0
        elif edge == 1:  # 右边缘
            x = arena_width
            y = random.uniform(0, arena_height)
        elif edge == 2:  # 下边缘
            x = random.uniform(0, arena_width)
            y = arena_height
        else:  # 左边缘
            x = 0
            y = random.uniform(0, arena_height)
        
        # 添加陨石到列表
        asteroids.append({
            "x": x,
            "y": y,
            "angle": random.random() * (2 * math.pi),
            "stage": len(asteroid_stages) - 1
        })
    
    return


reset()

def update(dt):
    global ship_x
    global ship_y
    global ship_speed_x
    global ship_speed_y
    global ship_angle
    global bullet_timer
    global is_dead
    global asteroid_count
    global score
    global last_score_update
    global bullet_radius
    global bullets
    global ship_stage
    global ship_stages
    global ship_stage

    if is_dead:
        return

    # 每秒增加分数
    current_time = time.time()
    if current_time - last_score_update >= 1.0:  # 如果已经过去至少1秒
        score += asteroid_count // 2  # 每秒增加 asteroid_count // 2 分
        last_score_update = current_time  # 更新上次更新分数的时间
    turn_speed = ship_stages[ship_stage][0]
    if keyboard.K_1:
        ship_stage = 0
    if keyboard.K_2:
        ship_stage = 1
    if keyboard.K_3:
        ship_stage = 2
    if keyboard.K_4:
        ship_stage = 3
    if keyboard.right:
        ship_angle += turn_speed * dt
    if keyboard.left:
        ship_angle -= turn_speed * dt
    ship_angle %= 2 * math.pi
    if keyboard.up:
        ship_speed = 100
        ship_speed_x += math.cos(ship_angle) * ship_speed * dt
        ship_speed_y += math.sin(ship_angle) * ship_speed * dt
    if keyboard.down:
        ship_speed = 100
        ship_speed_x -= math.cos(ship_angle) * ship_speed * dt
        ship_speed_y -= math.sin(ship_angle) * ship_speed * dt
    ship_x += ship_speed_x * dt
    ship_y += ship_speed_y * dt
    ship_x %= arena_width
    ship_y %= arena_height

    def are_circles_intersecting(a_x, a_y, a_radius, b_x, b_y, b_radius):
        return (a_x - b_x)**2 + (a_y - b_y)**2 <= (a_radius + b_radius)**2
    
    for bullet in bullets.copy():
        bullet["time_left"] -= dt
        bullet["safe_time"] -= dt  # 减少子弹的安全时间
        if bullet["time_left"] <= 0:
            bullets.remove(bullet)
            continue
        bullet_speed = 500
        bullet["x"] += math.cos(bullet["angle"]) * bullet_speed * dt
        bullet["y"] += math.sin(bullet["angle"]) * bullet_speed * dt
        bullet["x"] %= arena_width
        bullet["y"] %= arena_height
        for asteroid in asteroids.copy():
            if are_circles_intersecting(
                bullet["x"], bullet["y"], bullet_radius,
                asteroid["x"], asteroid["y"],
                asteroid_stages[asteroid["stage"]]["radius"]
            ):
                bullets.remove(bullet)
                score += 50 + asteroid_count // 5 # 击中陨石增加分数
                if asteroid["stage"] > 0:
                    angle1 = random.random() * (2 * math.pi)
                    angle2 = (angle1 - math.pi) % (2 * math.pi)
                    asteroids.append({
                        "x": asteroid["x"],
                        "y": asteroid["y"],
                        "angle": angle1,
                        "stage": asteroid["stage"] - 1
                    })
                    asteroids.append({
                        "x": asteroid["x"],
                        "y": asteroid["y"],
                        "angle": angle2,
                        "stage": asteroid["stage"] - 1
                    })
                asteroids.remove(asteroid)
                break
    bullet_timer += dt
    if keyboard.S:
        if bullet_timer >= bullet_timer_limit:
            bullet_timer = 0

            bullets.append({
                "x": ship_x + math.cos(ship_angle) * ship_radius,
                "y": ship_y + math.sin(ship_angle) * ship_radius,
                "angle": ship_angle,
                "time_left": 3,
                "safe_time": bullet_safe_time  # 添加安全时间属性
            })
    for asteroid in asteroids:
        asteroid_speed = asteroid_stages[asteroid["stage"]]["speed"]
        asteroid["x"] += math.cos(asteroid["angle"]) * asteroid_speed * dt
        asteroid["y"] += math.sin(asteroid["angle"]) * asteroid_speed * dt
        asteroid["x"] %= arena_width
        asteroid["y"] %= arena_height
        if are_circles_intersecting(
            ship_x, ship_y, ship_radius,
            asteroid["x"], asteroid["y"],
            asteroid_stages[asteroid["stage"]]["radius"]
        ):
            is_dead = True
            break
        # 修复了这里，遍历所有子弹检查是否与飞船碰撞
        for bullet in bullets:
            # 只有当子弹的安全时间已过，才检查碰撞
            if bullet["safe_time"] <= 0 and are_circles_intersecting(
                ship_x, ship_y, ship_radius,
                bullet["x"], bullet["y"],
                bullet_radius
            ):
                is_dead = True
                break
        if is_dead:
            break

    if len(asteroids) == 0:
        if asteroid_count < 21:
            asteroid_count += 2
        reset()
    return

def draw():
    global score
    global ship_stage
    global ship_stages

    screen.fill((0, 0, 0))

    for y in range(-1, 2):
        for x in range(-1, 2):
            offset_x = x * arena_width
            offset_y = y * arena_height

            screen.draw.filled_circle(
                (ship_x + offset_x, ship_y + offset_y),
                ship_radius, color=(0, 0, 255)
            )

            ship_circle_distance = 20
            screen.draw.filled_circle((
                ship_x + offset_x +
                    math.cos(ship_angle) * ship_circle_distance,
                ship_y + offset_y +
                    math.sin(ship_angle) * ship_circle_distance),
                5, color=(0, 255, 255)
            )
            # 添加从船头延伸出的红线
            line_length = ship_stages[ship_stage][1]
            line_start_x = ship_x + offset_x + math.cos(ship_angle) * ship_circle_distance
            line_start_y = ship_y + offset_y + math.sin(ship_angle) * ship_circle_distance
            line_end_x = line_start_x + math.cos(ship_angle) * line_length
            line_end_y = line_start_y + math.sin(ship_angle) * line_length
            screen.draw.line((line_start_x, line_start_y), (line_end_x, line_end_y), (255, 0, 0))

            for bullet in bullets:
                screen.draw.filled_circle(
                    (bullet["x"] + offset_x, bullet["y"] + offset_y),
                    bullet_radius, color=(0, 255, 0)
                )

            for asteroid in asteroids:
                screen.draw.filled_circle((
                    asteroid["x"] + offset_x, asteroid["y"] + offset_y),
                    asteroid_stages[asteroid["stage"]]["radius"],
                    color=(255, 255, 0)
                )
    if is_dead:
        screen.draw.text("You're dead!", center=(WIDTH/2, HEIGHT/2), fontsize=60, color="red")
    screen.draw.text("Score: " + str(score), center=(WIDTH/2, HEIGHT-50), fontsize=60, color="white")
    return
