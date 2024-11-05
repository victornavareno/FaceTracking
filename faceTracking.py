import pygame
import random
import sys
import cv2
import numpy as np
import mediapipe as mp
import enemy

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avoid the Red Squares")

# Colors
BLUE = (0, 0, 255)

# PLAYER SQUARE DIMENSION
PLAYER_SIZE = 20

# ENEMY STATS
MAX_ENEMIES = 4  # NUMBER OF ENEMIES ON THE SCREEN
ENEMY_SIZE = 40
ENEMY_SPEED = 5 # SPEED OF THE ENEMY:  1 is the default value 4 IS CRAAAZY FAST 

RED = (255, 0, 0)

# Set the game clock
clock = pygame.time.Clock()

# Font for displaying text
font = pygame.font.Font(None, 36)

# Initialize camera
cap = cv2.VideoCapture(0)  # 0 is typically the default camera

# Initialize MediaPipe face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

def detect_collision(player_pos, enemy_pos):
    px, py = player_pos
    ex, ey = enemy_pos

    if (ex < px < ex + ENEMY_SIZE or ex < px + PLAYER_SIZE < ex + ENEMY_SIZE) and \
       (ey < py < ey + ENEMY_SIZE or ey < py + PLAYER_SIZE < ey + ENEMY_SIZE):
        return True
    return False

def check_collisions(player_pos, enemies):
    for enemy in enemies:
        if detect_collision(player_pos, enemy.get_position()):
            return True
    return False

# Create a list of enemies
enemies = [enemy.Enemy(ENEMY_SIZE, WIDTH, HEIGHT, ENEMY_SPEED, screen) for _ in range(MAX_ENEMIES)]

# Main game loop
game_over = False
while not game_over:
    # Event loop to prevent freezing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            cap.release()  # Release the camera when quitting
            sys.exit()

    # Capture frame-by-frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame from camera.")
        break

    # Resize and flip the frame to fit the game window
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    # frame = cv2.flip(frame, 1)  # Flip horizontally to act like a mirror

    # Convert the frame to RGB for MediaPipe processing
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect face and landmarks
    results = face_mesh.process(frame_rgb)

    # Default player position if no face is detected
    player_pos = (WIDTH // 2, HEIGHT // 2)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Nose tip landmark (index 1 on MediaPipe face mesh)
            nose_tip = face_landmarks.landmark[1]
            nose_x = int((1-nose_tip.x) * WIDTH)
            nose_y = int(nose_tip.y * HEIGHT)

            # Update player position to follow nose
            player_pos = (nose_x, nose_y)
            break  # Use the first detected face

    # Display the camera frame as the background
    frame_surface = pygame.surfarray.make_surface(np.rot90(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
    screen.blit(frame_surface, (0, 0))

    # Check for collisions
    if check_collisions(player_pos, enemies):
        text = font.render("Game Over!", True, RED)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(2000)
        game_over = True
        break

    # Draw player at nose position
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE))

    # Move and draw enemies
    for enemy in enemies:
        enemy.move()
        enemy.draw()

    # Update display and set FPS
    pygame.display.update()
    clock.tick(30)

# Release the camera and quit pygame
cap.release()
pygame.quit()
sys.exit()
