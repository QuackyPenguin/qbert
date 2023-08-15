import random

import variables
from aspire import Player
from constants import *
from enemy import Enemy, JUMP_DURATION
from valid_cube_number_and_row import valid_cube_number_and_row, valid_cube_number_and_row_coily


class Sam(Enemy):
    def __init__(self, image, window, time):
        super().__init__(image, window, time)
        rand_cube = random.randint(1, 2)
        self.x = variables.cubes[rand_cube].x
        self.y = variables.cubes[rand_cube].y - CUBE_SIZE * 4
        self.cubeNumber = rand_cube
        self.rowNumber = 2

    def draw(self):
        if self.jumpDirection == STANDING:
            self.jumpCount -= 1
            if self.jumpCount == 0:
                random_number = random.randint(1, 2)
                if random_number == 1:
                    self.jumpDirection = LEFT
                    self.image = IMAGE_UGG_LEFT
                else:
                    self.jumpDirection = RIGHT
                    self.image = IMAGE_UGG_RIGHT
                self.jumpCount = JUMP_DURATION // 2
        else:
            if self.jumpDirection == FALLING:
                self.y -= CUBE_SIZE // JUMP_DURATION
                self.x -= CUBE_SIZE // JUMP_DURATION
                self.jumpCount -= 1

            elif self.jumpDirection == DOWN_LEFT:
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

            if self.jumpCount == 0:
                self.jumpDirection = STANDING
                self.jumpCount = JUMP_DURATION // 2
                if not valid_cube_number_and_row_coily(self.cubeNumber, self.rowNumber):
                    self.destroy = True
                else:
                    self.x = variables.cubes[self.cubeNumber].x + CUBE_SIZE * 3 // 4
                    self.y = variables.cubes[self.cubeNumber].y + CUBE_SIZE // 4

        self.window.blit(self.image, (self.x + CUBE_SIZE * 3 // 8, self.y - CUBE_SIZE * 1 // 4))

    def detect_collision(self, player: Player) -> bool:
        if abs(self.x - player.x) <= CUBE_SIZE // 4 + 3 and abs(
                self.y + CUBE_SIZE // 4 - player.y) <= CUBE_SIZE // 4 + 3:
            self.destroy = True

        return False