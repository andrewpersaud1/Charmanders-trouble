import pygame
import math
import random
from pygame import mixer

# initializes the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 800))

# background
background = pygame.image.load('background.png')

#sound in the background
mixer.music.load('pokemon battle.wav')
mixer.music.play(-1)


# Title and icon
pygame.display.set_caption("Charmander's trouble")
icon = pygame.image.load('fire.png')
pygame.display.set_icon(icon)

# player
Charmander = pygame.image.load('charmander.png')
charX = 370
charY = 600
charX_change = 0
charY_change =0

# enemy
Squirtle = []
squirtX = []
squirtY = []
squirtX_change = []
squirtY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    Squirtle.append(pygame.image.load('flat squirtle.png'))
    squirtX.append(random.randint(0, 735))
    squirtY.append(random.randint(50, 150))
    squirtX_change.append(3)
    squirtY_change.append(40)

# charmander attack
fire = pygame.image.load('fire.png')
fireX = 0
fireY = 480
fireX_change = 0
fireY_change = 10
fire_status = 'ready'

# tracker
score_progression = 0
font = pygame.font.Font('Adriana Italic.ttf', 80)
scoreX = 600
scoreY = 10




def score_tracker(x, y):
    score = font.render("score :" + str(score_progression), True, (0, 0, 0))
    screen.blit(score, (x, y))


def Mand(x, y):
    screen.blit(Charmander, (x, y))


def squirt(x, y, i):
    screen.blit(Squirtle[i], (x, y))


def ember(x, y):
    global fire_status
    fire_status = "launch"
    screen.blit(fire, (x + 16, y + 10))


def impact(squirtX, squirtY, fireX, fireY):
    distance = math.sqrt((math.pow(squirtX - fireX, 2)) + (math.pow(squirtY - fireY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:

    # RGB- red green blue
    screen.fill((0, 100, 255))
    # this displays the background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                charX_change = -5
            if event.key == pygame.K_RIGHT:
                charX_change = 5
            if event.key == pygame.K_UP:
                charY_change = -5
            if event.key == pygame.K_DOWN:
                charY_change = 5
            if event.key == pygame.K_SPACE:
                if fire_status is "ready":
                    fireX = charX
                    ember(fireX, fireY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                charX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                charY_change = 0
    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1
    charX += charX_change
    if charX <= 0:
        charX = 0
    elif charX >= 740:
        charX = 740
    charY += charY_change
    if charY <= 0:
        charY = 0
    elif charY >= 740:
        charY = 740

    # squirtle's moves
    for i in range(num_of_enemies):
        if squirtY[i] > 400:
            for j in range(num_of_enemies):
                    squirtY[j] = 2000


        squirtX[i] += squirtX_change[i]
        if squirtX[i] <= 0:
            squirtX_change[i] = 1
            squirtY[i] += squirtY_change[i]
        elif squirtX[i] >= 740:
            squirtX_change[i] = -1
            squirtY[i] += squirtY_change[i]

        # impact
        hitsTarget = impact(squirtX[i], squirtY[i], fireX, fireY)
        if hitsTarget:
            fireY = 480
            fire_status = "ready"
            ember_hit= mixer.Sound('slap.wav')
            ember_hit.play()
            score_progression += 1
            squirtX[i] = random.randint(0, 800)
            squirtY[i] = random.randint(50, 150)

        squirt(squirtX[i], squirtY[i], i)

    # launch process
    if fireY <= 0:
        fireY = 480
        fire_status = "ready"

    if fire_status is "launch":
        ember(fireX, fireY)
        fireY -= fireY_change

    Mand(charX, charY)
    score_tracker(scoreX, scoreY)
    pygame.display.update()
