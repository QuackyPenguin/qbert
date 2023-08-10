# imports

from typing import Optional, List

import pygame

# constants

GAME_WINDOW_WIDTH = 1024
GAME_WINDOW_HEIGHT = 768

CUBE_SIZE = 96

COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 100, 100)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 51)
COLOR_ORANGE = (255, 178, 80)
COLOR_PURPLE = (255, 102, 255)
COLOR_GRAY = (172, 172, 172)

STANDING = 0
DOWN_LEFT = 1
DOWN_RIGHT = 2
UP_LEFT = 3
UP_RIGHT = 4

START = 0
PLAYING = 1
GAME_OVER = 2

FONT_SIZE = 36

# variables

jumpDirectionPlayer = STANDING
state = START
score = 0


# help functions

def make_color_grayer(color, factor=0.5):
    new_color = tuple(int(component * factor) for component in color)
    return new_color


def validCubeNumberAndRow(number, row):
    if number < 0 or number > 27:
        return False

    if number > 20 and row != 7:
        return False
    elif 21 > number > 14 and row != 6:
        return False
    elif 15 > number > 9 and row != 5:
        return False
    elif 10 > number > 5 and row != 4:
        return False
    elif 6 > number > 2 and row != 3:
        return False
    elif 3 > number > 0 and row != 2:
        return False
    elif number == 0 and row != 1:
        return False

    return True


def initializeGame():
    global cubes
    global player
    global level
    global levelCompleted
    global x_center
    global y_center

    x1, y1 = x_center - CUBE_SIZE // 2, y_center + CUBE_SIZE // 4
    x2, y2 = x1 - CUBE_SIZE // 2, y1 + 3 * CUBE_SIZE // 4
    x3, y3 = x2 + CUBE_SIZE, y2
    x4, y4 = x2 - CUBE_SIZE // 2, y2 + 3 * CUBE_SIZE // 4
    x5, y5 = x4 + CUBE_SIZE, y4
    x6, y6 = x5 + CUBE_SIZE, y5
    x7, y7 = x4 - CUBE_SIZE // 2, y4 + 3 * CUBE_SIZE // 4
    x8, y8 = x7 + CUBE_SIZE, y7
    x9, y9 = x8 + CUBE_SIZE, y8
    x10, y10 = x9 + CUBE_SIZE, y9
    x11, y11 = x7 - CUBE_SIZE // 2, y7 + 3 * CUBE_SIZE // 4
    x12, y12 = x11 + CUBE_SIZE, y11
    x13, y13 = x12 + CUBE_SIZE, y12
    x14, y14 = x13 + CUBE_SIZE, y13
    x15, y15 = x14 + CUBE_SIZE, y14
    x16, y16 = x11 - CUBE_SIZE // 2, y11 + 3 * CUBE_SIZE // 4
    x17, y17 = x16 + CUBE_SIZE, y16
    x18, y18 = x17 + CUBE_SIZE, y17
    x19, y19 = x18 + CUBE_SIZE, y18
    x20, y20 = x19 + CUBE_SIZE, y19
    x21, y21 = x20 + CUBE_SIZE, y20
    x22, y22 = x16 - CUBE_SIZE // 2, y16 + 3 * CUBE_SIZE // 4
    x23, y23 = x22 + CUBE_SIZE, y22
    x24, y24 = x23 + CUBE_SIZE, y23
    x25, y25 = x24 + CUBE_SIZE, y24
    x26, y26 = x25 + CUBE_SIZE, y25
    x27, y27 = x26 + CUBE_SIZE, y26
    x28, y28 = x27 + CUBE_SIZE, y27

    cubes = [
        Cube(x1, y1, game_window),
        Cube(x2, y2, game_window),
        Cube(x3, y3, game_window),
        Cube(x4, y4, game_window),
        Cube(x5, y5, game_window),
        Cube(x6, y6, game_window),
        Cube(x7, y7, game_window),
        Cube(x8, y8, game_window),
        Cube(x9, y9, game_window),
        Cube(x10, y10, game_window),
        Cube(x11, y11, game_window),
        Cube(x12, y12, game_window),
        Cube(x13, y13, game_window),
        Cube(x14, y14, game_window),
        Cube(x15, y15, game_window),
        Cube(x16, y16, game_window),
        Cube(x17, y17, game_window),
        Cube(x18, y18, game_window),
        Cube(x19, y19, game_window),
        Cube(x20, y20, game_window),
        Cube(x21, y21, game_window),
        Cube(x22, y22, game_window),
        Cube(x23, y23, game_window),
        Cube(x24, y24, game_window),
        Cube(x25, y25, game_window),
        Cube(x26, y26, game_window),
        Cube(x27, y27, game_window),
        Cube(x28, y28, game_window)
    ]

    player = Player(x_center - CUBE_SIZE * 3 // 8, y_center - CUBE_SIZE * 3 // 8, imagePlayerLeftDown, game_window)
    level = Level()
    levelCompleted = False


# initialize window

pygame.init()

game_window = pygame.display.set_mode((GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT), 0, 32)
font = pygame.font.Font(None, FONT_SIZE)

caption = 'Q*bert'
pygame.display.set_caption(caption)

# import images

pathImageStartPage = 'images/startpage.png'

pathImagePlayerLeftDown = 'images/playerleftdown.png'
pathImagePlayerRightDown = 'images/playerrightdown.png'
pathImagePlayerLeftUp = 'images/playerleftup.png'
pathImagePlayerRightUp = 'images/playerrightup.png'
pathImagePlayerLittle = 'images/playerlittle.png'

imageStartPage = pygame.image.load(pathImageStartPage)

imagePlayerLeftDown = pygame.image.load(pathImagePlayerLeftDown)
imagePlayerRightDown = pygame.image.load(pathImagePlayerRightDown)
imagePlayerLeftUp = pygame.image.load(pathImagePlayerLeftUp)
imagePlayerRightUp = pygame.image.load(pathImagePlayerRightUp)
imagePlayerLittle = pygame.image.load(pathImagePlayerLittle)


# classes

class Level:
    def __init__(self):
        self.level = 1
        self.requestedColors = [COLOR_YELLOW, COLOR_BLUE]

    def nextColor(self, number):
        global cubes
        global levelCompleted
        global score
        new_color = COLOR_BLACK
        if self.level < 10:
            new_color = COLOR_YELLOW

        if new_color != cubes[number].color and new_color == self.requestedColors[self.level-1]:
            score += 25
            cubes[number].color = new_color

        flag = True
        for cube in cubes:
            if cube.color != self.requestedColors[self.level - 1]:
                flag = False
                break

        if flag:
            levelCompleted = True
            # TODO next level, self.level += 1
            for cube in cubes:
                cube.color = COLOR_PURPLE


class Cube:
    def __init__(self, x, y, window):
        self.x = x
        self.y = y
        self.color = COLOR_RED
        self.window = window

    def draw(self):
        vertices = [(self.x, self.y), (self.x + CUBE_SIZE // 2, self.y + CUBE_SIZE // 4),
                    (self.x + CUBE_SIZE, self.y),
                    (self.x + CUBE_SIZE // 2, self.y - CUBE_SIZE // 4)]

        pygame.draw.polygon(self.window, self.color, vertices)
        pygame.draw.lines(self.window, COLOR_GRAY, points=vertices, closed=True)

        vertices = [(self.x, self.y), (self.x + CUBE_SIZE // 2, self.y + CUBE_SIZE // 4),
                    (self.x + CUBE_SIZE // 2, self.y + CUBE_SIZE * 3 // 4),
                    (self.x, self.y + CUBE_SIZE // 2)]

        pygame.draw.polygon(self.window, make_color_grayer(COLOR_GRAY, 0.6), vertices)
        pygame.draw.lines(self.window, COLOR_GRAY, points=vertices, closed=True)

        vertices = [(self.x + CUBE_SIZE // 2, self.y + CUBE_SIZE // 4), (self.x + CUBE_SIZE, self.y),
                    (self.x + CUBE_SIZE, self.y + CUBE_SIZE // 2),
                    (self.x + CUBE_SIZE // 2, self.y + CUBE_SIZE * 3 // 4)]

        pygame.draw.polygon(self.window, make_color_grayer(COLOR_GRAY, 0.4), vertices)
        pygame.draw.lines(self.window, COLOR_GRAY, points=vertices, closed=True)


class Player:
    def __init__(self, x, y, image, window):
        self.x = x
        self.y = y
        self.image = image
        self.window = window
        self.cubeNumber = 0
        self.rowNumber = 1
        self.jumpDirection = STANDING
        self.jumpCount = 0
        self.outOfBounds = False
        self.lives = 3

    def draw(self):
        global jumpDirectionPlayer
        global cubes
        if jumpDirectionPlayer != self.jumpDirection and self.jumpCount == 0:
            self.jumpCount = 15
            self.jumpDirection = jumpDirectionPlayer
            if jumpDirectionPlayer == DOWN_LEFT:
                self.image = imagePlayerLeftDown
            elif jumpDirectionPlayer == DOWN_RIGHT:
                self.image = imagePlayerRightDown
            elif jumpDirectionPlayer == UP_LEFT:
                self.image = imagePlayerLeftUp
            elif jumpDirectionPlayer == UP_RIGHT:
                self.image = imagePlayerRightUp
        elif self.jumpCount == 0:
            if self.jumpDirection != STANDING and not self.outOfBounds:
                global level
                level.nextColor(self.cubeNumber)
            if self.outOfBounds:
                self.lives -= 1
                self.outOfBounds = False
            self.jumpDirection = STANDING
            jumpDirectionPlayer = STANDING
            # x_center - CUBE_SIZE * 3 // 8, y_center - CUBE_SIZE * 3 // 8
            self.x = cubes[self.cubeNumber].x + CUBE_SIZE // 8
            self.y = cubes[self.cubeNumber].y - CUBE_SIZE * 5 // 8
            self.outOfBounds = False

        if self.jumpCount > 0:
            changeCube = False
            if self.jumpCount == 10:
                changeCube = True

            if self.jumpDirection == DOWN_LEFT:
                self.x -= 96 // 29
                if self.jumpCount > 10:
                    self.y -= 96 // 20
                else:
                    self.y += 96 // 9
                self.jumpCount -= 1
                if changeCube:
                    self.cubeNumber = self.cubeNumber + self.rowNumber
                    self.rowNumber += 1

            elif self.jumpDirection == DOWN_RIGHT:
                self.x += 96 // 29
                if self.jumpCount > 10:
                    self.y -= 96 // 20
                else:
                    self.y += 96 // 9
                self.jumpCount -= 1
                if changeCube:
                    self.cubeNumber = self.cubeNumber + self.rowNumber + 1
                    self.rowNumber += 1

            elif self.jumpDirection == UP_RIGHT:
                self.x += 96 // 29
                if self.jumpCount < 6:
                    self.y += 96 // 20
                else:
                    self.y -= 96 // 9
                self.jumpCount -= 1
                if changeCube:
                    self.cubeNumber = self.cubeNumber - self.rowNumber + 1
                    self.rowNumber -= 1

            elif self.jumpDirection == UP_LEFT:
                self.x -= 96 // 29
                if self.jumpCount < 6:
                    self.y += 96 // 20
                else:
                    self.y -= 96 // 9
                self.jumpCount -= 1
                if changeCube:
                    self.cubeNumber = self.cubeNumber - self.rowNumber
                    self.rowNumber -= 1

            if changeCube:
                if not validCubeNumberAndRow(self.cubeNumber, self.rowNumber):
                    self.cubeNumber = 0
                    self.rowNumber = 1
                    self.outOfBounds = True
                    # TODO lose life, insert pause


        self.window.blit(self.image, (self.x, self.y))

        for i in range(0, self.lives):
            self.window.blit(imagePlayerLittle, (10, 300+i*20))


# initialize game

x_center = GAME_WINDOW_WIDTH // 2
y_center = 120

cubes: Optional[List[Cube]] = None
player: Optional[Player] = None
level: Optional[Level] = None
levelCompleted: Optional[bool] = None

initializeGame()


# draw function

def draw():
    global player
    global state
    global jumpDirectionPlayer
    global levelCompleted
    global score

    if state == START:
        game_window.blit(imageStartPage, (0, 0))
    elif state == PLAYING:
        game_window.fill(COLOR_BLACK)

        for cube in cubes:
            cube.draw()

        player.draw()

        text = font.render(str(score), True, COLOR_ORANGE)
        text_rect = text.get_rect(center=(100, 120))
        game_window.blit(text, text_rect)

# running loop

running = True

while running:
    pygame.time.delay(25)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if state == START:
        if pygame.mouse.get_pressed()[0]:
            state = PLAYING
    elif state == PLAYING:
        if jumpDirectionPlayer == STANDING:
            if keys[pygame.K_LEFT]:
                jumpDirectionPlayer = UP_LEFT
            if keys[pygame.K_RIGHT]:
                jumpDirectionPlayer = DOWN_RIGHT
            if keys[pygame.K_UP]:
                jumpDirectionPlayer = UP_RIGHT
            if keys[pygame.K_DOWN]:
                jumpDirectionPlayer = DOWN_LEFT

    draw()

    pygame.display.update()

    if levelCompleted:
        player.x, player.y, player.image = x_center - CUBE_SIZE * 3 // 8, y_center - CUBE_SIZE * 3 // 8, imagePlayerLeftDown
        levelCompleted = False

    if player.lives == 0:
        initializeGame()

pygame.quit()
