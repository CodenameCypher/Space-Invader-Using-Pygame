import pygame
from pygame import mixer
import random
import math
import time

#initializing pygame
pygame.init()
mainscreen = pygame.display.set_mode((800, 600))

#Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('images/icon.ico')
pygame.display.set_icon(icon)

#BG Image
bgImage = pygame.image.load('images/bgImg.png')

#Player image
playerImg = pygame.image.load('images/player.png')
playerX = 370
playerY = 480
playerXChange = 0
playerYChange = 0

#Bullet image
bulletImg = pygame.image.load('images/bullet.png')
bulletX = playerX
bulletY = playerY
bulletYChange = 7
bulletState = 'ready'

#Enemy image
enemyImg = []
enemyX = []
enemyY = []
enemyXChange = []
enemyYChange = []
number_Enemies = 5
for i in range(number_Enemies):
    enemyImg.append(pygame.image.load('images/enemy.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(0,200))
    enemyXChange.append(random.uniform(0.5,2.5))
    enemyYChange.append(random.randint(19,27))

#score
score = 0
font = pygame.font.Font('fonts/Neuterous.otf',32)
scoreX = 10
scoreY = 10

#game over
gameOverfont = pygame.font.Font('fonts/Spooky Haunt.otf',50)
gameX = 400
gameY = 300

#button play again
playAgain = pygame.font.Font('fonts/Neuterous.otf',35)
playAgainX = 350
playAgainY = 370

#quit text
quitText = pygame.font.Font('fonts/Neuterous.otf',35)
quitX = 410
quitY = 430

def quitText(x,y):
    s = playAgain.render("Quit",True,(255,255,255))
    # pygame.draw.rect(mainscreen,(170,170,170),[x,y,90,50])
    mainscreen.blit(s,(x,y))

def playAgainText(x,y):
    s = playAgain.render("Play Again",True,(255,255,255))
    # pygame.draw.rect(mainscreen,(170,170,170),[350,370,220,50])
    mainscreen.blit(s,(x,y))

def gameOverText(x,y):
    s = gameOverfont.render("GAME OVER",True,(255,255,255))
    mainscreen.blit(s,(x,y))

def showScore(x,y):
    s = font.render("Score : "+str(score),True,(255,255,255))
    mainscreen.blit(s,(x,y))

def player(x,y):
    mainscreen.blit(playerImg,(x,y))

def enemy(x,y,i):
    mainscreen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bulletState
    bulletState = 'fire'
    mainscreen.blit(bulletImg,(x+16,y+10))

def isCollision(eX, eY, bX, bY):
    distance = math.sqrt(math.pow(eX-bX,2)+math.pow(eY-bY,2))
    if distance < 27:
        return True
    else:
        return False

def isCollisionWithPlayer(eX, eY, pX, pY):
    distance = math.sqrt(math.pow(eX-pX,2)+math.pow(eY-pY,2))
    if distance < 40:
        return True
    else:
        return False

#Game loop
running = True
while running:
    mainscreen.fill((23,23,23))
    mainscreen.blit(bgImage,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if 350 <= mouse[0] <= 570 and 370 <= mouse[1] <= 420:
                score = 0
                playerX = 370
                playerY = 480
                running = True
            if quitX <= mouse[0] <= 500 and quitY <= mouse[1] <= quitY + 50:
                running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXChange = -0.8
            if event.key == pygame.K_RIGHT:
                playerXChange = +0.8
            if event.key == pygame.K_UP:
                playerYChange = -0.8
            if event.key == pygame.K_DOWN:
                playerYChange = +0.8
            if event.key == pygame.K_SPACE:
                bulletSound = mixer.music.load('sounds/shoot.wav')
                if bulletState is 'ready':
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX,playerY)
                    mixer.music.set_volume(0.5)
                    mixer.music.play(1)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXChange = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerYChange = 0

    #mouse movement
    mouse = pygame.mouse.get_pos()

    if score >= 20 or score <= -10:
        if 350 <= mouse[0] <= 570 and 370 <= mouse[1] <= 420:
            pygame.draw.rect(mainscreen,(110,110,110),[350,370,220,50])
        else:
            pygame.draw.rect(mainscreen,(170,170,170),[350,370,220,50])
        if quitX <= mouse[0] <= 500 and quitY <= mouse[1] <= quitY + 50:
            pygame.draw.rect(mainscreen,(100,100,100),[quitX,quitY,90,50])
        else:
            pygame.draw.rect(mainscreen,(170,170,170),[quitX,quitY,90,50])

    #player movement
    playerX += playerXChange
    playerY += playerYChange
    if playerX < 0 : 
        playerX = 0
    if playerY < 0 :
        playerY = 0
    if playerX > 736:
        playerX = 736
    if playerY > 536:
        playerY = 536
    if playerY < 0:
        playerY = 0

    #enemy loop
    for i in range(number_Enemies):
        if score >= 20 or score <=-10:
            gameOverText(gameX,gameY)
            playAgainText(playAgainX,playAgainY)
            quitText(quitX,quitY)
            break

        enemyX[i] += enemyXChange[i]

        if enemyX[i] < 0 : 
            enemyX[i] = 0
            enemyXChange[i] *= -1
            enemyY[i] += enemyYChange[i]
        if enemyX[i] > 736:
            enemyX[i] = 736
            enemyXChange[i] *= -1
            enemyY[i] += enemyYChange[i]

        if isCollision(enemyX[i],enemyY[i],bulletX,bulletY):
            bulletState = 'ready'
            bulletX = playerX
            bulletY = playerY
            score += 1
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(0,200)
            dead = mixer.music.load('sounds/dead.wav')
            mixer.music.set_volume(0.5)
            mixer.music.play(1)


        if isCollisionWithPlayer(enemyX[i],enemyY[i],playerX,playerY):
            score -= 5
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(0,200)
            error = mixer.music.load('sounds/error.wav')
            mixer.music.set_volume(0.5)
            mixer.music.play(1)

        enemy(enemyX[i],enemyY[i],i)
    #enemy loop ends

    #bullet boundaries
    if bulletY < 0 :
        bulletY = playerY
        bulletX = playerX
        bulletState = 'ready'
    if bulletState is 'fire':
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletYChange


    player(playerX,playerY) #creating and updating the player
    showScore(scoreX,scoreY) #creating and updating the score
    pygame.display.update()
#gameloop ends