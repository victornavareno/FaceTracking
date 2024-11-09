# AUTHOR: Victor Navareño 2024
# Computer Vision - Face Tracking arcade game using OpenCV and MediaPipe
# DESCRIPTION: This is the main file for the game. It contains the main game loop and the logic. SAVE THE F*CKING WORLD.
# LICENSE: MIT

import pygame
import sys
import cv2
import numpy as np
import mediapipe as mp
from entities import asteroid

pygame.init()

# VARIABLES GLOBALES
WIDTH, HEIGHT = 1200, 900  # tamaño del frame a crear

# COLORES
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# TAMAÑO DEL JUGADOR Y asteroide
PLAYER_SIZE = 70
ASTEROID_SIZE = 50
ASTEROID_SPEED = 3  # velocidad de los asteroides

# Lista de posiciones recientes de la nariz para suavizar el movimiento del jugador
nose_positions = []
SMOOTHING_FACTOR = 5  # Número de posiciones recientes para calcular el promedio
######################

### CARGANDO ASSETS ###
font_small = pygame.font.Font("fonts/SPACE.ttf", 30)  
font_medium = pygame.font.Font("fonts/SPACE.ttf", 45)  
font_large = pygame.font.Font("fonts/SPACE.ttf", 60)
#######################
# ASSET EARTH 
earth_image = pygame.image.load("img/earth.png")
earth_image = pygame.transform.scale(earth_image, (PLAYER_SIZE * 2, PLAYER_SIZE * 2))

# ASSET ASTEROID
asteroid_image = pygame.image.load("img/asteroid.png")
asteroid_image = pygame.transform.scale(asteroid_image, (ASTEROID_SIZE * 5, ASTEROID_SIZE * 5))

# cargo imagen background A FUEGOOOOOOO
loading_screen = pygame.image.load("img/LOADING_SCREEN.png")
loading_screen = pygame.transform.scale(loading_screen, (WIDTH, HEIGHT))
#########################
space_background = pygame.image.load("img/BACKGROUND.png")
space_background = pygame.transform.scale(space_background, (WIDTH, HEIGHT))
#########################

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SAVE THE F*CKING WORLD")

# inicializo el reloj del juego y la camara con opencv
clock = pygame.time.Clock() # inicializo el reloj del juegog
cap = cv2.VideoCapture(0)  # 0 se refiere a la camara por defecto

# inicializo el modelo de deteccion de rostros con mediapipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

def display_loading_screen():
    screen.blit(loading_screen, (0, 0))
    pygame.display.update()
    pygame.time.delay(3000)  # muestrala pantalla de carga durante3 segundos

def detect_collision(player_pos, asteroid_pos):
    px, py = player_pos
    ax, ay = asteroid_pos
    return (ax < px < ax + ASTEROID_SIZE or ax < px + PLAYER_SIZE < ax + ASTEROID_SIZE) and \
           (ay < py < ay + ASTEROID_SIZE or ay < py + PLAYER_SIZE < ay + ASTEROID_SIZE)

def check_collisions(player_pos, asteroids):
    for asteroid in asteroids:
        if detect_collision(player_pos, asteroid.get_position()):
            return True
    return False

# DESCOMENTAR ESTE METODO PARA UN TRACKING SIN SUAVIZADO
# def handle_player_position(results):

#     # Posicion inicial del jugador si no detecta la nariz
#     player_pos = (WIDTH // 2, HEIGHT // 2)

#     # actualizo basado en posicion d ela nariz
#     if results.multi_face_landmarks:
#         for face_landmarks in results.multi_face_landmarks:
#             nose_tip = face_landmarks.landmark[1]
#             nose_x = int((1 - nose_tip.x) * WIDTH)
#             nose_y = int(nose_tip.y * HEIGHT)
#             player_pos = ((nose_x - 30), (nose_y - 30))
#             break
#     return player_pos


# EL METODO ANTERIOR HACE QUE EL TRACKING DE LA IMAGEN SEA BASTANTE IRREGULAR
def handle_player_position(results):
    player_pos = (WIDTH // 2, HEIGHT // 2)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            nose_tip = face_landmarks.landmark[1]
            nose_x = int((1 - nose_tip.x) * WIDTH)
            nose_y = int(nose_tip.y * HEIGHT)

            # Añade la posición actual de la nariz a la lista
            nose_positions.append((nose_x, nose_y))

            # Limita el tamaño de la lista para mantener las últimas N posiciones
            if len(nose_positions) > SMOOTHING_FACTOR:
                nose_positions.pop(0)

            # Calcula el promedio de las posiciones recientes de la nariz
            avg_nose_x = sum([pos[0] for pos in nose_positions]) // len(nose_positions)
            avg_nose_y = sum([pos[1] for pos in nose_positions]) // len(nose_positions)

            # Ajusta la posición del jugador usando la posición suavizada
            player_pos = ((avg_nose_x - 30), (avg_nose_y - 30))
            break

    return player_pos


def initialize_asteroids(round_number):
    num_asteroids = 4 + 2 * (round_number - 1)
    return [asteroid.Asteroid(ASTEROID_SIZE, WIDTH, HEIGHT, ASTEROID_SPEED, screen, asteroid_image) for _ in range(num_asteroids)]

# ES UN LIO ESTE METODO PERO FUNCIONA (hacksssss)
def display_countdown(round_number, asteroids):
    countdown_duration = 3000  # 3 segundos de game start
    start_time = pygame.time.get_ticks()

    while True:
        # INICIO LA CUENTA ATRSA
        elapsed_time = pygame.time.get_ticks() - start_time
        remaining_time = max(0, countdown_duration - elapsed_time)
        count = remaining_time // 1000 + 1

        if remaining_time <= 0:
            break

        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame from camera.")
            break

        # REESCALADO DE LA IMAGEN 
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame_surface = pygame.surfarray.make_surface(np.rot90(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))

        # OVERLAY DE LA CAMARA EN EL FONDO (MAS DE 230 HACE QUE NO SE VE AL JUG, SOLO ALL PLANETA)
        screen.blit(frame_surface, (0, 0))

        #####################
        # AQUI SE AJUSTA LA TRANSPARENCIA DE LA CAMARA
        #space_background.set_alpha(220)  # ajusta la transparencia aqui TRANSPARENCY ADJUSTMENT
        space_background.set_alpha(300)  # THE PLAYER ISNT SEEN WITH THIS SETTING
        #####################

        screen.blit(space_background, (0, 0))

        # dibujo los asteroides quietos en la pantalla antes de iniciar la ronda
        for asteroid in asteroids:
            asteroid.draw()

        countdown_text = font_medium.render(f"ROUND {round_number} STARTING IN {count}...", True, WHITE)
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))

        pygame.display.update()
        clock.tick(30)

def run_round(round_number):
    asteroids = initialize_asteroids(round_number)
    round_time = 20000  # 20 SEGUNDOS // SERA LA DURACION DE LA RONDA
    round_start_time = pygame.time.get_ticks()

    # CAPUTRO EL FRAME DE LA CAMARA
    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)
        player_pos = handle_player_position(results)
    else:
        player_pos = (WIDTH // 2, HEIGHT // 2)

    display_countdown(round_number, asteroids)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                cap.release()
                sys.exit()

        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame from camera.")
            break

        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = face_mesh.process(frame_rgb)
        player_pos = handle_player_position(results)

        frame_surface = pygame.surfarray.make_surface(np.rot90(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        screen.blit(frame_surface, (0, 0))
        screen.blit(space_background, (0, 0))

        if check_collisions(player_pos, asteroids):
            pygame.display.update()
            pygame.time.delay(2000)
            return False

        # este lio para que ell jugador quede centrado en la nariz y no ladeado abjo derecha (hackssssssssssssssss)
        earth_width, earth_height = earth_image.get_size()
        earth_x = player_pos[0] + PLAYER_SIZE / 2 - earth_width / 2
        earth_y = player_pos[1] + PLAYER_SIZE / 2 - earth_height / 2
        screen.blit(earth_image, (earth_x, earth_y))

        elapsed_time = pygame.time.get_ticks() - round_start_time

        if elapsed_time >= 3000:
            for asteroid in asteroids:
                asteroid.move()
                asteroid.draw()

        if elapsed_time >= round_time:
            return True

        round_text = font_small.render(f"Round: {round_number}", True, WHITE)
        time_text = font_small.render(f"Time: {round_time // 1000 - elapsed_time // 1000}", True, WHITE)
        screen.blit(round_text, (WIDTH//2 - round_text.get_width() //2, 20))
        screen.blit(time_text, (WIDTH//2 - time_text.get_width() //2, 50))
        
        pygame.display.update()
        clock.tick(30)

def main_game():
    display_loading_screen()
    round_number = 1
    while True:
        survived = run_round(round_number)
        if not survived:
            break
        round_number += 1

    # TEXTOS DE PANTALLA FINAL
    text_gameover = font_large.render("GAME OVER", True, WHITE)
    # pa imprimir las rondas que sobreviviste
    if round_number == 1:
        text_game_stats = font_medium.render(f"You survived: {round_number} round", True, WHITE)
    else:
        text_game_stats = font_medium.render(f"You survived: {round_number} rounds", True, WHITE)

    # horrible me lo ha hecho chatgpt y funciona
    screen.blit(text_game_stats, (WIDTH // 2 - text_game_stats.get_width() // 2, (HEIGHT // 2 - text_game_stats.get_height() // 2) + 90)).scale_by(6)
    screen.blit(text_gameover, (WIDTH // 2 - text_gameover.get_width() // 2, HEIGHT // 2 - text_gameover.get_height() // 2)).scale_by(6)
    ############################

    pygame.display.update()
    pygame.time.delay(5000)


main_game();

cap.release()
pygame.quit()
sys.exit()