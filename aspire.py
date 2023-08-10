#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame, sys

from pygame.locals import *

from random import randint

import math

import time

# QBERT

# make the window

pygame.init()

winScreen = pygame.display.set_mode((1024, 768), 0, 32)

pygame.display.set_caption('Q*bert')

# declare commonly used colors

clrLightBlue = pygame.Color(0, 200, 200)

clrBlack = pygame.Color(0, 0, 0)

clrBlue = pygame.Color(0, 0, 255)

clrRed = pygame.Color(255, 0, 0)

clrWhite = pygame.Color(255, 255, 255)

clrBlack = pygame.Color(0, 0, 0)

clrYellow = pygame.Color(255, 255, 0)

# declare images(load some images)

imgPlayerDownLeft = '/Users/estellaliu/Desktop/qbertproject/playerleftdown.png'

imgPlayerDownRight = '/Users/estellaliu/Desktop/qbertproject/playerrightdown.png'

imgPlayerDownRightLives = '/Users/estellaliu/Desktop/qbertproject/playerlittle.png'

imgPlayerUpLeft = '/Users/estellaliu/Desktop/qbertproject/playerupleft.png'

imgPlayerUpRight = '/Users/estellaliu/Desktop/qbertproject/playerupright.png'

imgPlayerDownLeftJump = '/Users/estellaliu/Desktop/qbertproject/playerleftdownjump.png'

imgPlayerDownRightJump = '/Users/estellaliu/Desktop/qbertproject/playerdownrightjump.png'

imgPlayerUpLeftJump = '/Users/estellaliu/Desktop/qbertproject/playerupleftJump.png'

imgPlayerUpRightJump = '/Users/estellaliu/Desktop/qbertproject/playeruprightjump.png'

imgPlayer = '/Users/estellaliu/Desktop/qbertproject/playerleftdown.png'

imgRedBall = '/Users/estellaliu/Desktop/qbertproject/redEnemyBall.png'

imgGreenBall = '/Users/estellaliu/Desktop/qbertproject/greenEnemyBall.png'

imgNothingBall = '/Users/estellaliu/Desktop/qbertproject/nothingEnemyBall.png'

imgPlayerSwear = '/Users/estellaliu/Desktop/qbertproject/swearQbert.png'

imgPlayerSpindownleft = '/Users/estellaliu/Desktop/qbertproject/downleftspin.png'

imgPlayerSpindownright = '/Users/estellaliu/Desktop/qbertproject/downrightspin.png'

imgDisk = '/Users/estellaliu/Desktop/qbertproject/disk.png'

imgPurpleBall = '/Users/estellaliu/Desktop/qbertproject/purpleEnemyBall.png'

# imgPurpleBall= 'RedEnemyBall.png'

imgSnake = '/Users/estellaliu/Desktop/qbertproject/snake.png'

imgLose = pygame.image.load('/Users/estellaliu/Desktop/qbertproject/qbertloses.png')

imgStart = pygame.image.load('/Users/estellaliu/Desktop/qbertproject/startscreenqbert.jpg')

imgWin = pygame.image.load('/Users/estellaliu/Desktop/qbertproject/qbertloses.png')

PlayerSwear = pygame.image.load(imgPlayerSwear).convert_alpha()

Livesigns = pygame.image.load(imgPlayerDownRightLives).convert_alpha()

PlayerSpin = pygame.image.load(imgDisk)

# print("output\n")

# create mixers and load sounds

pygame.mixer.pre_init(44100, -16, 2, 2048)

sndQBJump = pygame.mixer.Sound('/Users/estellaliu/Desktop/qbertproject/jump1.wav')  # load sound

sndQBDeath1 = pygame.mixer.Sound('/Users/estellaliu/Desktop/qbertproject/jump1.wav')  # load sound

sndQBDeath2 = pygame.mixer.Sound('/Users/estellaliu/Desktop/qbertproject/jump1.wav')  # load sound

sndQBWin = pygame.mixer.Sound('/Users/estellaliu/Desktop/qbertproject/jump1.wav')  # load sound

sndEnemyJump = pygame.mixer.Sound('/Users/estellaliu/Desktop/qbertproject/jump2.wav')

sndQBStart = pygame.mixer.Sound('/Users/estellaliu/Desktop/qbertproject/gamestart.wav')

print("output\n")

lives = 3

term = 0

totalScore = 0

myfont = pygame.font.SysFont("Britannic Bold", 40)


class ball:
    from random import randint

    import math

    def __init__(self):

        # create the ball and set color pattern, and initial position, then blit on screen

        self.color = randint(0, 1)

        self.position = randint(0, 1)

        if self.position == 0:

            self.x = 410

            self.y = 110

        elif self.position == 1:

            self.x = 510

            self.y = 110

        if self.color == 0:

            self.image = pygame.image.load(imgRedBall).convert_alpha()

        else:

            self.image = pygame.image.load(imgGreenBall).convert_alpha()

        self.pattern = randint(0, 3)

        winScreen.blit(self.image, (self.x, self.y))

    def collision(self):

        # check collision: if distance is < 60 return true

        Bool = False

        if math.sqrt((self.x - PlayerX) ** 2 + (self.y - PlayerY) ** 2) < 60:
            Bool = True

        return Bool

    # move the ball based on the pattern it was assigned, put new ball on the screen

    def update(self):

        global loop

        global term

        global sndEnemyJump

        if self.y < 520:

            # move the ball and play jump sound until its y > 520, , move the ball based on the pattern it was assigned, put new ball on the screen

            # straight downleft

            if self.pattern == 0:

                if (loop + 5) % 10 == 0:
                    self.x -= 50

                    self.y += 80

                    sndEnemyJump.play()

            # straigt downright

            elif self.pattern == 1:

                if (loop + 5) % 10 == 0:
                    self.x += 50

                    self.y += 80

                    sndEnemyJump.play()

            # alternate down left and right

            elif self.pattern == 2:

                if (loop + 5) % 10 == 0:

                    self.y += 80

                    sndEnemyJump.play()

                    term += 1

                    if term % 2 == 0:

                        self.x += 50

                        sndEnemyJump.play()

                    else:

                        self.x -= 50

                        sndEnemyJump.play()

            else:

                # default:alternate down right and left

                if (loop + 5) % 10 == 0:

                    self.y += 80

                    sndEnemyJump.play()

                    term += 1

                    if term % 2 == 0:

                        self.x -= 50

                        sndEnemyJump.play()

                    else:

                        self.x += 50

                        sndEnemyJump.play()

        else:

            # if passed 520 set image to nothing

            self.image = pygame.image.load(imgNothingBall).convert_alpha()

        winScreen.blit(self.image, (self.x, self.y))


class purple:
    global loop

    global PlayerX

    global PlayerY

    def __init__(self):

        # creat the purpleball and give it a location

        self.snakeimg = False

        self.x = 460

        self.y = 190

        self.image = pygame.image.load(imgPurpleBall).convert_alpha()

        winScreen.blit(self.image, (self.x, self.y))

    def update(self):

        # only check self.x once and keep using the snake image

        if self.x >= 660:
            self.snakeimg = True

        # change the purple ball image to snake image once the ball arrives a certain position

        if self.snakeimg == True:

            if (loop + 5) % 20 == 0:

                if self.y > 510:

                    self.image = pygame.image.load(imgNothingBall).convert_alpha()

                else:

                    self.image = pygame.image.load(imgSnake).convert_alpha()

                    if self.x <= PlayerX and self.y >= PlayerY:

                        self.x += 50

                        self.y -= 80

                        sndEnemyJump.play()

                    elif self.x <= PlayerX and self.y <= PlayerY:

                        self.x += 50

                        self.y += 80

                        sndEnemyJump.play()

                    elif self.x > PlayerX and self.y < PlayerY:

                        self.x -= 50

                        self.y += 80

                        sndEnemyJump.play()

                    elif self.x > PlayerX and self.y > PlayerY:

                        self.x -= 50

                        self.y -= 80

                        sndEnemyJump.play()

        else:

            if (loop + 5) % 10 == 0:
                self.x += 50

                self.y += 80

                sndEnemyJump.play()

        winScreen.blit(self.image, (self.x, self.y))

    def collision(self):

        # define a collision function under the purple ball

        Bool = False

        if math.sqrt((self.x - PlayerX) ** 2 + (self.y - PlayerY) ** 2) < 60:
            Bool = True

        return Bool


def spinLeft(PlayerX, PlayerY):
    # check left disk hasnt been used, check distance between qbert and disk, if their colliding do spin animation and return the disk has been spun

    loopspin = 0

    spun = False

    # check distance between qbert and disk

    if math.sqrt((160 - PlayerX) ** 2 + (350 - PlayerY) ** 2) < 60:

        spun = True

        PlayerX = 160

        PlayerY = 350

        imgPlayer = imgPlayerSpindownright

        Player = pygame.image.load(imgPlayer).convert_alpha()

        # gives player a moving path
        while PlayerX < 410:

            loopspin += 5

            if loopspin % 10 == 0:
                PlayerX += 5

                PlayerY -= 8

            winScreen.blit(Player, (PlayerX, PlayerY))

            pygame.display.update()

        # winScreen.fill(clrBlack)

    return spun


def spinRight(PlayerX, PlayerY):
    # check right disk hasnt been used, check distance between qbert and disk, if their colliding do spin animation and return the disk has been spun

    loopspin = 0  # define loopspin， loop rise and spun

    loopRise = 0

    spun = False

    # check distance between qbert and disk

    if math.sqrt((760 - PlayerX) ** 2 + (350 - PlayerY) ** 2) < 60:

        spun = True

        PlayerX = 760

        PlayerY = 350

        imgPlayer = imgPlayerSpindownleft

        Player = pygame.image.load(imgPlayer).convert_alpha()

        # gives player a moving path

        while PlayerX != 480:

            loopspin += 5

            if loopspin % 10 == 0:
                PlayerX -= 5

                PlayerY -= 8

            winScreen.blit(Player, (PlayerX, PlayerY))

            pygame.display.update()

            winScreen.fill(clrBlack)

    return spun


print("Game start\n")

end_it = False
print("Game start\n")

while (end_it == False):

    # start screen shows instructions and waits for player to click on the screen to start the game

    winScreen.fill(clrBlack)

    nlabel2 = myfont.render("Use the 4,6,1,3 on the keypad to move. Light all", 1, clrRed)

    nlabel3 = myfont.render("the panels while avoiding enemys to win.", 1, clrRed)

    nlabel = myfont.render("click anywhere to begin", 1, clrWhite)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            lives = 0

            end_it = True

        if event.type == MOUSEBUTTONDOWN:
            end_it = True

    winScreen.blit(imgStart, (325, 150))

    winScreen.blit(nlabel, (350, 650))

    winScreen.blit(nlabel2, (175, 95))

    winScreen.blit(nlabel3, (200, 120))

    pygame.display.flip()

# starting sound plays

print("Game start\n")

sndQBStart.play()

time.sleep(3)

# set round to 1

round_amt = 1

while lives != 0:

    snakemade = False

    # boolean disks used

    diskUsedleft = False

    diskUsedright = False

    # declare array of balls, and array of positions

    BallList = []

    list_of_positions = []

    # boolean game over-no more lives and player win

    RunGamereal = False

    Win = False

    # set Player initial x and y

    PlayerX = 460

    PlayerY = 30

    # set game loop counter to 0

    loop = 0

    # boolean game running

    RunGame = True

    # while game is running

    while RunGame:

        # creates the very left and right column of the blocks

        for x in range(0, 7):
            pygame.draw.polygon(winScreen, clrBlue, (
            (500 - 50 * x, 50 + 80 * x), (450 - 50 * x, 80 + 80 * x), (500 - 50 * x, 110 + 80 * x),
            (550 - 50 * x, 80 + 80 * x)))

            pygame.draw.polygon(winScreen, clrWhite, (
            (450 - 50 * x, 80 + 80 * x), (500 - 50 * x, 110 + 80 * x), (500 - 50 * x, 160 + 80 * x),
            (450 - 50 * x, 130 + 80 * x)))

            pygame.draw.polygon(winScreen, clrLightBlue, (
            (500 - 50 * x, 110 + 80 * x), (550 - 50 * x, 80 + 80 * x), (550 - 50 * x, 130 + 80 * x),
            (500 - 50 * x, 160 + 80 * x)))

            pygame.draw.polygon(winScreen, clrBlue, (
            (500 + 50 * x, 50 + 80 * x), (450 + 50 * x, 80 + 80 * x), (500 + 50 * x, 110 + 80 * x),
            (550 + 50 * x, 80 + 80 * x)))

            pygame.draw.polygon(winScreen, clrWhite, (
            (450 + 50 * x, 80 + 80 * x), (500 + 50 * x, 110 + 80 * x), (500 + 50 * x, 160 + 80 * x),
            (450 + 50 * x, 130 + 80 * x)))

            pygame.draw.polygon(winScreen, clrLightBlue, (
            (500 + 50 * x, 110 + 80 * x), (550 + 50 * x, 80 + 80 * x), (550 + 50 * x, 130 + 80 * x),
            (500 + 50 * x, 160 + 80 * x)))

        # creates the second left and right column of the blocks

        for x in range(0, 5):
            pygame.draw.polygon(winScreen, clrBlue, (
            (500 - 50 * x, 210 + 80 * x), (450 - 50 * x, 240 + 80 * x), (500 - 50 * x, 270 + 80 * x),
            (550 - 50 * x, 240 + 80 * x)))

            pygame.draw.polygon(winScreen, clrWhite, (
            (450 - 50 * x, 240 + 80 * x), (500 - 50 * x, 270 + 80 * x), (500 - 50 * x, 320 + 80 * x),
            (450 - 50 * x, 290 + 80 * x)))

            pygame.draw.polygon(winScreen, clrLightBlue, (
            (500 - 50 * x, 270 + 80 * x), (550 - 50 * x, 240 + 80 * x), (550 - 50 * x, 290 + 80 * x),
            (500 - 50 * x, 320 + 80 * x)))

            pygame.draw.polygon(winScreen, clrBlue, (
            (500 + 50 * x, 210 + 80 * x), (450 + 50 * x, 240 + 80 * x), (500 + 50 * x, 270 + 80 * x),
            (550 + 50 * x, 240 + 80 * x)))

            pygame.draw.polygon(winScreen, clrWhite, (
            (450 + 50 * x, 240 + 80 * x), (500 + 50 * x, 270 + 80 * x), (500 + 50 * x, 320 + 80 * x),
            (450 + 50 * x, 290 + 80 * x)))

            pygame.draw.polygon(winScreen, clrLightBlue, (
            (500 + 50 * x, 270 + 80 * x), (550 + 50 * x, 240 + 80 * x), (550 + 50 * x, 290 + 80 * x),
            (500 + 50 * x, 320 + 80 * x)))

        # create the third left and right column of the blocks

        for x in range(0, 3):
            pygame.draw.polygon(winScreen, clrBlue, (
            (500 - 50 * x, 370 + 80 * x), (450 - 50 * x, 400 + 80 * x), (500 - 50 * x, 430 + 80 * x),
            (550 - 50 * x, 400 + 80 * x)))

            pygame.draw.polygon(winScreen, clrWhite, (
            (450 - 50 * x, 400 + 80 * x), (500 - 50 * x, 430 + 80 * x), (500 - 50 * x, 480 + 80 * x),
            (450 - 50 * x, 450 + 80 * x)))

            pygame.draw.polygon(winScreen, clrLightBlue, (
            (500 - 50 * x, 430 + 80 * x), (550 - 50 * x, 400 + 80 * x), (550 - 50 * x, 450 + 80 * x),
            (500 - 50 * x, 480 + 80 * x)))

            pygame.draw.polygon(winScreen, clrBlue, (
            (500 + 50 * x, 370 + 80 * x), (450 + 50 * x, 400 + 80 * x), (500 + 50 * x, 430 + 80 * x),
            (550 + 50 * x, 400 + 80 * x)))

            pygame.draw.polygon(winScreen, clrWhite, (
            (450 + 50 * x, 400 + 80 * x), (500 + 50 * x, 430 + 80 * x), (500 + 50 * x, 480 + 80 * x),
            (450 + 50 * x, 450 + 80 * x)))

            pygame.draw.polygon(winScreen, clrLightBlue, (
            (500 + 50 * x, 430 + 80 * x), (550 + 50 * x, 400 + 80 * x), (550 + 50 * x, 450 + 80 * x),
            (500 + 50 * x, 480 + 80 * x)))

            # creat the middle block on the bottom row (there is only one block left over after the above functions

            pygame.draw.polygon(winScreen, clrBlue, ((500, 530), (450, 560), (500, 590), (550, 560)))

            pygame.draw.polygon(winScreen, clrWhite, ((450, 560), (500, 590), (500, 640), (450, 610)))

            pygame.draw.polygon(winScreen, clrLightBlue, ((500, 590), (550, 560), (550, 610), (500, 640)))

        # make a purple ball

        if loop == 120:
            snake = purple()

            snakemade = True

        # frames per second = 30

        iFPS = 30

        fpsClock = pygame.time.Clock()

        # keeps track of events

        for event in pygame.event.get():

            # Player quits->end game loop and lives loop

            if event.type == pygame.QUIT:

                RunGamereal = True

                RunGame = False

            elif event.type == pygame.KEYDOWN:

                # player presses keypad 4->change qberts pic,play player jump sound, move qberts x/y so he moves upright

                if event.key == pygame.K_KP4 or event.key == pygame.K_u:

                    PlayerX -= 50

                    PlayerY -= 80

                    imgPlayer = imgPlayerUpRight

                    sndQBJump.play()

                # player presses keypad 6->change qberts pic,play player jump sound, move qberts x/y so he moves upleft

                elif event.key == pygame.K_KP6 or event.key == pygame.K_o:

                    PlayerX += 50

                    PlayerY -= 80

                    imgPlayer = imgPlayerUpLeft

                    sndQBJump.play()

                # player presses keypad 1->change qberts pic,play player jump sound, move qberts x/y so he moves downleft

                elif event.key == pygame.K_KP1 or event.key == pygame.K_j:

                    imgPlayer = imgPlayerDownLeft

                    PlayerX -= 50

                    PlayerY += 80

                    sndQBJump.play()

                # player presses keypad 3->change qberts pic,play player jump sound, move qberts x/y so he moves downright

                elif event.key == pygame.K_KP3 or event.key == pygame.K_l:

                    imgPlayer = imgPlayerDownRight

                    PlayerX += 50

                    PlayerY += 80

                    sndQBJump.play()

        # set Player Position to the new player xy

        PlayerPosition = (PlayerX, PlayerY)

        # load current image player

        Player = pygame.image.load(imgPlayer).convert_alpha()

        # if left disk hasnt been used

        if diskUsedleft == False:

            # check if player is colliding with left disk

            if spinLeft(PlayerX, PlayerY):
                # if player spinleft returns true, set player xy to top block and set left disk to has been used

                PlayerX = 460

                PlayerY = 30

                diskUsedleft = True

        # same has above if statement but for right disk

        if diskUsedright == False:

            if spinRight(PlayerX, PlayerY):
                PlayerX = 460

                PlayerY = 30

                diskUsedright = True

        # if players y is less than the equation of the line for the left side of the pyrimid

        if PlayerY < PlayerX * 8 / 5 - 706:

            # play player death sound, swear appears above player and game stops running

            sndQBDeath1.play()

            winScreen.blit(PlayerSwear, (PlayerX - 72, PlayerY - 72))

            RunGame = False

        # if players y is less than the equation of the line for the right side of the pyrimid

        elif PlayerY < PlayerX * (-8) / 5 + 766 and PlayerY != 350 and PlayerX != 160:

            # play player death sound, swear appears above player and game stops running

            sndQBDeath1.play()

            winScreen.blit(PlayerSwear, (PlayerX - 72, PlayerY - 72))

            RunGame = False

        # if players y is less than 510, bottom of pyrimid

        elif PlayerY > 510:

            # play player death sound, swear appears above player and game stops running

            sndQBDeath1.play()

            winScreen.blit(PlayerSwear, (PlayerX - 72, PlayerY - 72))

            RunGame = False

        # if qberts current position is not in an array of his positions so far, and he isnt off of the pyrimid

        if PlayerPosition not in list_of_positions and PlayerY < 560 and PlayerY > PlayerX * 8 / 5 - 766 and PlayerY > PlayerX * (
        -8) / 5 + 686:
            # add his current xy values to the array of total positions

            list_of_positions.append((PlayerX, PlayerY))

        # for every position in the array of positions

        for item in list_of_positions:
            # seperate the tuple position, and draw a yellow square on that position

            PlayerPosition2 = item

            PlayerX1, PlayerY1 = PlayerPosition2

            pygame.draw.polygon(winScreen, clrYellow, (
            (PlayerX1 + 40, PlayerY1 + 20), (PlayerX1 - 10, PlayerY1 + 50), (PlayerX1 + 40, PlayerY1 + 80),
            (PlayerX1 + 90, PlayerY1 + 50)))

        # if qbert has been in 28 different positions(covered the pyrimid)

        if len(list_of_positions) == 28:
            # play the win sound,stop running the game and set win to true

            sndQBWin.play()

            RunGame = False

            Win = True

        # score = the amount of positions qbert has been in x25 plus the score from previous rounds/deaths

        score = (len(list_of_positions) * 25) + totalScore

        # create a score label, put the total score under it and put it on the screen

        strlable1_under = str(score)

        nlabel1 = myfont.render("Score:", 1, clrRed)

        nlabel1_under = myfont.render(strlable1_under, 1, clrRed)

        winScreen.blit(nlabel1, (100, 100))

        winScreen.blit(nlabel1_under, (100, 125))

        # create a round label, put the amount of rounds under it and put it on the screen

        strlable2_under = str(round_amt)

        nlabel3 = myfont.render("Round:", 1, clrRed)

        nlabel3_under = myfont.render(strlable2_under, 1, clrRed)

        winScreen.blit(nlabel3, (100, 200))

        winScreen.blit(nlabel3_under, (100, 225))

        # create a lives label, put the live symbols under it and put it on the screen

        nlabel2 = myfont.render("Lives:", 1, clrRed)

        winScreen.blit(nlabel2, (100, 150))

        # the amount of live symbols depends on how many lives are left

        if lives == 1:

            winScreen.blit(Livesigns, (100, 175))

        elif lives == 2:

            winScreen.blit(Livesigns, (130, 175))

            winScreen.blit(Livesigns, (100, 175))

        elif lives == 3:

            winScreen.blit(Livesigns, (160, 175))

            winScreen.blit(Livesigns, (130, 175))

            winScreen.blit(Livesigns, (100, 175))

        # put the player on the screen

        winScreen.blit(Player, (PlayerX, PlayerY))

        # if the left disk hasnt been used put the disk on the screen

        if diskUsedleft == False:

            winScreen.blit(PlayerSpin, (160, 390))

        else:

            # if the left disk has been used then the position it used to be in now kills qbert

            if PlayerX == 160 and PlayerY == 350:
                sndQBDeath1.play()

                winScreen.blit(PlayerSwear, (PlayerX - 72, PlayerY - 72))

                RunGame = False

        # if the right disk hasnt been used put the disk on the screen

        if diskUsedright == False:

            winScreen.blit(PlayerSpin, (780, 390))

        else:

            # if the right disk has been used then the position it used to be in now kills qbert

            if PlayerX == 760 and PlayerY == 350:
                sndQBDeath1.play()

                winScreen.blit(PlayerSwear, (PlayerX - 72, PlayerY - 72))

                RunGame = False

        # increment game loop counter by 1

        loop += 1

        # update the movement of the purple ball

        if snakemade == True:
            snake.update()

        # if the loop xround mod 120 = 0(multiplying by round amount increases the amount of balls per round which increases the difficulty

        if loop * round_amt % 120 == 0:
            # make a ball

            BallList.append(ball())

        # for every ball in array of balls check collision

        for a in range(0, len(BallList)):

            if BallList[a].collision():
                # if collide kill qbert

                sndQBDeath1.play()

                winScreen.blit(PlayerSwear, (PlayerX - 72, PlayerY - 72))

                RunGame = False

        if snakemade == True:

            if snake.collision():
                # if collide kill qbert

                sndQBDeath1.play()

                winScreen.blit(PlayerSwear, (PlayerX - 72, PlayerY - 72))

                RunGame = False

        # for every ball in array of balls update the balls position

        for x in range(0, len(BallList)):
            BallList[x].update()

        # update the screen, fill black and tick 1 second

        pygame.display.update()

        winScreen.fill(clrBlack)

        fpsClock.tick(iFPS)

    # after game stops running (RunGame == True)

    # if qbert is out of lives or the player has quit

    if lives == 0 or RunGamereal == True:

        # play game over sound and if lives dont = 0 set lives to 0

        sndQBDeath2.play()

        time.sleep(2)

        lives = 0

    else:

        # if the player won

        if Win == True:

            # play winning music add that rounds score to total score, increment round by 1

            sndQBWin.play()

            totalScore += score

            round_amt += 1

            # win screen waits for player to click on the screen to start the next round

            end_it = False

            while (end_it == False):

                winScreen.fill((238, 232, 170))

                nlabel2 = myfont.render("YOU WON", 1, clrRed)

                nlabel1 = myfont.render("click anywhere to keep playing", 1, clrRed)

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        lives = 0

                        end_it = True

                    if event.type == MOUSEBUTTONDOWN:
                        end_it = True

                winScreen.blit(imgWin, (325, 150))

                winScreen.blit(nlabel2, (180, 95))

                winScreen.blit(nlabel1, (275, 450))

                pygame.display.flip()

        else:

            # if the player lost

            # play losing music add that rounds score to total score

            lives -= 1

            totalScore += score

            sndQBDeath1.play()

            time.sleep(2)

            if lives == 0:

                sndQBDeath2.play()

                time.sleep(2)

                # lose screen waits for player to click on the screen to end the game(close game)

                end_it = False

                while (end_it == False):

                    winScreen.fill((205, 92, 92))

                    nlabel2 = myfont.render("YOU LOST", 1, clrRed)

                    for event in pygame.event.get():

                        if event.type == pygame.QUIT:
                            lives = 0

                            end_it = True

                        if event.type == MOUSEBUTTONDOWN:
                            end_it = True

                    winScreen.blit(imgLose, (325, 150))

                    winScreen.blit(nlabel2, (175, 95))

                    pygame.display.flip()

                lives = 0


