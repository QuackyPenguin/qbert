import pygame
import variables

from constants import *


def make_color_grayer(color, factor=0.5):
    new_color = tuple(int(component * factor) for component in color)
    return new_color


class Cube:
    def __init__(self, x, y, row):
        self.x = x
        self.y = y
        self.color = COLOR_RED
        self.row = row

    def draw(self):
        vertices = [(self.x, self.y), (self.x + CUBE_SIZE // 2, self.y + CUBE_SIZE // 4),
                    (self.x + CUBE_SIZE, self.y),
                    (self.x + CUBE_SIZE // 2, self.y - CUBE_SIZE // 4)]

        pygame.draw.polygon(variables.game_window, self.color, vertices)
        pygame.draw.lines(variables.game_window, COLOR_GRAY, points=vertices, closed=True)

        vertices = [(self.x, self.y), (self.x + CUBE_SIZE // 2, self.y + CUBE_SIZE // 4),
                    (self.x + CUBE_SIZE // 2, self.y + CUBE_SIZE * 3 // 4),
                    (self.x, self.y + CUBE_SIZE // 2)]

        pygame.draw.polygon(variables.game_window, make_color_grayer(COLOR_GRAY, 0.6), vertices)
        pygame.draw.lines(variables.game_window, COLOR_GRAY, points=vertices, closed=True)

        vertices = [(self.x + CUBE_SIZE // 2, self.y + CUBE_SIZE // 4), (self.x + CUBE_SIZE, self.y),
                    (self.x + CUBE_SIZE, self.y + CUBE_SIZE // 2),
                    (self.x + CUBE_SIZE // 2, self.y + CUBE_SIZE * 3 // 4)]

        pygame.draw.polygon(variables.game_window, make_color_grayer(COLOR_GRAY, 0.4), vertices)
        pygame.draw.lines(variables.game_window, COLOR_GRAY, points=vertices, closed=True)
