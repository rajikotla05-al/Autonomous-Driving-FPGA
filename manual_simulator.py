import pygame
import numpy as np
import cv2
import random
import os
import csv

# ---------------- DATASET ----------------
if not os.path.exists("dataset"):
    os.makedirs("dataset")

with open("labels.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["filename", "label"])

frame_count = 0

# ---------------- PYGAME ----------------
pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Manual Data Collection")

WHITE = (255,255,255)
GRAY = (40,40,40)
ROAD_COLOR = (60,60,60)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)

LEFT_BOUND = 100
RIGHT_BOUND = 300

car_width = 40
car_height = 60
car_x = WIDTH//2 - car_width//2
car_y = HEIGHT - 120

velocity = 3
clock = pygame.time.Clock()

# -------- OBSTACLES --------
obstacles = [[random.randint(LEFT_BOUND+20, RIGHT_BOUND-40), -200]]

# -------- TRAFFIC SIGNAL --------
signal_state = "GREEN"
signal_timer = 0
signal_x = 50
signal_y = 80

# ---------------- MAIN LOOP ----------------
running = True
while running:

    screen.fill(GRAY)

    # ROAD
    pygame.draw.rect(screen, ROAD_COLOR, (LEFT_BOUND, 0, RIGHT_BOUND-LEFT_BOUND, HEIGHT))
    pygame.draw.line(screen, WHITE, (LEFT_BOUND,0), (LEFT_BOUND,HEIGHT), 5)
    pygame.draw.line(screen, WHITE, (RIGHT_BOUND,0), (RIGHT_BOUND,HEIGHT), 5)

    # SIGNAL
    signal_timer += 1
    if signal_timer < 150:
        signal_state = "GREEN"
    elif signal_timer < 250:
        signal_state = "YELLOW"
    elif signal_timer < 400:
        signal_state = "RED"
    else:
        signal_timer = 0

    if signal_state == "GREEN":
        color = GREEN
    elif signal_state == "YELLOW":
        color = YELLOW
    else:
        color = RED

    pygame.draw.circle(screen, color, (signal_x, signal_y), 15)

    # -------- MANUAL CONTROL --------
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        car_x -= 5
        label = -1
    elif keys[pygame.K_RIGHT]:
        car_x += 5
        label = 1
    else:
        label = 0

    car_x = max(LEFT_BOUND, min(RIGHT_BOUND - car_width, car_x))

    # -------- OBSTACLE --------
    for obs in obstacles:
        obs[1] += velocity

        if obs[1] > HEIGHT:
            obs[1] = -200
            obs[0] = random.randint(LEFT_BOUND+20, RIGHT_BOUND-40)

        pygame.draw.rect(screen, GREEN, (obs[0], obs[1], 30, 30))

    # DRAW CAR
    pygame.draw.rect(screen, RED, (car_x, car_y, car_width, car_height))

    # -------- SAVE DATA --------
    frame = pygame.surfarray.array3d(screen)
    frame = np.transpose(frame, (1,0,2))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(gray, (32,32))

    if frame_count % 5 == 0:
        filename = f"img_{frame_count}.png"
        cv2.imwrite(os.path.join("dataset", filename), img)

        with open("labels.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([filename, label])

        print(f"Saved: {filename}, Label: {label}")

    frame_count += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(30)

pygame.quit()