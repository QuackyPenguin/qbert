from typing import Optional, List
import pygame
from cube import Cube
from player import Player
from level import Level

# Constants
CUBE_SIZE = 96
COLOR_BLACK = (0, 0, 0)
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


# Global variables
cubes: Optional[List[Cube]] = None
player: Optional[Player] = None
level: Optional[Level] = None
level_completed: Optional[bool] = None

def initialize_game(gameWindow):
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
        Cube(x1, y1, gameWindow),
        Cube(x2, y2, gameWindow),
        Cube(x3, y3, gameWindow),
        Cube(x4, y4, gameWindow),
        Cube(x5, y5, gameWindow),
        Cube(x6, y6, gameWindow),
        Cube(x7, y7, gameWindow),
        Cube(x8, y8, gameWindow),
        Cube(x9, y9, gameWindow),
        Cube(x10, y10, gameWindow),
        Cube(x11, y11, gameWindow),
        Cube(x12, y12, gameWindow),
        Cube(x13, y13, gameWindow),
        Cube(x14, y14, gameWindow),
        Cube(x15, y15, gameWindow),
        Cube(x16, y16, gameWindow),
        Cube(x17, y17, gameWindow),
        Cube(x18, y18, gameWindow),
        Cube(x19, y19, gameWindow),
        Cube(x20, y20, gameWindow),
        Cube(x21, y21, gameWindow),
        Cube(x22, y22, gameWindow),
        Cube(x23, y23, gameWindow),
        Cube(x24, y24, gameWindow),
        Cube(x25, y25, gameWindow),
        Cube(x26, y26, gameWindow),
        Cube(x27, y27, gameWindow),
        Cube(x28, y28, gameWindow)
    ]

    player = Player(x_center - CUBE_SIZE * 3 // 8, y_center - CUBE_SIZE * 3 // 8, imagePlayerLeftDown, gameWindow)
    level = Level()
    levelCompleted = False

def draw():
    # Draw cubes and player
    # ...

# Other functions if needed