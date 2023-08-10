from constants import *
import variables


def draw(game_window, font):
    if variables.state == START:
        game_window.blit(IMAGE_START_PAGE, (0, 0))
    elif variables.state == PLAYING:
        game_window.fill(COLOR_BLACK)

        for cube in variables.cubes:
            cube.draw()

        variables.player.draw()

        for red_ball in variables.red_balls:
            red_ball.draw()
            if red_ball.destroy:
                variables.red_balls.remove(red_ball)

        text = font.render(str(variables.score), True, COLOR_ORANGE)
        text_rect = text.get_rect(center=(100, 120))
        game_window.blit(text, text_rect)

        text = font.render("Level " + str(variables.level.level) + ", round " + str(variables.level.round), True,
                           COLOR_RED)
        text_rect = text.get_rect(center=(750, 120))
        game_window.blit(text, text_rect)
