import variables
from constants import *
from player import Player
from level import Level
from cube import Cube


def initialize_game(game_window):
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

    variables.player = Player(X_CENTER - CUBE_SIZE * 3 // 8, Y_CENTER - CUBE_SIZE * 3 // 8,
                              IMAGE_PLAYER_LEFT_DOWN, game_window)
    variables.level = Level()
    variables.round_completed = False
