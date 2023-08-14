import variables
from constants import *
from valid_cube_number_and_row import valid_cube_number_and_row

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
        self.outOfBounds = False
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
            if self.jumpDirection != STANDING and not self.outOfBounds:
                variables.level.next_color(self.cubeNumber)
            if self.outOfBounds:
                self.lives -= 1
                variables.state = ONE_SECOND_PAUSE

            self.jumpDirection = STANDING
            variables.jump_direction_player = STANDING
            self.x = variables.cubes[self.cubeNumber].x
            self.y = variables.cubes[self.cubeNumber].y
            self.outOfBounds = False

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
                self.x += (CUBE_SIZE * 21 // 8) // 44
                self.y -= (CUBE_SIZE * 3) // 44
                if self.image == IMAGE_PLAYER_SPINS[0]:
                    self.image = IMAGE_PLAYER_SPINS[1]
                else:
                    self.image = IMAGE_PLAYER_SPINS[0]
                self.jumpCount -= 1
                if self.jumpCount == 0:
                    self.x += 15
                    self.jumpDirection = FALLING
                    self.jumpCount = (JUMP_DURATION * 2 // 3)
                    self.image = IMAGE_PLAYER_LEFT_DOWN

            elif self.jumpDirection == RIGHT_SPIN:
                self.x -= (CUBE_SIZE * 21 // 8) // 44
                self.y -= (CUBE_SIZE * 3) // 44
                if self.image == IMAGE_PLAYER_SPINS[0]:
                    self.image = IMAGE_PLAYER_SPINS[1]
                else:
                    self.image = IMAGE_PLAYER_SPINS[0]
                self.jumpCount -= 1
                if self.jumpCount == 0:
                    self.x -= 15
                    self.jumpDirection = FALLING
                    self.jumpCount = (JUMP_DURATION * 2 // 3)
                    self.image = IMAGE_PLAYER_LEFT_DOWN

            elif self.jumpDirection == FALLING:
                self.y += (CUBE_SIZE // 2) // (JUMP_DURATION * 2 // 3)
                self.jumpCount -= 1
                if self.jumpCount == 0:
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

                if self.rowNumber == 4 and ((self.cubeNumber == 5 and self.leftPlatform) or
                                            (self.cubeNumber == 10 and self.rightPlatform)):
                    if self.cubeNumber == 5:
                        self.jumpDirection = LEFT_SPIN
                        self.leftPlatform = False
                    else:
                        self.jumpDirection = RIGHT_SPIN
                        self.rightPlatform = False
                    variables.jump_direction_player = self.jumpDirection
                    self.image = IMAGE_PLAYER_SPINS[self.jumpDirection - LEFT_SPIN]
                    self.jumpCount = 45
                elif not valid_cube_number_and_row(self.cubeNumber, self.rowNumber):
                    self.cubeNumber = 0
                    self.rowNumber = 1
                    self.outOfBounds = True

        self.window.blit(self.image, (self.x + CUBE_SIZE // 8, self.y - CUBE_SIZE * 5 // 8))

        for i in range(0, self.lives):
            self.window.blit(IMAGE_PLAYER_LITTLE, ((JUMP_DURATION * 2 // 3), 300 + i * (JUMP_DURATION * 4 // 3)))
