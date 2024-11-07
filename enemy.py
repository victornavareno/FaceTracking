import pygame
import random

class Enemy:
    #TODO: HACER SKIN DE LOS ENEMIGOS
    ENEMY_COLOR = (255, 0, 0)
    
    #constructor del enemigo
    def __init__(self, ENEMY_SIZE, WIDTH, HEIGHT, ENEMY_SPEED, screen, image):

        self.ENEMY_SIZE = ENEMY_SIZE
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.SPEED = ENEMY_SPEED
        self.screen = screen
        self.image = image

        # posicion random del enemigo cuando spawnea
        self.x = random.randint(0, WIDTH - self.ENEMY_SIZE)
        self.y = random.randint(0, HEIGHT - self.ENEMY_SIZE)

        # elige direccion random del enemigo, 2, 3 y 4 para q sea mas natural y haya enemigos muy rapidos
        self.vx = random.choice([-4, -3, -2, -2, 2, 3, 3])
        self.vy = random.choice([-4, -3, -3, -2, 2, 3, 4])

    def move(self):
        # mueve el enemigo con una velocidad concreta
        self.x += self.SPEED * self.vx
        self.y += self.SPEED * self.vy

        # colision para rebotar en el muro
        if self.x <= 0 or self.x >= self.WIDTH - self.ENEMY_SIZE:
            self.vx = -self.vx
        if self.y <= 0 or self.y >= self.HEIGHT - self.ENEMY_SIZE:
            self.vy = -self.vy

    def draw(self):
        
        # # dibujo el asteroide
        
        # Draw the red square (enemy)
        pygame.draw.rect(self.screen, self.ENEMY_COLOR, (self.x, self.y, self.ENEMY_SIZE, self.ENEMY_SIZE))

        # Center the asteroid on the red square
        asteroid_width, asteroid_height = self.image.get_size()  # Get the dimensions of the asteroid image
        center_x = self.x + self.ENEMY_SIZE / 2
        center_y = self.y + self.ENEMY_SIZE / 2

        # Calculate the top-left position to center the asteroid
        asteroid_x = center_x - asteroid_width / 2
        asteroid_y = center_y - asteroid_height / 2

        # Draw the asteroid centered on the square
        self.screen.blit(self.image, (asteroid_x, asteroid_y))


    def get_position(self):
        return [self.x, self.y]
