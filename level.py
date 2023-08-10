from constants import *
import variables


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
