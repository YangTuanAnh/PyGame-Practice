import pygame
from pygame import mixer
import random
import math

# Initilize the game
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.png")

# Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("gift-box.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("shuttle.png")
playerX = 360
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("monster.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet

# Ready - you can't see the bullet
# Fire - the bullet is currently being fired
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg[0], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX-bulletX)**2 + (enemyY-bulletY)**2)
    if distance < 27:
        return True
    return False


# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    game_over = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over, (250, 250))


# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    playerX += playerX_change

    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] >= 480:
            for i in range(num_of_enemies):
                enemyY[i] = 480
            game_over_text()
            break

        # Enemy movement
        enemyX[i] += enemyX_change[i]

        if enemyX[i] < 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
            explosion = mixer.Sound("explosion.wav")
            explosion.play()

        enemy(enemyX[i], enemyY[i])

    # Bullet movement
    if bulletY < -64:
        bullet_state = "ready"
        bulletY = 480

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
