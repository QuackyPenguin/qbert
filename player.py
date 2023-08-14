import variables
from constants import *

JUMP_DURATION = 12


class Player:
    def __init__(self, x, y, image, window):
        self.x = x
        self.y = y
        self.image = image
        self.window = window
        self.cubeNumber = 0
        self.rowNumber = 1
        self.jumpDirection = STANDING
        self.jumpCount = 0
        self.leftPlatform = True
        self.rightPlatform = True
        self.lives = 3

    def draw(self):
        if variables.jump_direction_player != self.jumpDirection and self.jumpCount == 0:
            self.jumpCount = JUMP_DURATION
            self.jumpDirection = variables.jump_direction_player
            if variables.jump_direction_player == DOWN_LEFT:
                self.image = IMAGE_PLAYER_LEFT_DOWN
            elif variables.jump_direction_player == DOWN_RIGHT:
                self.image = IMAGE_PLAYER_RIGHT_DOWN
            elif variables.jump_direction_player == UP_LEFT:
                self.image = IMAGE_PLAYER_LEFT_UP
            elif variables.jump_direction_player == UP_RIGHT:
                self.image = IMAGE_PLAYER_RIGHT_UP
        elif self.jumpCount == 0 and RIGHT_SPIN != self.jumpDirection != LEFT_SPIN:
            if self.jumpDirection != STANDING:
                variables.level.next_color(self.cubeNumber)

            self.jumpDirection = STANDING
            variables.jump_direction_player = STANDING
            self.x = variables.cubes[self.cubeNumber].x
            self.y = variables.cubes[self.cubeNumber].y

        if self.jumpCount > 0:

            if self.jumpDirection == DOWN_LEFT:
                self.x -= CUBE_SIZE // (2 * JUMP_DURATION - 1)
                if self.jumpCount > (JUMP_DURATION * 2 // 3):
                    self.y -= CUBE_SIZE // (JUMP_DURATION * 4 // 3)
                else:
                    self.y += CUBE_SIZE // (JUMP_DURATION * 2 // 3 - 1)
                self.jumpCount -= 1
                if self.jumpCount == 0:
                    self.cubeNumber = self.cubeNumber + self.rowNumber
                    self.rowNumber += 1

            elif self.jumpDirection == DOWN_RIGHT:
                self.x += CUBE_SIZE // (2 * JUMP_DURATION - 1)
                if self.jumpCount > (JUMP_DURATION * 2 // 3):
                    self.y -= CUBE_SIZE // (JUMP_DURATION * 4 // 3)
                else:
                    self.y += CUBE_SIZE // (JUMP_DURATION * 2 // 3 - 1)
                self.jumpCount -= 1
                if self.jumpCount == 0:
                    self.cubeNumber = self.cubeNumber + self.rowNumber + 1
                    self.rowNumber += 1

            elif self.jumpDirection == UP_RIGHT:
                self.x += CUBE_SIZE // (2 * JUMP_DURATION - 1)
                if self.jumpCount < JUMP_DURATION // 2:
                    self.y += CUBE_SIZE // (JUMP_DURATION * 4 // 3)
                else:
                    self.y -= CUBE_SIZE // (JUMP_DURATION * 2 // 3 - 1)
                self.jumpCount -= 1
                if self.jumpCount == 0:
                    self.cubeNumber = self.cubeNumber - self.rowNumber + 1
                    self.rowNumber -= 1

            elif self.jumpDirection == UP_LEFT:
                self.x -= CUBE_SIZE // (2 * JUMP_DURATION - 1)
                if self.jumpCount < JUMP_DURATION // 2:
                    self.y += CUBE_SIZE // (JUMP_DURATION * 4 // 3)
                else:
                    self.y -= CUBE_SIZE // (JUMP_DURATION * 2 // 3 - 1)
                self.jumpCount -= 1
                if self.jumpCount == 0:
                    self.cubeNumber = self.cubeNumber - self.rowNumber
                    self.rowNumber -= 1

            elif self.jumpDirection == LEFT_SPIN:
                self.x += ((variables.cubes[0].x) - variables.helpx) // 44
                self.y -= (variables.helpy + CUBE_SIZE - variables.cubes[0].y) // 44
                if self.image == IMAGE_PLAYER_SPINS[0]:
                    self.image = IMAGE_PLAYER_SPINS[1]
                else:
                    self.image = IMAGE_PLAYER_SPINS[0]
                self.jumpCount -= 1
                if self.jumpCount == 0:
                    self.x = variables.cubes[0].x
                    self.jumpDirection = FALLING
                    self.jumpCount = (JUMP_DURATION * 2 // 3)
                    self.image = IMAGE_PLAYER_LEFT_DOWN

            elif self.jumpDirection == RIGHT_SPIN:
                self.x -= (variables.helpx - (variables.cubes[0].x)) // 44
                self.y -= (variables.helpy + CUBE_SIZE - variables.cubes[0].y) // 44
                if self.image == IMAGE_PLAYER_SPINS[0]:
                    self.image = IMAGE_PLAYER_SPINS[1]
                else:
                    self.image = IMAGE_PLAYER_SPINS[0]
                self.jumpCount -= 1
                if self.jumpCount == 0:
                    self.x = variables.cubes[0].x
                    self.jumpDirection = FALLING
                    self.jumpCount = (JUMP_DURATION * 2 // 3)
                    self.image = IMAGE_PLAYER_LEFT_DOWN

            elif self.jumpDirection == FALLING:
                self.y += (CUBE_SIZE // 2) // (JUMP_DURATION * 2 // 3)
                self.jumpCount -= 1
                if self.jumpCount == 0:
                    for disc in variables.discs:
                        if disc.cube == self.cubeNumber and disc.row == self.rowNumber:
                            disc.used = True
                            break
                    self.jumpDirection = STANDING
                    variables.jump_direction_player = STANDING
                    self.cubeNumber = 0
                    self.rowNumber = 1
                    variables.level.next_color(self.cubeNumber)

            if self.jumpCount == 0:
                if variables.jump_direction_player == DOWN_LEFT:
                    self.image = IMAGE_PLAYER_LEFT_DOWN_JUMP
                elif variables.jump_direction_player == DOWN_RIGHT:
                    self.image = IMAGE_PLAYER_RIGHT_DOWN_JUMP
                elif variables.jump_direction_player == UP_LEFT:
                    self.image = IMAGE_PLAYER_LEFT_UP_JUMP
                elif variables.jump_direction_player == UP_RIGHT:
                    self.image = IMAGE_PLAYER_RIGHT_UP_JUMP

        self.window.blit(self.image, (self.x + CUBE_SIZE // 8, self.y - CUBE_SIZE * 5 // 8))

        for i in range(0, self.lives):
            self.window.blit(IMAGE_PLAYER_LITTLE, (20, 300 + i * 30))
