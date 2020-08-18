import pygame
import math

from pygame import mixer

# Initialize pygame
pygame.init()

# create the screen
height = 800
width = 600
screen = pygame.display.set_mode((height, width))

# FPS
clock = pygame.time.Clock()
FPS = 144

# background
background = pygame.image.load("background.png")

# background sound
mixer.music.load('background_final.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('space-invaders.png')
pygame.display.set_icon(icon)

# PLayer
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
player_speed = 4

# Enemy
"""
enemyImg = []
enemyX = []
enemyY = []
enemy_speed = []
enemyX_change = []
enemyY_change = []
enemyChanges = []
enemyY_variable = []
"""

enemyImg = pygame.image.load('alien.png')
enemyX = 370
enemyY = 20
enemy_speed = 4
enemyX_change = enemy_speed
enemyY_change = 0
enemyChanges = 0
enemyY_variable = 0



# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 7
bullet_state = "ready"

score = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:

    clock.tick(FPS)
    # RGB
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change += -player_speed

            elif event.key == pygame.K_RIGHT:
                playerX_change += +player_speed

            elif event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_change += player_speed

            elif event.key == pygame.K_RIGHT:
                playerX_change += -player_speed

    playerX += playerX_change

    # Enemy movement
    if enemyX <= 0:
        enemyX_change = enemy_speed
        enemyChanges += 1

    elif enemyX >= 736:
        enemyX_change = -enemy_speed
        enemyChanges += 1

    elif enemyChanges == 1:
        enemyX_change = 0
        enemyY_change = +enemy_speed
        enemyChanges = 0

    elif enemyY >= (enemyY_variable + 32):
        enemyY_variable = enemyY
        enemyY_change = 0
        if enemyX <= 2:
            enemyX_change = enemy_speed
        elif enemyX >= 734:
            enemyX_change = -enemy_speed

    enemyX += enemyX_change
    enemyY += enemyY_change

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Collision
    collision = is_collision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        explosion_sound = mixer.Sound('explosion_final.wav')
        explosion_sound.play()
        bulletY = 480
        bullet_state = "ready"
        score += 1
        print(score)
        enemyX = 370
        enemyY = 20
        enemyY_variable = 0

    # Player screen boundaries
    if playerX < -64:
        playerX = 800
    elif playerX > 800:
        playerX = -64

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
