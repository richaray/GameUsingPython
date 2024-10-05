import pygame
import math
import random
from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Backgrounds
background_level_1 = pygame.image.load('20252.png')
background_level_2 = pygame.image.load('51796.png')

# Initial background music
mixer.music.load('Background_FA.mp3')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Fruit Attack")
icon = pygame.image.load('001-arcade-game.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('001-tank.png')
playerX = 370
playerY = 480
playerX_change = 0

# Bullet
bulletImg = pygame.image.load('001-bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.5
bullet_state = "ready"

# Score and level variables
score_value = 0
level = 1  # Start with level 1
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Enemy data
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

def reset_level_1_enemies():
    global enemyImg, enemyX, enemyY, enemyX_change, enemyY_change
    num_of_enemies = 2  # Set to 2 enemies for level 1
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('006-angry-face-1.png'))
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(0.3)
        enemyY_change.append(40)


def reset_level_2_enemies():
    global enemyImg, enemyX, enemyY, enemyX_change, enemyY_change
    num_of_enemies = 6  # Set to 6 enemies for level 2
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('006-angry-face-1.png'))
        enemyImg.append(pygame.image.load('001-pumpkin.png'))
        enemyImg.append(pygame.image.load('002-fruit.png'))
        enemyImg.append(pygame.image.load('003-fruit-1.png'))
        enemyImg.append(pygame.image.load('004-fruit-2.png'))
        enemyImg.append(pygame.image.load('005-angry-face.png'))
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(0.05)  # Faster movement for level 2
        enemyY_change.append(10)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_level(x, y):
    level_text = font.render("Level: " + str(level), True, (255, 255, 255))
    screen.blit(level_text, (x, y + 40))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    play_again_text = font.render("Press ENTER to Play Again", True, (255, 255, 255))
    screen.blit(play_again_text, (200, 350))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    return False


def transition_to_level_2():
    global level
    level = 2
    reset_level_2_enemies()

    # Change the background music
    mixer.music.stop()
    mixer.music.load('Background_FA.mp3')
    mixer.music.play(-1)


def restart_game():
    global score_value, level, playerX, playerY, bulletY, bullet_state, game_over
    score_value = 0
    level = 1
    playerX = 370
    playerY = 480
    bulletY = 480
    bullet_state = "ready"
    reset_level_1_enemies()  # Reset enemies for level 1
    game_over = False
    mixer.music.load('Background_FA.mp3')  # Restart music for level 1
    mixer.music.play(-1)


# Game Loop
running = True
game_over = False
reset_level_1_enemies()  # Initial setup of enemies for level 1

while running:

    # Change the background based on level
    if level == 1:
        screen.blit(background_level_1, (0, 0))
    else:
        screen.blit(background_level_2, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not game_over:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT and not game_over:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE and not game_over:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

            # If the game is over, allow the player to restart or quit
            if event.key == pygame.K_RETURN and game_over:
                restart_game()

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT) and not game_over:
                playerX_change = 0

    if not game_over:
        # checking for boundaries of spaceship so it doesn't go out of bounds
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy Movement
        for i in range(len(enemyX)):
            if enemyY[i] > 440:
                # When the player loses, stop the game and show the "Game Over" screen
                for j in range(len(enemyX)):
                    enemyY[j] = 2000  # Move all enemies off-screen
                game_over = True

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 0.3 if level == 1 else 0.2
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -0.3 if level == 1 else -0.2
                enemyY[i] += enemyY_change[i]

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_Sound = mixer.Sound('explosion.wav')
                explosion_Sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        # Bullet Movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        # Check if the player reaches score 3, then move to level 2
        if score_value >= 3 and level == 1:
            transition_to_level_2()

        player(playerX, playerY)
        show_score(textX, textY)
        show_level(textX, textY)

    else:
        # Display the Game Over screen when the game is over
        game_over_text()

    pygame.display.update()

pygame.quit()
