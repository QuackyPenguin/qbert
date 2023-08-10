from typing import Optional, List
import pygame

import variables
from constants import *
from help_functions import *
from draw import draw

# initialize window

pygame.init()

game_window = pygame.display.set_mode((GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT), 0, 32)
font = pygame.font.Font(None, FONT_SIZE)

caption = 'Q*bert'
pygame.display.set_caption(caption)

# initialize game


initialize_game(game_window)

# running loop

running = True

while running:
    pygame.time.delay(25)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if variables.state == START:
        if pygame.mouse.get_pressed()[0]:
            variables.state = PLAYING
    elif variables.state == PLAYING:
        if variables.jump_direction_player == STANDING:
            if keys[pygame.K_LEFT]:
                variables.jump_direction_player = UP_LEFT
            if keys[pygame.K_RIGHT]:
                variables.jump_direction_player = DOWN_RIGHT
            if keys[pygame.K_UP]:
                variables.jump_direction_player = UP_RIGHT
            if keys[pygame.K_DOWN]:
                variables.jump_direction_player = DOWN_LEFT

    draw(game_window, font)

    pygame.display.update()

    if variables.round_completed:
        print(variables.player.x, variables.player.y)
        (variables.player.x, variables.player.y, variables.player.image,
         variables.player.cubeNumber, variables.player.rowNumber) = (
            X_CENTER - CUBE_SIZE * 3 // 8,
            Y_CENTER - CUBE_SIZE * 3 // 8,
            IMAGE_PLAYER_LEFT_DOWN, 0, 1)

        variables.score += 250
        if variables.level_completed:
            variables.score += 250
            variables.level_completed = False

        variables.round_completed = False

    if variables.player.lives == 0:
        initialize_game(game_window)
        variables.score = 0

pygame.quit()
