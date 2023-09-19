import random

import variables
from constants import *
from enemy import Enemy, JUMP_DURATION
from valid_cube_number_and_row import valid_cube_number_and_row


class RedBall(Enemy):
    def __init__(self, image, time):
        super().__init__(image, time)
        rand_cube = random.randint(1, 2)
        self.x = variables.cubes[rand_cube].x
        self.y = variables.cubes[rand_cube].y - CUBE_SIZE * 4
        self.cubeNumber = rand_cube
        self.rowNumber = 2

    def move(self):
        if not variables.freeze:
            if self.jumpCount == 0 and not self.destroy:
                if not valid_cube_number_and_row(self.cubeNumber + self.rowNumber, self.rowNumber + 1):
                    self.jumpDirection = DOWN_RIGHT
                elif not valid_cube_number_and_row(self.cubeNumber + self.rowNumber + 1, self.rowNumber + 1):
                    self.jumpDirection = DOWN_LEFT
                else:
                    self.jumpDirection = random.randint(1, 2)
                self.x = variables.cubes[self.cubeNumber].x
                self.y = variables.cubes[self.cubeNumber].y
                self.jumpCount = JUMP_DURATION

            elif self.jumpCount > 0:
                if self.jumpDirection == DOWN_LEFT:
                    self.x -= CUBE_SIZE // (2 * JUMP_DURATION - 1)
                    if self.jumpCount > JUMP_DURATION * 2 // 3:
                        self.y -= CUBE_SIZE // (JUMP_DURATION * 4 // 3)
                    else:
                        self.y += CUBE_SIZE // (JUMP_DURATION * 2 // 3 - 1)
                    self.jumpCount -= 1
                    if self.jumpCount == 0:
                        self.cubeNumber = self.cubeNumber + self.rowNumber
                        self.rowNumber += 1

                elif self.jumpDirection == DOWN_RIGHT:
                    self.x += CUBE_SIZE // (2 * JUMP_DURATION - 1)
                    if self.jumpCount > JUMP_DURATION * 2 // 3:
                        self.y -= CUBE_SIZE // (JUMP_DURATION * 4 // 3)
                    else:
                        self.y += CUBE_SIZE // (JUMP_DURATION * 2 // 3 - 1)
                    self.jumpCount -= 1
                    if self.jumpCount == 0:
                        self.cubeNumber = self.cubeNumber + self.rowNumber + 1
                        self.rowNumber += 1

                elif self.jumpDirection == FALLING:
                    self.y += (CUBE_SIZE * 2) // JUMP_DURATION
                    self.jumpCount -= 1

                if self.jumpCount == 0:
                    if self.rowNumber > 7:
                        self.destroy = True

    def draw(self):
        self.move()

        variables.game_window.blit(self.image, (self.x + CUBE_SIZE * 3 // 8, self.y - CUBE_SIZE * 1 // 4))
