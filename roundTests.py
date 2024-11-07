import pygame
import random
import sys
import cv2
import numpy as np
import mediapipe as mp
import enemy

# Initialize pygame
pygame.init()

# VARIABLES GLOBALES
WIDTH, HEIGHT = 1000, 700


BLUE = (0, 0, 255)
RED = (255, 0, 0)

PLAYER_SIZE = 60

ENEMY_SIZE = 40
ENEMY_SPEED = 1  # Speed of the enemy

### CARGANDO ASSETS ###
# ASSET TIERRA 
earth_image = pygame.image.load("img/earth.png")
earth_image = pygame.transform.scale(earth_image, (PLAYER_SIZE*2, PLAYER_SIZE*2))

# ASSET ASTEROIDE
asteroid_image = pygame.image.load("img/asteroid.png")
asteroid_image = pygame.transform.scale(asteroid_image, (ENEMY_SIZE*5, ENEMY_SIZE*5))
#########################

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SALVA LA TIERRA")

# Set the game clock
clock = pygame.time.Clock()

# Font for displaying text
font = pygame.font.Font(None, 36)

# Initialize camera
cap = cv2.VideoCapture(0)  # 0 is typically the default camera

# Initialize MediaPipe face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

# Load loading screen image
loading_image = pygame.image.load("img/loading_screen.jpg")  # Replace with your image path
loading_image = pygame.transform.scale(loading_image, (WIDTH, HEIGHT))

def display_loading_screen():
    screen.blit(loading_image, (0, 0))
    pygame.display.update()
    pygame.time.delay(1000)  # Display for 3 seconds

def detect_collision(player_pos, enemy_pos):
    px, py = player_pos
    ex, ey = enemy_pos
    return (ex < px < ex + ENEMY_SIZE or ex < px + PLAYER_SIZE < ex + ENEMY_SIZE) and \
           (ey < py < ey + ENEMY_SIZE or ey < py + PLAYER_SIZE < ey + ENEMY_SIZE)

def check_collisions(player_pos, enemies):
    for enemy in enemies:
        if detect_collision(player_pos, enemy.get_position()):
            return True
    return False

def handle_player_position(results):
    # Default player position if no face is detected
    player_pos = (WIDTH // 2, HEIGHT // 2)

    # Update player position based on nose tip detection
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            nose_tip = face_landmarks.landmark[1]
            nose_x = int((1 - nose_tip.x) * WIDTH)
            nose_y = int(nose_tip.y * HEIGHT)
            player_pos = (nose_x, nose_y)
            break
    return player_pos


def initialize_enemies(round_number):
    num_enemies = 4 + 2 * (round_number - 1)
    return [enemy.Enemy(ENEMY_SIZE, WIDTH, HEIGHT, ENEMY_SPEED, screen, asteroid_image) for _ in range(num_enemies)]

def display_countdown(round_number, enemies, player_pos):
    # Display countdown on screen with frozen enemies and player position
    for count in range(3, 0, -1):
        # Display background
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame from camera.")
            break

        # Resize and flip the frame to fit the game window
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(np.rot90(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        screen.blit(frame_surface, (0, 0))

        # Draw the player's tracked nose
        pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE))

        # Draw stationary enemies
        for enemy in enemies:
            enemy.draw()

        # Display countdown text in the center
        countdown_text = font.render(f"ROUND {round_number} STARTING IN {count}...", True, RED)
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))
        
        # Update the display and wait for 1 second
        pygame.display.update()
        pygame.time.delay(1000)

def run_round(round_number):
    # Initialize enemies for the current round
    
    enemies = initialize_enemies(round_number)
    round_time = 20000  # 20 seconds in milliseconds
    round_start_time = pygame.time.get_ticks()  # Record the start time of the round

    # Capture a frame for the player position detection
    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)
        player_pos = handle_player_position(results)
    else:
        player_pos = (WIDTH // 2, HEIGHT // 2)  # Default to center if no frame

    # Display the countdown before starting the round
    display_countdown(round_number, enemies, player_pos)

    # Main round loop
    while True:
        # Event loop to handle quitting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                cap.release()
                sys.exit()

        # Capture frame-by-frame from the camera
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame from camera.")
            break

        # Resize and flip the frame to fit the game window
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect face and landmarks
        results = face_mesh.process(frame_rgb)
        player_pos = handle_player_position(results)

        # Display the camera frame as the background
        frame_surface = pygame.surfarray.make_surface(np.rot90(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        screen.blit(frame_surface, (0, 0))

        # Check for collisions
        if check_collisions(player_pos, enemies):
            pygame.display.update()
            pygame.time.delay(2000)
            return False  # Player lost the game

        # Draw player at nose position
        pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE))
        # Draw the Earth image at the player's position

        # Center the asteroid on the red square
        earth_width, earth_height = earth_image.get_size()  # Get the dimensions of the asteroid image
        center_x = player_pos[0] + PLAYER_SIZE / 2
        center_y = player_pos[1] + PLAYER_SIZE / 2

        # Calculate the top-left position to center the asteroid
        earth_x = center_x - earth_width / 2
        earth_y = center_y - earth_height / 2

        screen.blit(earth_image, (earth_x, earth_y))


        # Calculate elapsed time for the current round
        elapsed_time = pygame.time.get_ticks() - round_start_time

        # Only start moving enemies after the countdown (3 seconds)
        if elapsed_time >= 3000:
            for enemy in enemies:
                enemy.move()
                enemy.draw()

        # Check if 20 seconds have passed for the current round
        if elapsed_time >= round_time:
            return True  # Player survived this round

        # Display the round number and time remaining
        round_text = font.render(f"Round: {round_number}", True, RED)
        time_text = font.render(f"Time: {round_time // 1000 - elapsed_time // 1000}", True, RED)
        screen.blit(round_text, (10, 10))
        screen.blit(time_text, (10, 40))

        # Update display and set FPS
        pygame.display.update()
        clock.tick(30)

def main_game():
    display_loading_screen()  # Show the loading screen at the start
    round_number = 1
    while True:
        survived = run_round(round_number)
        if not survived:
            break  # End the game if the player lost

        # Move to the next round if the player survived
        round_number += 1

    # Game over message
    text = font.render("GAME OVER!!", True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)

# Run the main game function
main_game()

# Release the camera and quit pygame
cap.release()
pygame.quit()
sys.exit()
