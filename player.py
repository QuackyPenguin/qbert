from constants import *
import variables
from valid_cube_number_and_row import valid_cube_number_and_row

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
        self.lives = 3

    def draw(self):
        if variables.jump_direction_player != self.jumpDirection and self.jumpCount == 0:
            self.jumpCount = 15
            self.jumpDirection = variables.jump_direction_player
            if variables.jump_direction_player == DOWN_LEFT:
                self.image = IMAGE_PLAYER_LEFT_DOWN
            elif variables.jump_direction_player == DOWN_RIGHT:
                self.image = IMAGE_PLAYER_RIGHT_DOWN
            elif variables.jump_direction_player == UP_LEFT:
                self.image = IMAGE_PLAYER_LEFT_UP
            elif variables.jump_direction_player == UP_RIGHT:
                self.image = IMAGE_PLAYER_RIGHT_UP
        elif self.jumpCount == 0:
            if self.jumpDirection != STANDING and not self.outOfBounds:
                variables.level.next_color(self.cubeNumber)
            if self.outOfBounds:
                self.lives -= 1
                self.outOfBounds = False
            self.jumpDirection = STANDING
            variables.jump_direction_player = STANDING
            # x_center - CUBE_SIZE * 3 // 8, y_center - CUBE_SIZE * 3 // 8
            self.x = variables.cubes[self.cubeNumber].x + CUBE_SIZE // 8
            self.y = variables.cubes[self.cubeNumber].y - CUBE_SIZE * 5 // 8
            self.outOfBounds = False

        if self.jumpCount > 0:
            change_cube = False
            if self.jumpCount == 10:
                change_cube = True

            if self.jumpDirection == DOWN_LEFT:
                self.x -= 96 // 29
                if self.jumpCount > 10:
                    self.y -= 96 // 20
                else:
                    self.y += 96 // 9
                self.jumpCount -= 1
                if change_cube:
                    self.cubeNumber = self.cubeNumber + self.rowNumber
                    self.rowNumber += 1

            elif self.jumpDirection == DOWN_RIGHT:
                self.x += 96 // 29
                if self.jumpCount > 10:
                    self.y -= 96 // 20
                else:
                    self.y += 96 // 9
                self.jumpCount -= 1
                if change_cube:
                    self.cubeNumber = self.cubeNumber + self.rowNumber + 1
                    self.rowNumber += 1

            elif self.jumpDirection == UP_RIGHT:
                self.x += 96 // 29
                if self.jumpCount < 6:
                    self.y += 96 // 20
                else:
                    self.y -= 96 // 9
                self.jumpCount -= 1
                if change_cube:
                    self.cubeNumber = self.cubeNumber - self.rowNumber + 1
                    self.rowNumber -= 1

            elif self.jumpDirection == UP_LEFT:
                self.x -= 96 // 29
                if self.jumpCount < 6:
                    self.y += 96 // 20
                else:
                    self.y -= 96 // 9
                self.jumpCount -= 1
                if change_cube:
                    self.cubeNumber = self.cubeNumber - self.rowNumber
                    self.rowNumber -= 1

            if change_cube:
                if not valid_cube_number_and_row(self.cubeNumber, self.rowNumber):
                    self.cubeNumber = 0
                    self.rowNumber = 1
                    self.outOfBounds = True
                    # TODO lose life, insert pause

        self.window.blit(self.image, (self.x, self.y))

        for i in range(0, self.lives):
            self.window.blit(IMAGE_PLAYER_LITTLE, (10, 300 + i * 20))
