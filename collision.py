def detect_collision(player_pos, asteroid_pos):
    px, py = player_pos
    ax, ay = asteroid_pos
    return (ax < px < ax + 50 or ax < px + 70 < ax + 50) and \
           (ay < py < ay + 50 or ay < py + 70 < ay + 50)

def check_collisions(player_pos, asteroids):
    for asteroid in asteroids:
        if detect_collision(player_pos, asteroid.get_position()):
            return True
    return False
