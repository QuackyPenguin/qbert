import random

import variables
from coily import Coily
from constants import *
from disc import Disc
from enemy import Enemy
from red_ball import RedBall
from slick import Slick
from ugg import Ugg
from wrongway import Wrongway


class Level:
    def __init__(self):
        self.level = 1
        self.round = 1
        self.requestedColors = [COLOR_YELLOW, COLOR_BLUE]

    def next_color(self, number):
        new_color = COLOR_BLACK
        if self.level < 10:
            new_color = COLOR_YELLOW

        if new_color != variables.cubes[number].color and new_color == self.requestedColors[self.level - 1]:
            variables.score += 25

        variables.cubes[number].color = new_color

        flag = True
        for cube in variables.cubes:
            if cube.color != self.requestedColors[self.level - 1]:
                flag = False
                break

        if flag:
            variables.round_completed = True
            if self.round == 4:
                self.round = 1
                self.level += 1
                variables.level_completed = True
            else:
                self.round += 1

            for cube in variables.cubes:
                cube.color = COLOR_PURPLE

    def init_next_level(self):
        variables.discs = []
        variables.enemies = []

        number_of_discs = 7
        if (self.level == 2 and (self.round == 1 or self.round == 2)) or (
                self.level == 3 and (self.round == 3 or self.round == 4)):
            number_of_discs = 3
        elif (self.level == 3 and (self.round == 1 or self.round == 2)) or (self.level == 4 and self.round == 4):
            number_of_discs = 4
        elif (self.level == 4 and (self.round == 1 or self.round == 2)) or (
                self.level == 5 and (self.round == 2 or self.round == 3)):
            number_of_discs = 6
        elif self.level == 5 and self.round == 1:
            number_of_discs = 7
        elif (self.level == 4 and self.round == 3) or (self.level == 5 and self.round == 4) or self.level >= 6:
            number_of_discs = 5

        for i in range(0, number_of_discs):
            variables.discs.append(Disc(variables.discs))

        variables.score += ((self.level - 1) * 4 + (self.round - 1)) * 250 + 1000

        variables.round_completed = False
        variables.level_completed = False

    def next_enemy_appearance(self):
        time = variables.game_time + random.randint(4, 8) * 15
        return time

    def generate_enemy(self, game_window) -> Enemy:
        red_ball_odds = 2 / 3
        coily_odds = 1 / 3
        number_of_red_balls = 0
        coily_alive = False
        if not coily_alive:
            return Ugg(IMAGE_UGG_LEFT, game_window, variables.game_time)

        for enemy in variables.enemies:
            if isinstance(enemy, RedBall):
                number_of_red_balls += 1
            elif isinstance(enemy, Coily):
                coily_alive = True

        if coily_alive:
            coily_odds = 0
            red_ball_odds = 100
        else:
            red_ball_odds -= number_of_red_balls / 9
            coily_odds += number_of_red_balls / 9

        red_ball_odds *= 100
        coily_odds *= 100

        random_number = random.randint(1, 100)
        if random_number <= red_ball_odds:
            return RedBall(IMAGE_RED_BALL, game_window, variables.game_time)
        else:
            return Coily(IMAGE_PURPLE_BALL, game_window, variables.game_time)
