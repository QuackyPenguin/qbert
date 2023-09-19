import random
from typing import List

LEFT = 1
RIGHT = 2


class Disc:
    def __init__(self, discs):
        side = 0
        used_spaces = {}
        for disc in discs:
            if disc.side == LEFT:
                side += 1
            else:
                side -= 1   
            used_spaces[(disc.row, disc.side)] = 1

        random_number = random.randint(1, 2)
        if side < 0 or (side == 0 and random_number == 1):
            self.side = LEFT
        else:
            self.side = RIGHT

        while True:
            random_number = random.randint(1, 6)
            if not (random_number, self.side) in used_spaces:
                self.row = random_number
                break

        if self.side == LEFT:
            self.cube = self.row * (self.row - 1) // 2 - 1
        else:
            self.cube = self.row * (self.row + 1) // 2

        self.used = False
        self.inuse = False
