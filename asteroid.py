import pygame
import random

class asteroid:
    #TODO: HACER SKIN DE LOS ENEMIGOS
    ASTEROID_COLOR = (255, 0, 0)
    
    #constructor del enemigo
    def __init__(self, ASTEROID_SIZE, WIDTH, HEIGHT, ASTEROID_SPEED, screen, image):

        self.ASTEROID_SIZE = ASTEROID_SIZE
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.SPEED = ASTEROID_SPEED
        self.screen = screen
        self.image = image

        # posicion random del enemigo cuando spawnea
        self.x = random.randint(0, WIDTH - self.ASTEROID_SIZE)
        self.y = random.randint(0, HEIGHT - self.ASTEROID_SIZE)

        # elige direccion random del enemigo, 2, 3 y 4 para q sea mas natural y haya enemigos muy rapidos
        self.vx = random.choice([-4, -3, -2, -2, 2, 3, 3])
        self.vy = random.choice([-4, -3, -3, -2, 2, 3, 4])

    def move(self):
        # mueve el enemigo con una velocidad concreta
        self.x += self.SPEED * self.vx
        self.y += self.SPEED * self.vy

        # colision para rebotar en el muro
        if self.x <= 0 or self.x >= self.WIDTH - self.ASTEROID_SIZE:
            self.vx = -self.vx
        if self.y <= 0 or self.y >= self.HEIGHT - self.ASTEROID_SIZE:
            self.vy = -self.vy

    def draw(self):
        
        # # dibujo el ASTEROIDe
        
        # Draw the red square (ASTEROID)
        pygame.draw.rect(self.screen, self.ASTEROID_COLOR, (self.x, self.y, self.ASTEROID_SIZE, self.ASTEROID_SIZE))

        # Center the ASTEROID on the red square
        ASTEROID_width, ASTEROID_height = self.image.get_size()  # Get the dimensions of the ASTEROID image
        center_x = self.x + self.ASTEROID_SIZE / 2
        center_y = self.y + self.ASTEROID_SIZE / 2

        # Calculate the top-left position to center the ASTEROID
        ASTEROID_x = center_x - ASTEROID_width / 2
        ASTEROID_y = center_y - ASTEROID_height / 2

        # Draw the ASTEROID centered on the square
        self.screen.blit(self.image, (ASTEROID_x, ASTEROID_y))


    def get_position(self):
        return [self.x, self.y]
