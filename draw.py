import variables
from constants import *


def draw(game_window, font):
    if variables.state == START:
        game_window.blit(IMAGE_START_PAGE, (0, 0))
    elif variables.state == PLAYING:
        game_window.fill(COLOR_BLACK)

        for cube in variables.cubes:
            cube.draw()

        for disc in variables.discs:
            if disc.used or disc.inuse:
                continue
            offset = 1
            if disc.side == 2:
                offset = -1
            game_window.blit(IMAGE_DISK, (variables.cubes[disc.cube + offset].x + CUBE_SIZE * offset * (-1),
                                          variables.cubes[disc.cube + offset].y - CUBE_SIZE // 2))

        variables.player.draw()

        for red_ball in variables.enemies:
            red_ball.draw()
            if red_ball.destroy:
                variables.enemies.remove(red_ball)

        text = font.render(str(variables.score), True, COLOR_ORANGE)
        text_rect = text.get_rect(center=(100, 120))
        game_window.blit(text, text_rect)

        text = font.render("Level " + str(variables.level.level) + ", round " + str(variables.level.round), True,
                           COLOR_RED)
        text_rect = text.get_rect(center=(750, 120))
        game_window.blit(text, text_rect)
    elif variables.state == ONE_SECOND_PAUSE:
        if variables.game_time * variables.speed >= 2000:
            game_window.blit(IMAGE_SWEAR, (variables.player.x+65, variables.player.y - 65))
    elif variables.state == GAME_OVER:
        game_window.blit(IMAGE_QBERT_LOSES, (0, 0))
    pass
