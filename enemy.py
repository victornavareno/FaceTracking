import pygame
import random

class Enemy:
    ENEMY_COLOR = (255, 0, 0)
    

    def __init__(self, ENEMY_SIZE, WIDTH, HEIGHT, ENEMY_SPEED, screen):

        self.ENEMY_SIZE = ENEMY_SIZE
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.SPEED = ENEMY_SPEED
        self.screen = screen
        

        # Random initial position for the enemy within screen boundaries
        self.x = random.randint(0, WIDTH - self.ENEMY_SIZE)
        self.y = random.randint(0, HEIGHT - self.ENEMY_SIZE)
        # Random velocity for movement
        self.vx = random.choice([-3, -2, 2, 3])
        self.vy = random.choice([-3, -2, 2, 3])

    def move(self):
        # Move the enemy
        self.x += self.SPEED * self.vx
        self.y += self.SPEED * self.vy
        # Bounce off walls
        if self.x <= 0 or self.x >= self.WIDTH - self.ENEMY_SIZE:
            self.vx = -self.vx
        if self.y <= 0 or self.y >= self.HEIGHT - self.ENEMY_SIZE:
            self.vy = -self.vy

    def draw(self):
        # Draw the enemy on the screen
        pygame.draw.rect(self.screen, self.ENEMY_COLOR, (self.x, self.y, self.ENEMY_SIZE, self.ENEMY_SIZE))

    def get_position(self):
        # Return the current position of the enemy
        return [self.x, self.y]
