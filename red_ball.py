import random

from constants import *
import variables
from valid_cube_number_and_row import valid_cube_number_and_row

JUMP_DURATION = 24


class RedBall:
    def __init__(self, x, y, image, window, time, cube_number):
        self.x = x
        self.y = y - CUBE_SIZE * 4 - CUBE_SIZE * 1 // 4
        self.image = image
        self.window = window
        self.cubeNumber = cube_number
        self.rowNumber = 2
        self.jumpDirection = FALLING
        self.jumpCount = JUMP_DURATION
        self.destroy = False
        self.time = time

    def draw(self):
        if self.jumpCount == 0 and not self.destroy:
            if not valid_cube_number_and_row(self.cubeNumber + self.rowNumber, self.rowNumber + 1):
                self.jumpDirection = DOWN_RIGHT
            elif not valid_cube_number_and_row(self.cubeNumber + self.rowNumber + 1, self.rowNumber + 1):
                self.jumpDirection = DOWN_LEFT
            else:
                self.jumpDirection = random.randint(1, 2)
            # x_center - CUBE_SIZE * 3 // 8, y_center - CUBE_SIZE * 3 // 8
            self.x = variables.cubes[self.cubeNumber].x + CUBE_SIZE * 3 // 8
            self.y = variables.cubes[self.cubeNumber].y - CUBE_SIZE * 1 // 4
            self.jumpCount = JUMP_DURATION

        elif self.jumpCount > 0:
            change_cube = False
            if self.jumpCount == (JUMP_DURATION * 2 // 3):
                change_cube = True

            if self.jumpDirection == DOWN_LEFT:
                self.x -= CUBE_SIZE // (2 * JUMP_DURATION - 1)
                if self.jumpCount > JUMP_DURATION * 2 // 3:
                    self.y -= CUBE_SIZE // (JUMP_DURATION * 4 // 3)
                else:
                    self.y += CUBE_SIZE // (JUMP_DURATION * 2 // 3 - 1)
                self.jumpCount -= 1
                if change_cube:
                    self.cubeNumber = self.cubeNumber + self.rowNumber
                    self.rowNumber += 1

            elif self.jumpDirection == DOWN_RIGHT:
                self.x += CUBE_SIZE // (2 * JUMP_DURATION - 1)
                if self.jumpCount > JUMP_DURATION * 2 // 3:
                    self.y -= CUBE_SIZE // (JUMP_DURATION * 4 // 3)
                else:
                    self.y += CUBE_SIZE // (JUMP_DURATION * 2 // 3 - 1)
                self.jumpCount -= 1
                if change_cube:
                    self.cubeNumber = self.cubeNumber + self.rowNumber + 1
                    self.rowNumber += 1

            elif self.jumpDirection == FALLING:
                self.y += (CUBE_SIZE * 4) // JUMP_DURATION
                self.jumpCount -= 1

            if change_cube:
                if self.rowNumber > 7:
                    self.destroy = True

        self.window.blit(self.image, (self.x, self.y))
