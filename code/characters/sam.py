import random

import variables
from characters.player import Player
from constants import *
from characters.enemy import Enemy, JUMP_DURATION
from valid_cube_number_and_row import valid_cube_number_and_row_coily


class Sam(Enemy):
    def __init__(self, image, time):
        super().__init__(image, time)
        rand_cube = random.randint(1, 2)
        self.x = variables.cubes[rand_cube].x
        self.y = variables.cubes[rand_cube].y - CUBE_SIZE * 4
        self.cubeNumber = rand_cube
        self.rowNumber = 2

    def move(self):
        if not variables.freeze:
            if self.jumpDirection == STANDING:
                self.jumpCount -= 1
                if self.jumpCount == 0:
                    random_number = random.randint(1, 2)
                    if random_number == 1:
                        self.jumpDirection = DOWN_LEFT
                        self.image = IMAGE_SAM_LEFT
                    else:
                        self.jumpDirection = DOWN_RIGHT
                        self.image = IMAGE_SAM_RIGHT
                    self.jumpCount = JUMP_DURATION // 2
            else:
                if self.jumpDirection == FALLING:
                    self.y += (CUBE_SIZE*2) // JUMP_DURATION
                    self.jumpCount -= 1

                elif self.jumpDirection == DOWN_LEFT:
                    self.x -= CUBE_SIZE // (JUMP_DURATION - 1)
                    if self.jumpCount > (JUMP_DURATION // 3):
                        self.y -= CUBE_SIZE // (JUMP_DURATION * 2 // 3)
                    else:
                        self.y += CUBE_SIZE // (JUMP_DURATION // 3 - 1)
                    self.jumpCount -= 1
                    if self.jumpCount == 0:
                        self.cubeNumber = self.cubeNumber + self.rowNumber
                        self.rowNumber += 1

                elif self.jumpDirection == DOWN_RIGHT:
                    self.x += CUBE_SIZE // (JUMP_DURATION - 1)
                    if self.jumpCount > (JUMP_DURATION // 3):
                        self.y -= CUBE_SIZE // (JUMP_DURATION * 2 // 3)
                    else:
                        self.y += CUBE_SIZE // (JUMP_DURATION // 3 - 1)
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
                        self.x = variables.cubes[self.cubeNumber].x
                        self.y = variables.cubes[self.cubeNumber].y
                        variables.cubes[self.cubeNumber].color = variables.level.colors[0]

    def draw(self):
        if variables.state == PLAYING:
            self.move()

        variables.game_window.blit(self.image, (self.x+CUBE_SIZE //
                         8, self.y - CUBE_SIZE*5//8))

    def detect_collision(self, player: Player) -> bool:
        if player.jumpDirection == LEFT_SPIN or player.jumpDirection == RIGHT_SPIN:
            return False
        if abs(self.x - player.x) <= CUBE_SIZE // 4 + 3 and abs(
                self.y + CUBE_SIZE // 4 - player.y) <= CUBE_SIZE // 4 + 3:
            self.destroy = True
            variables.score += 300

        return False
