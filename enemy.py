import pygame
import random

class Enemy:
    #TODO: HACER SKIN DE LOS ENEMIGOS
    ENEMY_COLOR = (255, 0, 0)
    
    #constructor del enemigo
    def __init__(self, ENEMY_SIZE, WIDTH, HEIGHT, ENEMY_SPEED, screen):

        self.ENEMY_SIZE = ENEMY_SIZE
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.SPEED = ENEMY_SPEED
        self.screen = screen
        

        # posicion random del enemigo cuando spawnea
        self.x = random.randint(0, WIDTH - self.ENEMY_SIZE)
        self.y = random.randint(0, HEIGHT - self.ENEMY_SIZE)

        # elige direccion random del enemigo (siempre la misma velocidad)
        self.vx = random.choice([-2, 2])
        self.vy = random.choice([-2, 2])

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
        pygame.draw.rect(self.screen, self.ENEMY_COLOR, (self.x, self.y, self.ENEMY_SIZE, self.ENEMY_SIZE))

    def get_position(self):
        return [self.x, self.y]
