import random

import variables
from constants import *
from enemy import JUMP_DURATION, Enemy
from valid_cube_number_and_row import valid_cube_number_and_row, valid_cube_number_and_row_coily

EGG = 0
HATCHING = 1
SNAKE = 2


def direction(coily_cube, coily_row, player_cube, player_row):
    coily_modifier = (coily_row * (coily_row + 1) // 2 + coily_row * (coily_row - 1) // 2) // 2
    mod_coily_cube = coily_cube - coily_modifier
    player_modifier = (player_row * (player_row + 1) // 2 + player_row * (player_row - 1) // 2) // 2
    mod_player_cube = player_cube - player_modifier

    randomized_1 = False
    return_value_1 = (None, None)

    if player_row > coily_row:
        if mod_player_cube > mod_coily_cube:
            return_value_1 = DOWN_RIGHT, IMAGE_COILY_RIGHT
        elif mod_player_cube < mod_coily_cube:
            return_value_1 = DOWN_LEFT, IMAGE_COILY_LEFT
        else:
            if not valid_cube_number_and_row(coily_cube + coily_row, coily_row + 1):
                return_value_1 = DOWN_RIGHT, IMAGE_COILY_RIGHT
            elif not valid_cube_number_and_row(coily_cube + coily_row + 1, coily_row + 1):
                return_value_1 = DOWN_LEFT, IMAGE_COILY_LEFT
            else:
                if player_row - coily_row == 1:
                    if coily_row % 2 == 0:
                        return_value_1 = DOWN_LEFT, IMAGE_COILY_LEFT
                    else:
                        return_value_1 = DOWN_RIGHT, IMAGE_COILY_RIGHT
                else:
                    randomized_1 = True
                    random_number = random.randint(1, 2)
                    if random_number == 1:
                        return_value_1 = DOWN_LEFT, IMAGE_COILY_LEFT
                    else:
                        return_value_1 = DOWN_RIGHT, IMAGE_COILY_RIGHT
    elif player_row < coily_row:
        if mod_player_cube > mod_coily_cube:
            return_value_1 = UP_RIGHT, IMAGE_COILY_RIGHT
        elif mod_player_cube < mod_coily_cube:
            return_value_1 = UP_LEFT, IMAGE_COILY_LEFT
        else:
            if not valid_cube_number_and_row(coily_cube - coily_row, coily_row - 1):
                return_value_1 = UP_RIGHT, IMAGE_COILY_RIGHT
            elif not valid_cube_number_and_row(coily_cube - coily_row + 1, coily_row - 1):
                return_value_1 = UP_LEFT, IMAGE_COILY_LEFT
            else:
                if coily_row - player_row == 1:
                    if coily_row % 2 == 1:
                        return_value_1 = UP_RIGHT, IMAGE_COILY_RIGHT
                    else:
                        return_value_1 = UP_LEFT, IMAGE_COILY_LEFT
                else:
                    randomized_1 = True
                    random_number = random.randint(1, 2)
                    if random_number == 1:
                        return_value_1 = UP_LEFT, IMAGE_COILY_LEFT
                    else:
                        return_value_1 = UP_RIGHT, IMAGE_COILY_RIGHT
    else:
        randomized_1 = True
        option_array = []
        if valid_cube_number_and_row(coily_cube + coily_row,
                                     coily_row + 1) and mod_coily_cube > mod_player_cube:
            option_array.append(1)
        if valid_cube_number_and_row(coily_cube + coily_row + 1,
                                     coily_row + 1) and mod_coily_cube < mod_player_cube:
            option_array.append(2)
        if valid_cube_number_and_row(coily_cube - coily_row,
                                     coily_row - 1) and mod_coily_cube > mod_player_cube:
            option_array.append(3)
        if valid_cube_number_and_row(coily_cube - coily_row - 1,
                                     coily_row - 1) and mod_coily_cube < mod_player_cube:
            option_array.append(4)

        random_number = random.randint(0, len(option_array) - 1)
        if option_array[random_number] == 1:
            return_value_1 = DOWN_LEFT, IMAGE_COILY_LEFT
        elif option_array[random_number] == 2:
            return_value_1 = DOWN_RIGHT, IMAGE_COILY_RIGHT
        elif option_array[random_number] == 3:
            return_value_1 = UP_LEFT, IMAGE_COILY_LEFT
        else:
            return_value_1 = UP_RIGHT, IMAGE_COILY_RIGHT

    mod_coily_cube += ((coily_row + 1) % 2)
    mod_player_cube += ((player_row + 1) % 2)

    randomized_2 = False
    return_value_2 = (None, None)

    if player_row > coily_row:
        if mod_player_cube > mod_coily_cube:
            return_value_2 = DOWN_RIGHT, IMAGE_COILY_RIGHT
        elif mod_player_cube < mod_coily_cube:
            return_value_2 = DOWN_LEFT, IMAGE_COILY_LEFT
        else:
            if not valid_cube_number_and_row(coily_cube + coily_row, coily_row + 1):
                return_value_2 = DOWN_RIGHT, IMAGE_COILY_RIGHT
            elif not valid_cube_number_and_row(coily_cube + coily_row + 1, coily_row + 1):
                return_value_2 = DOWN_LEFT, IMAGE_COILY_LEFT
            else:
                if player_row - coily_row == 1:
                    if coily_row % 2 == 1:
                        return_value_2 = DOWN_LEFT, IMAGE_COILY_LEFT
                    else:
                        return_value_2 = DOWN_RIGHT, IMAGE_COILY_RIGHT
                else:
                    randomized_2 = True
                    random_number = random.randint(1, 2)
                    if random_number == 1:
                        return_value_2 = DOWN_LEFT, IMAGE_COILY_LEFT
                    else:
                        return_value_2 = DOWN_RIGHT, IMAGE_COILY_RIGHT
    elif player_row < coily_row:
        if mod_player_cube > mod_coily_cube:
            return_value_2 = UP_RIGHT, IMAGE_COILY_RIGHT
        elif mod_player_cube < mod_coily_cube:
            return_value_2 = UP_LEFT, IMAGE_COILY_LEFT
        else:
            if not valid_cube_number_and_row(coily_cube - coily_row, coily_row - 1):
                return_value_2 = UP_RIGHT, IMAGE_COILY_RIGHT
            elif not valid_cube_number_and_row(coily_cube - coily_row + 1, coily_row - 1):
                return_value_2 = UP_LEFT, IMAGE_COILY_LEFT
            else:
                if coily_row - player_row == 1:
                    if coily_row % 2 == 1:
                        return_value_2 = UP_LEFT, IMAGE_COILY_LEFT
                    else:
                        return_value_2 = UP_RIGHT, IMAGE_COILY_RIGHT
                else:
                    randomized_2 = True
                    random_number = random.randint(1, 2)
                    if random_number == 1:
                        return_value_2 = UP_LEFT, IMAGE_COILY_LEFT
                    else:
                        return_value_2 = UP_RIGHT, IMAGE_COILY_RIGHT
    else:
        randomized_2 = True
        option_array = []
        if valid_cube_number_and_row(coily_cube + coily_row,
                                     coily_row + 1) and mod_coily_cube > mod_player_cube:
            option_array.append(1)
        if valid_cube_number_and_row(coily_cube + coily_row + 1,
                                     coily_row + 1) and mod_coily_cube < mod_player_cube:
            option_array.append(2)
        if valid_cube_number_and_row(coily_cube - coily_row,
                                     coily_row - 1) and mod_coily_cube > mod_player_cube:
            option_array.append(3)
        if valid_cube_number_and_row(coily_cube - coily_row - 1,
                                     coily_row - 1) and mod_coily_cube < mod_player_cube:
            option_array.append(4)

        random_number = random.randint(0, len(option_array) - 1)
        if option_array[random_number] == 1:
            return_value_2 = DOWN_LEFT, IMAGE_COILY_LEFT
        elif option_array[random_number] == 2:
            return_value_2 = DOWN_RIGHT, IMAGE_COILY_RIGHT
        elif option_array[random_number] == 3:
            return_value_2 = UP_LEFT, IMAGE_COILY_LEFT
        else:
            return_value_2 = UP_RIGHT, IMAGE_COILY_RIGHT

    if randomized_1 and not randomized_2:
        return return_value_2
    if not randomized_1 and randomized_2:
        return return_value_1

    random_number = random.randint(1, 2)
    if random_number == 1:
        return return_value_1
    else:
        return return_value_2


class Coily(Enemy):
    def __init__(self, image, window, time):
        super().__init__(image, window, time)
        rand_cube = random.randint(1, 2)
        self.x = variables.cubes[rand_cube].x
        self.y = variables.cubes[rand_cube].y - CUBE_SIZE * 4
        self.cubeNumber = rand_cube
        self.rowNumber = 2
        self.version = EGG

    def draw_egg(self):
        if self.jumpCount == 0:
            if not valid_cube_number_and_row(self.cubeNumber + self.rowNumber, self.rowNumber + 1):
                self.jumpDirection = DOWN_RIGHT
            elif not valid_cube_number_and_row(self.cubeNumber + self.rowNumber + 1, self.rowNumber + 1):
                self.jumpDirection = DOWN_LEFT
            else:
                self.jumpDirection = random.randint(1, 2)
            self.x = variables.cubes[self.cubeNumber].x
            self.y = variables.cubes[self.cubeNumber].y
            self.jumpCount = JUMP_DURATION

        else:
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

            if self.jumpCount == 0 and self.rowNumber == 7:
                self.version = HATCHING
                self.jumpCount = JUMP_DURATION * 2
                self.jumpDirection = UP_LEFT
        self.window.blit(self.image, (self.x + CUBE_SIZE * 3 // 8, self.y - CUBE_SIZE * 1 // 4))

    def draw_hatch(self):
        if self.jumpCount == 0:
            self.version = SNAKE
            self.image = IMAGE_COILY_LEFT
            self.jumpDirection = STANDING
            self.jumpCount = JUMP_DURATION // 2
        else:
            self.jumpCount -= 1
            if self.jumpCount % 3 == 0:
                if self.jumpDirection == UP_LEFT:
                    self.jumpDirection = UP_RIGHT
                elif self.jumpDirection == UP_RIGHT:
                    self.jumpDirection = DOWN_RIGHT
                elif self.jumpDirection == DOWN_RIGHT:
                    self.jumpDirection = DOWN_LEFT
                elif self.jumpDirection == DOWN_LEFT:
                    self.jumpDirection = UP_LEFT

            if self.jumpDirection == UP_LEFT:
                self.window.blit(self.image,
                                 (self.x + CUBE_SIZE * 3 // 8, self.y - CUBE_SIZE * 1 // 4 - JUMP_DURATION // 4))
            elif self.jumpDirection == UP_RIGHT:
                self.window.blit(self.image,
                                 (self.x + CUBE_SIZE * 3 // 8 + JUMP_DURATION // 4, self.y - CUBE_SIZE * 1 // 4))
            elif self.jumpDirection == DOWN_RIGHT:
                self.window.blit(self.image,
                                 (self.x + CUBE_SIZE * 3 // 8, self.y - CUBE_SIZE * 1 // 4 + JUMP_DURATION // 4))
            elif self.jumpDirection == DOWN_LEFT:
                self.window.blit(self.image,
                                 (self.x + CUBE_SIZE * 3 // 8 - JUMP_DURATION // 4, self.y - CUBE_SIZE * 1 // 4))

    def draw_snake(self):
        if self.jumpDirection == STANDING:
            self.jumpCount -= 1
            if self.jumpCount == 0:
                self.jumpDirection, self.image = direction(self.cubeNumber, self.rowNumber, variables.player.cubeNumber,
                                                           variables.player.rowNumber)
                self.jumpCount = JUMP_DURATION // 2

        else:
            if self.jumpDirection == DOWN_LEFT:
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

            elif self.jumpDirection == UP_RIGHT:
                self.x += CUBE_SIZE // (JUMP_DURATION - 1)
                if self.jumpCount < JUMP_DURATION // 4:
                    self.y += CUBE_SIZE // (JUMP_DURATION * 2 // 3)
                else:
                    self.y -= CUBE_SIZE // (JUMP_DURATION // 3 - 1)
                self.jumpCount -= 1
                if self.jumpCount == 0:
                    self.cubeNumber = self.cubeNumber - self.rowNumber + 1
                    self.rowNumber -= 1

            elif self.jumpDirection == UP_LEFT:
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
                if self.jumpDirection == DOWN_LEFT or self.jumpDirection == UP_LEFT:
                    self.image = IMAGE_COILY_LEFT_JUMP
                else:
                    self.image = IMAGE_COILY_RIGHT_JUMP
                self.jumpDirection = STANDING
                self.jumpCount = JUMP_DURATION // 2
                if not valid_cube_number_and_row_coily(self.cubeNumber, self.rowNumber):
                    self.destroy = True
                else:
                    self.x = variables.cubes[self.cubeNumber].x
                    self.y = variables.cubes[self.cubeNumber].y

        self.window.blit(self.image, (self.x + CUBE_SIZE * 1 // 8, self.y - CUBE_SIZE * 3 // 4))

    def draw(self):
        if self.version == EGG:
            self.draw_egg()
        elif self.version == HATCHING:
            self.draw_hatch()
        else:
            self.draw_snake()
