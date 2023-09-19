import random

import variables
from enemy import Enemy, JUMP_DURATION
from constants import *
from player import Player
from valid_cube_number_and_row import valid_cube_number_and_row_coily


class Ugg(Enemy):
    def __init__(self, image, time):
        super().__init__(image, time)
        self.cubeNumber = 27
        self.rowNumber = 7
        self.x = variables.cubes[27].x + CUBE_SIZE * 3 // 4 + CUBE_SIZE * 2
        self.y = variables.cubes[27].y + CUBE_SIZE // 4 + CUBE_SIZE * 2

    def move(self):
        if not variables.freeze:
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

                elif self.jumpDirection == LEFT:
                    self.x -= CUBE_SIZE // (JUMP_DURATION // 2 - 1)
                    if self.jumpCount < JUMP_DURATION * 3 // 8:
                        self.y -= CUBE_SIZE // (JUMP_DURATION * 3)
                    else:
                        self.y += CUBE_SIZE // JUMP_DURATION
                    self.jumpCount -= 1
                    if self.jumpCount == 0:
                        self.cubeNumber = self.cubeNumber - 1

                elif self.jumpDirection == RIGHT:
                    self.x -= CUBE_SIZE // (JUMP_DURATION - 1)
                    if self.jumpCount < JUMP_DURATION // 4:
                        self.y += CUBE_SIZE // (JUMP_DURATION * 2 // 3)
                    else:
                        self.y -= CUBE_SIZE // (JUMP_DURATION // 3 - 1)
                    self.jumpCount -= 1
                    if self.jumpCount == 0:
                        self.cubeNumber = self.cubeNumber - self.rowNumber
                        self.rowNumber -= 1

                if self.jumpCount == 0:
                    self.jumpDirection = STANDING
                    self.jumpCount = JUMP_DURATION // 2
                    if not valid_cube_number_and_row_coily(self.cubeNumber, self.rowNumber):
                        self.destroy = True
                    else:
                        self.x = variables.cubes[self.cubeNumber].x + CUBE_SIZE * 3 // 4
                        self.y = variables.cubes[self.cubeNumber].y + CUBE_SIZE // 4


    def draw(self):
        self.move()

        variables.game_window.blit(self.image, (self.x, self.y))

    def detect_collision(self, player: Player) -> bool:
        if player.jumpDirection == RIGHT_SPIN or player.jumpDirection == LEFT_SPIN or player.jumpDirection == FALLING:
            return False
        if abs(self.x - player.x) <= CUBE_SIZE // 4 + 3 and abs(
                self.y + CUBE_SIZE // 4 - player.y) <= CUBE_SIZE // 4 + 3:
            return True

        return False
