import pygame
import random
import math
from pygame import mixer
#initialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800, 600))
 #BACKGROUND IMAGE
background = pygame.image.load('background.png')

#background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#TITLE
pygame.display.set_caption("ALiEn ShOoT")

#caption
icon = pygame.image.load('balloon.png')
pygame.display.set_icon(icon)

#PLAYER
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

def player(x,y):
   #For draw the image
    screen.blit(playerImg, (x, y))

#enemy
enemyImg = [] #Multiple enemy
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):

    enemyImg.append(pygame.image.load('ufo.png'))
    #random place show the enemy
    enemyX.append(random.randint(0, 749))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(10)

def enemy(x,y,i):
   #For draw the image
 screen.blit(enemyImg[i], (x, y))


#Bullet
bulletImg = pygame.image.load('bullet.png')

bulletX = 2
bulletY = 480
bulletX_change = 0
bulletY_change = 3
bullet_state = "ready" #ready-can't see bullet, Fire-bullet moving
def fire_bullet(x,y):
   #For draw the image
   global bullet_state
   bullet_state="fire"
   screen.blit(bulletImg, (x+20, y+10))


#SCORE
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

def show_score(x,y):
  score = font.render("Score: "+str(score_value), True, (255,255, 255))
  screen.blit(score, (x, y))

#game over
over_font = pygame.font.Font('freesansbold.ttf', 64)
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200, 250))


def isCollision(enemyX, enemyY, bulletX, bulletY):
  distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY, 2)))
  if distance < 27:
      return True
  else:
      return False


#GAME LOOP
running = True
while running:
    #RGB = Red,green,blue
    screen.fill((0, 0, 0))
    #backgrond image always show
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #keystroke is pressed check whether its right or left
        if event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.8
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.8
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type ==pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
 #Boundary so that the spaceship never go outside the border
    if playerX<=0:
        playerX = 0
    elif playerX >= 700:
        playerX = 700

#enemy movement

    # Boundary so that the enemy never go outside the border
    for i in range(num_of_enemies):

        #game OVER
        if enemyY[i] >400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 750:
            enemyX_change[i] = -1.2
            enemyY[i] += enemyY_change[i]

        # COllision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explotion_sound = mixer.Sound('explosion.wav')
            explotion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            enemyX[i] = random.randint(0, 749)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    #Bullet movement
    if bulletY<=0:
        bulletY = 500
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()