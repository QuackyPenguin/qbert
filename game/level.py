import random

import variables
from coily import Coily
from constants import *
from disc import Disc
from enemy import Enemy
from green_ball import GreenBall
from player import JUMP_DURATION
from red_ball import RedBall
from sam import Sam
from slick import Slick
from ugg import Ugg
from wrongway import Wrongway


class Level:
    def __init__(self):
        self.level = 0
        self.round = 0
        self.colors = [COLOR_BLUE, COLOR_YELLOW]

    def next_color(self, number):
        old_color = variables.cubes[number].color
        new_color = COLOR_BLACK

        if self.level == 1 or (self.level == 0 and self.round == 0):
            new_color = self.colors[1]
        elif self.level == 2 or (self.level == 0 and self.round == 1):
            if old_color == self.colors[0]:
                new_color = self.colors[1]
            else:
                new_color = self.colors[2]
        elif self.level == 3 or (self.level == 0 and self.round == 2):
            if old_color == self.colors[0]:
                new_color = self.colors[1]
            else:
                new_color = self.colors[0]
        elif self.level == 4 or (self.level == 0 and self.round == 3):
            if old_color == self.colors[1]:
                new_color = self.colors[2]
            else:
                new_color = self.colors[1]
        elif self.level >= 5 or (self.level == 0 and self.round == 4):
            if old_color == self.colors[0]:
                new_color = self.colors[1]
            elif old_color == self.colors[1]:
                new_color = self.colors[2]
            else:
                new_color = self.colors[0]

        if new_color != old_color and new_color == self.colors[len(self.colors) - 1]:
            variables.score += 25

        variables.cubes[number].color = new_color

        flag = True
        for cube in variables.cubes:
            if cube.color != self.colors[len(self.colors) - 1]:
                flag = False
                break

        if flag:
            if self.level == 0:
                variables.score += 1000
            else:
                variables.score += ((self.level - 1) * 4 +
                                    (self.round - 1)) * 250 + 1000
            variables.celebrate = True
            variables.round_completed = True
            if self.round == 4:
                self.round = 1
                self.level += 1
                variables.level_completed = True
            else:
                self.round += 1

            if self.level == 1 or self.level == 3 or (self.level == 0 and (self.round == 0 or self.round == 2)):
                if self.round == 1:
                    self.colors = [COLOR_BLUE, COLOR_YELLOW]
                elif self.round == 2:
                    self.colors = [COLOR_GOLD, COLOR_DARK_BLUE]
                elif self.round == 3:
                    self.colors = [COLOR_SILVER, COLOR_MAROON]
                else:
                    self.colors = [COLOR_LAVENDER, COLOR_LIME]
            else:
                if self.round == 1:
                    self.colors = [COLOR_ORANGE, COLOR_RED, COLOR_YELLOW]
                elif self.round == 2:
                    self.colors = [COLOR_CYAN, COLOR_PURPLE, COLOR_DARK_BLUE]
                elif self.round == 3:
                    self.colors = [COLOR_GRAY, COLOR_PINK, COLOR_MAROON]
                else:
                    self.colors = [COLOR_BROWN, COLOR_SKY_BLUE, COLOR_LIME]

    def init_next_level(self):
        variables.speed = max(10, variables.speed - 1)
        (variables.player.x, variables.player.y, variables.player.image,
         variables.player.cubeNumber, variables.player.rowNumber,
         variables.player.leftPlatform, variables.player.rightPlatform) = (
            X_CENTER - CUBE_SIZE * 3 // 8,
            Y_CENTER - CUBE_SIZE * 3 // 8,
            IMAGE_PLAYER_LEFT_DOWN, 0, 1, True, True)
        for cube in variables.cubes:
            cube.color = self.colors[0]
        variables.discs = []
        variables.enemies = []

        number_of_discs = 2
        if self.level == 0:
            if self.round == 0:
                number_of_discs = 1
            elif self.round == 1:
                number_of_discs = 3
            elif self.round == 2:
                number_of_discs = 2
            elif self.round == 3:
                number_of_discs = 5
            elif self.round == 4:
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

        variables.round_completed = False
        variables.level_completed = False

    def next_enemy_appearance(self):
        if self.round == 0:
            return -1
        a = max(7 - self.level // 2, 3)
        b = max(14 - self.level // 3 - self.round // 2, 8)
        time = variables.game_time + random.randint(a, b) * JUMP_DURATION
        return time

    def generate_enemy(self) -> Enemy:
        red_ball_odds = coily_odds = ugg_odds = wrongway_odds = sam_odds = slick_odds = green_ball_odds = 1000
        red_ball_odds += 250
        number_of_red_balls = 0
        case_enemy = NONE

        for enemy in variables.enemies:
            if isinstance(enemy, RedBall):
                number_of_red_balls += 1
            elif isinstance(enemy, Coily):
                coily_odds = 0
            elif isinstance(enemy, Ugg):
                ugg_odds = 0
            elif isinstance(enemy, Wrongway):
                wrongway_odds = 0
            elif isinstance(enemy, Sam):
                sam_odds = 0
            elif isinstance(enemy, Slick):
                slick_odds = 0
            elif isinstance(enemy, GreenBall):
                green_ball_odds = 0

        odds_array = []
        case_array = []

        if self.level == 0:
            if self.round == 0:
                odds_array.append(red_ball_odds)
                case_array.append(RED_BALL)

            elif self.round == 1:
                red_ball_odds = red_ball_odds + 1000 * (self.round % 2)
                red_ball_odds -= number_of_red_balls * 1000 / 4.5

                odds_array.append(red_ball_odds)
                case_array.append(RED_BALL)
                odds_array.append(coily_odds)
                case_array.append(COILY)
            
            elif self.round == 3:
                odds_array.append(green_ball_odds)
                case_array.append(GREEN_BALL)
                odds_array.append(coily_odds)
                case_array.append(COILY)
                odds_array.append(ugg_odds)
                case_array.append(UGG)
                odds_array.append(wrongway_odds)
                case_array.append(WRONGWAY)
            
            elif self.round == 2:
                odds_array.append(green_ball_odds)
                case_array.append(GREEN_BALL)
                odds_array.append(sam_odds)
                case_array.append(SAM)
                odds_array.append(slick_odds)
                case_array.append(SLICK)
            
            elif self.round == 4:
                red_ball_odds -= number_of_red_balls * 1000 / 4.5

                odds_array.append(green_ball_odds)
                case_array.append(GREEN_BALL)
                odds_array.append(red_ball_odds)
                case_array.append(RED_BALL)
                odds_array.append(coily_odds)
                case_array.append(COILY)
                odds_array.append(ugg_odds)
                case_array.append(UGG)
                odds_array.append(wrongway_odds)
                case_array.append(WRONGWAY)
                odds_array.append(sam_odds)
                case_array.append(SAM)
                odds_array.append(slick_odds)
                case_array.append(SLICK)

        if self.level == 1 and (self.round == 1 or self.round == 2):
            red_ball_odds = red_ball_odds + 1000 * (self.round % 2)
            red_ball_odds -= number_of_red_balls * 1000 / 4.5

            odds_array.append(red_ball_odds)
            case_array.append(RED_BALL)
            odds_array.append(coily_odds)
            case_array.append(COILY)

        elif (self.level == 2 and self.round == 4) or (self.level == 3 and (self.round == 3 or self.round == 4)) \
                or (self.level == 4 and (self.round == 2 or self.round == 4)) and (
                self.level == 5 and (self.round == 3 or self.round == 4)) \
                or self.level >= 6:

            red_ball_odds -= number_of_red_balls * 1000 / 4.5

            odds_array.append(green_ball_odds)
            case_array.append(GREEN_BALL)
            odds_array.append(red_ball_odds)
            case_array.append(RED_BALL)
            odds_array.append(coily_odds)
            case_array.append(COILY)
            odds_array.append(ugg_odds)
            case_array.append(UGG)
            odds_array.append(wrongway_odds)
            case_array.append(WRONGWAY)
            odds_array.append(sam_odds)
            case_array.append(SAM)
            odds_array.append(slick_odds)
            case_array.append(SLICK)

        elif (self.level == 1 and self.round == 4) or (self.level == 2 and self.round == 3) or (
                self.level == 3 and self.round == 1) \
                or (self.level == 4 and (self.round == 1 or self.round == 3)) \
                or (self.level == 5 and (self.round == 1 or self.round == 2)):
            red_ball_odds -= number_of_red_balls * 1000 / 4.5

            odds_array.append(green_ball_odds)
            case_array.append(GREEN_BALL)
            odds_array.append(red_ball_odds)
            case_array.append(RED_BALL)
            odds_array.append(coily_odds)
            case_array.append(COILY)
            odds_array.append(sam_odds)
            case_array.append(SAM)
            odds_array.append(slick_odds)
            case_array.append(SLICK)

        elif (self.level == 2 and (self.round == 1 or self.round == 2)) \
                or (self.level == 3 and self.round == 2):
            odds_array.append(green_ball_odds)
            case_array.append(GREEN_BALL)
            odds_array.append(coily_odds)
            case_array.append(COILY)
            odds_array.append(ugg_odds)
            case_array.append(UGG)
            odds_array.append(wrongway_odds)
            case_array.append(WRONGWAY)
            odds_array.append(sam_odds)
            case_array.append(SAM)
            odds_array.append(slick_odds)
            case_array.append(SLICK)
        elif self.level == 1 and self.round == 3:

            odds_array.append(green_ball_odds)
            case_array.append(GREEN_BALL)
            odds_array.append(coily_odds)
            case_array.append(COILY)
            odds_array.append(ugg_odds)
            case_array.append(UGG)
            odds_array.append(wrongway_odds)
            case_array.append(WRONGWAY)

        odds_sum = 0
        for odd in odds_array:
            odds_sum += odd

        random_number = random.randint(1, int(odds_sum + 1))
        odds_sum = 0
        for i in range(0, len(odds_array)):
            if odds_sum < random_number <= odds_sum + odds_array[i]:
                case_enemy = case_array[i]
                break
            odds_sum += odds_array[i]

        if case_enemy == RED_BALL:
            return RedBall(IMAGE_RED_BALL, variables.game_time)
        elif case_enemy == COILY:
            return Coily(IMAGE_PURPLE_BALL, variables.game_time)
        elif case_enemy == UGG:
            return Ugg(IMAGE_UGG_LEFT, variables.game_time)
        elif case_enemy == WRONGWAY:
            return Wrongway(IMAGE_WRONGWAY_LEFT, variables.game_time)
        elif case_enemy == SAM:
            return Sam(IMAGE_SAM_LEFT, variables.game_time)
        elif case_enemy == SLICK:
            return Slick(IMAGE_SLICK_LEFT, variables.game_time)
        elif case_enemy == GREEN_BALL:
            return GreenBall(IMAGE_GREEN_BALL, variables.game_time)
