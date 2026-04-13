import pygame
import numpy as np
import cv2
import random
import os
import csv

# --- SETUP ---
if not os.path.exists("dataset"):
    os.makedirs("dataset")

with open("labels.csv", "w", newline="") as f:
    csv.writer(f).writerow(["filename", "label"])

pygame.init()

WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Autonomous Car")

clock = pygame.time.Clock()

# Colors
ROAD_COLOR = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BG = (30, 30, 30)

LEFT_BOUND = 150
RIGHT_BOUND = 450

# Car
car_w, car_h = 50, 80
car_x = WIDTH // 2 - car_w // 2
car_y = HEIGHT - 150

# --- SINGLE OBSTACLE ---
obstacle = [
    random.randint(LEFT_BOUND + 20, RIGHT_BOUND - 60),
    random.randint(-800, -300)
]

# Traffic signal
signal_state = "GREEN"
signal_timer = 0

# --- STEERING & LOCK ---
steering = 0
decision_made = False   # 🔒 prevents multiple decisions

frame_count = 0
running = True

# --- GAME LOOP ---
while running:
    screen.fill(BG)

    # Draw road
    pygame.draw.rect(screen, ROAD_COLOR,
                     (LEFT_BOUND, 0, RIGHT_BOUND - LEFT_BOUND, HEIGHT))

    # Lane divider
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, WHITE,
                         ((LEFT_BOUND + RIGHT_BOUND)//2, y),
                         ((LEFT_BOUND + RIGHT_BOUND)//2, y + 20), 4)

    # --- TRAFFIC SIGNAL ---
    signal_timer += 1
    if signal_timer < 250:
        signal_state = "GREEN"
    elif signal_timer < 350:
        signal_state = "YELLOW"
    elif signal_timer < 600:
        signal_state = "RED"
    else:
        signal_timer = 0

    sig_color = GREEN if signal_state == "GREEN" else YELLOW if signal_state == "YELLOW" else RED
    pygame.draw.circle(screen, sig_color, (80, 80), 20)

    # Speed control
    speed = 6 if signal_state != "RED" else 0

    car_rect = pygame.Rect(car_x, car_y, car_w, car_h)

    # --- OBSTACLE ---
    obstacle[1] += speed
    obs_rect = pygame.Rect(obstacle[0], obstacle[1], 50, 50)

    distance = car_y - obstacle[1]

    # --- DECISION LOGIC (FINAL PERFECT) ---
    if 0 < distance < 240:

        obs_center = obstacle[0] + 25
        car_center = car_x + car_w // 2

        # 🔒 ONLY ONE DECISION PER OBSTACLE
        if not decision_made:

            # LEFT → go RIGHT
            if obs_center < car_center - 10:
                steering = 1

            # RIGHT → go LEFT
            elif obs_center > car_center + 10:
                steering = -1

            # CENTER → choose safest
            else:
                left_space = car_x - LEFT_BOUND
                right_space = RIGHT_BOUND - (car_x + car_w)

                if left_space > right_space:
                    steering = -1
                else:
                    steering = 1

            decision_made = True   # 🔒 lock decision

    # Apply movement
    car_x += steering * 5

    # Lane safety
    car_x = max(LEFT_BOUND + 5, min(RIGHT_BOUND - car_w - 5, car_x))

    # --- COLLISION DETECTION ---
    if car_rect.colliderect(obs_rect):
        print("💥 COLLISION OCCURRED")
        running = False

    # Draw obstacle
    pygame.draw.rect(screen, GREEN, obs_rect)

    # --- SPAWN NEXT OBSTACLE ---
    if obstacle[1] > HEIGHT:
        obstacle[1] = random.randint(-800, -300)
        obstacle[0] = random.randint(LEFT_BOUND + 20, RIGHT_BOUND - 60)

        decision_made = False   # 🔓 allow new decision
        steering = 0

    # Draw car
    pygame.draw.rect(screen, RED, (car_x, car_y, car_w, car_h))

    # --- DATASET EXPORT ---
    if frame_count % 5 == 0 and speed > 0:
        frame = pygame.surfarray.array3d(screen)
        gray = cv2.cvtColor(np.transpose(frame, (1, 0, 2)), cv2.COLOR_BGR2GRAY)
        img_32 = cv2.resize(gray, (32, 32))

        fname = f"img_{frame_count}.png"
        cv2.imwrite(os.path.join("dataset", fname), img_32)

        with open("labels.csv", "a", newline="") as f:
            csv.writer(f).writerow([fname, steering])

    frame_count += 1

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(30)

pygame.quit()