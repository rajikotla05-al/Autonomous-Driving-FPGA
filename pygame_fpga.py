import pygame
import numpy as np
import cv2
import random
import os
import csv
import serial

# --- SERIAL SETUP ---
# IMPORTANT: Close the "Hardware Manager" in Vivado before running this!
try:
    # Change 'COM3' to your actual port from Device Manager
    ser = serial.Serial('COM7', 9600, timeout=0.01) 
    print("Connected to Basys 3!")
except Exception as e:
    print(f"Serial Error: {e}. Running in simulation mode only.")
    ser = None

# --- SETUP ---
if not os.path.exists("dataset"):
    os.makedirs("dataset")

with open("labels.csv", "w", newline="") as f:
    csv.writer(f).writerow(["filename", "label"])

pygame.init()
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Autonomous Car - FPGA Interface")
clock = pygame.time.Clock()

# Colors & Constants
ROAD_COLOR, RED, GREEN, YELLOW, WHITE, BG = (50, 50, 50), (255, 0, 0), (0, 200, 0), (255, 255, 0), (255, 255, 255), (30, 30, 30)
LEFT_BOUND, RIGHT_BOUND = 150, 450
car_w, car_h = 50, 80
car_x, car_y = WIDTH // 2 - car_w // 2, HEIGHT - 150

# Obstacle & Logic Variables
obstacle = [random.randint(LEFT_BOUND + 20, RIGHT_BOUND - 60), random.randint(-800, -300)]
signal_state, signal_timer, steering, decision_made, frame_count = "GREEN", 0, 0, False, 0

running = True
while running:
    screen.fill(BG)
    
    # 1. Handle Events (Crucial to prevent blank/frozen screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Draw Environment
    pygame.draw.rect(screen, ROAD_COLOR, (LEFT_BOUND, 0, RIGHT_BOUND - LEFT_BOUND, HEIGHT))
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, WHITE, ((LEFT_BOUND + RIGHT_BOUND)//2, y), ((LEFT_BOUND + RIGHT_BOUND)//2, y + 20), 4)

    # 3. Traffic Signal Logic
    signal_timer += 1
    if signal_timer < 250: signal_state = "GREEN"
    elif signal_timer < 350: signal_state = "YELLOW"
    elif signal_timer < 600: signal_state = "RED"
    else: signal_timer = 0
    
    sig_color = GREEN if signal_state == "GREEN" else YELLOW if signal_state == "YELLOW" else RED
    pygame.draw.circle(screen, sig_color, (80, 80), 20)
    speed = 6 if signal_state != "RED" else 0

    # 4. Obstacle Movement
    obstacle[1] += speed
    obs_rect = pygame.Rect(obstacle[0], obstacle[1], 50, 50)
    car_rect = pygame.Rect(car_x, car_y, car_w, car_h)
    distance = car_y - obstacle[1]

    # 5. Decision Logic & FPGA Serial Output
    if 0 < distance < 240:
        obs_center = obstacle[0] + 25
        car_center = car_x + car_w // 2

        if not decision_made:
            if obs_center < car_center - 10:
                steering = 1
                if ser: ser.write(b'R') # Send 'r' to FPGA
                print("Action: Move Right")
            elif obs_center > car_center + 10:
                steering = -1
                if ser: ser.write(b'L') # Send 'L' to FPGA
                print("Action: Move Left")
            else:
                steering = -1 if (car_x - LEFT_BOUND) > (RIGHT_BOUND - (car_x + car_w)) else 1
                if ser: ser.write(b'L' if steering == -1 else b'R')
            decision_made = True 

    # 6. Apply Movement & Reset
    car_x += steering * 5
    car_x = max(LEFT_BOUND + 5, min(RIGHT_BOUND - car_w - 5, car_x))

    if obstacle[1] > HEIGHT:
        obstacle = [random.randint(LEFT_BOUND + 20, RIGHT_BOUND - 60), random.randint(-800, -300)]
        decision_made = False
        steering = 0
        if ser: ser.write(b'S') # Send 'S' for Straight
        print("Action: Straight")

    # 7. Draw Car & Obstacle
    pygame.draw.rect(screen, GREEN, obs_rect)
    pygame.draw.rect(screen, RED, car_rect)

    # 8. Refresh Screen
    pygame.display.update()
    clock.tick(30)

if ser: ser.close()
pygame.quit()