import player
import variables
from constants import *
from cube import Cube, make_color_grayer


def draw_requested(font, game_window):
    text = font.render("COLOR --->", True, COLOR_SKY_BLUE)
    text_rect = text.get_rect(center=(120, 200))
    game_window.blit(text, text_rect)

    x = 200
    y = 175 + CUBE_SIZE//4

    vertices = [(x, y), (x + CUBE_SIZE // 2, y + CUBE_SIZE // 4),
                (x + CUBE_SIZE, y),
                (x + CUBE_SIZE // 2, y - CUBE_SIZE // 4)]

    pygame.draw.polygon(game_window, variables.level.colors[len(variables.level.colors)-1], vertices)
    pygame.draw.lines(game_window, COLOR_GRAY, points=vertices, closed=True)

    vertices = [(x, y), (x + CUBE_SIZE // 2, y + CUBE_SIZE // 4),
                (x + CUBE_SIZE // 2, y + CUBE_SIZE // 2),
                (x, y + CUBE_SIZE // 4)]

    pygame.draw.polygon(game_window, make_color_grayer(COLOR_GRAY, 0.6), vertices)
    pygame.draw.lines(game_window, COLOR_GRAY, points=vertices, closed=True)

    vertices = [(x + CUBE_SIZE // 2, y + CUBE_SIZE // 4), (x + CUBE_SIZE, y),
                (x + CUBE_SIZE, y + CUBE_SIZE // 4),
                (x + CUBE_SIZE // 2, y + CUBE_SIZE // 2)]

    pygame.draw.polygon(game_window, make_color_grayer(COLOR_GRAY, 0.4), vertices)
    pygame.draw.lines(game_window, COLOR_GRAY, points=vertices, closed=True)


def draw(game_window, font):
    if variables.state == START:
        game_window.blit(IMAGE_START_PAGE, (0, 0))
    elif variables.state == PLAYING:
        game_window.fill(COLOR_BLACK)

        for cube in variables.cubes:
            cube.draw()
        draw_requested(font, game_window)

        for disc in variables.discs:
            if disc.used or disc.inuse:
                continue
            offset = 1
            if disc.side == 2:
                offset = -1
            game_window.blit(IMAGE_DISK, (variables.cubes[disc.cube + offset].x + CUBE_SIZE * offset * (-1),
                                          variables.cubes[disc.cube + offset].y - CUBE_SIZE // 4))

        variables.player.draw()

        for enemy in variables.enemies:
            enemy.draw()
            if enemy.destroy:
                variables.enemies.remove(enemy)

        text = font.render(str(variables.score), True, COLOR_ORANGE)
        text_rect = text.get_rect(center=(100, 120))
        game_window.blit(text, text_rect)

        text = font.render("Level " + str(variables.level.level) + ", round " + str(variables.level.round), True,
                           COLOR_RED)
        text_rect = text.get_rect(center=(750, 120))
        game_window.blit(text, text_rect)
    elif variables.state == ONE_SECOND_PAUSE:
        if variables.celebrate:
            variables.rainbow_color = variables.rainbow_color % (len(RAINBOW)*5)
            for cube in variables.cubes:
                cube.color = RAINBOW[variables.rainbow_color//5]
                cube.draw()
            variables.player.draw()
            variables.rainbow_color += 1
        elif variables.game_time * variables.speed >= 2000:
            game_window.blit(IMAGE_SWEAR, (variables.player.x + 65, variables.player.y - 65))
    elif variables.state == GAME_OVER:
        game_window.blit(IMAGE_QBERT_LOSES, (0, 0))
    pass
