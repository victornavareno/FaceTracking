import pygame
import random
import sys
import cv2
import numpy as np


pygame.init()

# dimensiones de la pantalla
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avoid the Red Squares")

# Ccolores q usaremos
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Player square dimensions
PLAYER_SIZE = 20

# Enemy square dimensions
ENEMY_SIZE = 20
MAX_ENEMIES = 4  # Maximum number of red squares

# Set the game clock
clock = pygame.time.Clock()

# Font for displaying text
font = pygame.font.Font(None, 36)

# Initialize camera
cap = cv2.VideoCapture(0)  # 0 is typically the default camera

class Enemy:
    def __init__(self):
        # Random initial position for the enemy within screen boundaries
        self.x = random.randint(0, WIDTH - ENEMY_SIZE)
        self.y = random.randint(0, HEIGHT - ENEMY_SIZE)
        # Random velocity for movement
        self.vx = random.choice([-3, -2, 2, 3])
        self.vy = random.choice([-3, -2, 2, 3])

    def move(self):
        # Move the enemy
        self.x += self.vx
        self.y += self.vy
        # Bounce off walls
        if self.x <= 0 or self.x >= WIDTH - ENEMY_SIZE:
            self.vx = -self.vx
        if self.y <= 0 or self.y >= HEIGHT - ENEMY_SIZE:
            self.vy = -self.vy

    def draw(self):
        # Draw the enemy on the screen
        pygame.draw.rect(screen, RED, (self.x, self.y, ENEMY_SIZE, ENEMY_SIZE))

    def get_position(self):
        # Return the current position of the enemy
        return [self.x, self.y]

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
enemies = [Enemy() for _ in range(MAX_ENEMIES)]

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
    frame = cv2.flip(frame, 1)  # Flip horizontally to act like a mirror

    # Convert the frame to RGB (from BGR) and then to a Pygame Surface
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))

    # Display the camera frame as the background
    screen.blit(frame_surface, (0, 0))

    # Get player position from mouse
    player_pos = pygame.mouse.get_pos()

    # Check for collisions
    if check_collisions(player_pos, enemies):
        text = font.render("Game Over!", True, RED)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(2000)
        game_over = True
        break

    # Draw player
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
