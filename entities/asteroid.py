import pygame
import random

class Asteroid:
    ASTEROID_COLOR = (255, 0, 0)

    # Constructor del asteroide
    def __init__(self, ASTEROID_SIZE, WIDTH, HEIGHT, ASTEROID_SPEED, screen, image):
        self.ASTEROID_SIZE = ASTEROID_SIZE
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.SPEED = ASTEROID_SPEED
        self.screen = screen
        self.image = image

        # Posición aleatoria del asteroide cuando aparece
        self.x = random.randint(0, WIDTH - self.ASTEROID_SIZE)
        self.y = random.randint(0, HEIGHT - self.ASTEROID_SIZE)

        # Elige dirección aleatoria del asteroide
        self.vx = random.choice([-4, -3, -2, -2, 2, 3, 3])
        self.vy = random.choice([-4, -3, -3, -2, 2, 3, 4])

    def move(self):
        # Mueve el asteroide con una velocidad concreta
        self.x += self.SPEED * self.vx
        self.y += self.SPEED * self.vy

        # Colisión para rebotar en el muro
        if self.x <= 0 or self.x >= self.WIDTH - self.ASTEROID_SIZE:
            self.vx = -self.vx
        if self.y <= 0 or self.y >= self.HEIGHT - self.ASTEROID_SIZE:
            self.vy = -self.vy

    def draw(self):
        # Dibuja el asteroide

        # Dibuja el cuadrado rojo (asteroide)
        pygame.draw.rect(self.screen, self.ASTEROID_COLOR, (self.x, self.y, self.ASTEROID_SIZE, self.ASTEROID_SIZE))

        # Centra el asteroide en el cuadrado
        ASTEROID_width, ASTEROID_height = self.image.get_size()
        center_x = self.x + self.ASTEROID_SIZE / 2
        center_y = self.y + self.ASTEROID_SIZE / 2

        # Calcula la posición superior-izquierda para centrar el asteroide
        ASTEROID_x = center_x - ASTEROID_width / 2
        ASTEROID_y = center_y - ASTEROID_height / 2

        # Dibuja el asteroide centrado sobre el cuadrado
        self.screen.blit(self.image, (ASTEROID_x, ASTEROID_y))

    def get_position(self):
        return [self.x, self.y]
