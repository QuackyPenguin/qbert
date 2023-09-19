import variables
from constants import *
from cube import Cube
from level import Level
from player import Player


def initialize_game():
    x1, y1 = X_CENTER - CUBE_SIZE // 2, Y_CENTER + CUBE_SIZE // 4
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

    variables.cubes = [
        Cube(x1, y1, 1),
        Cube(x2, y2, 2),
        Cube(x3, y3, 2),
        Cube(x4, y4, 3),
        Cube(x5, y5, 3),
        Cube(x6, y6, 3),
        Cube(x7, y7, 4),
        Cube(x8, y8, 4),
        Cube(x9, y9, 4),
        Cube(x10, y10, 4),
        Cube(x11, y11, 5),
        Cube(x12, y12, 5),
        Cube(x13, y13, 5),
        Cube(x14, y14, 5),
        Cube(x15, y15, 5),
        Cube(x16, y16, 6),
        Cube(x17, y17, 6),
        Cube(x18, y18, 6),
        Cube(x19, y19, 6),
        Cube(x20, y20, 6),
        Cube(x21, y21, 6),
        Cube(x22, y22, 7),
        Cube(x23, y23, 7),
        Cube(x24, y24, 7),
        Cube(x25, y25, 7),
        Cube(x26, y26, 7),
        Cube(x27, y27, 7),
        Cube(x28, y28, 7)
    ]

    variables.player = Player(
        X_CENTER, Y_CENTER, IMAGE_PLAYER_LEFT_DOWN)
    variables.level = Level()
    variables.round_completed = False
    variables.jump_direction_player = STANDING
    variables.score = 0

def initialize_window():
    pygame.init()

    variables.game_window = pygame.display.set_mode((GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT), 0, 32)
    variables.font = pygame.font.Font(None, FONT_SIZE)

    caption = 'Q*bert'
    pygame.display.set_caption(caption)