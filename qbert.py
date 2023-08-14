import random

from coily import Coily
from draw import draw
from enemy import Enemy
from initialize_game import *
from red_ball import RedBall

speed = 31


def next_enemy_appearance():
    time = variables.game_time + random.randint(4, 8) * 15
    return time


def generate_enemy() -> Enemy:
    red_ball_odds = 2 / 3
    coily_odds = 1 / 3
    number_of_red_balls = 0
    coily_alive = False

    for enemy in variables.enemies:
        if isinstance(enemy, RedBall):
            number_of_red_balls += 1
        elif isinstance(enemy, Coily):
            coily_alive = True

    if coily_alive:
        coily_odds = 0
        red_ball_odds = 100
    else:
        red_ball_odds -= number_of_red_balls / 9
        coily_odds += number_of_red_balls / 9

    red_ball_odds *= 100
    coily_odds *= 100

    random_number = random.randint(1, 100)
    if random_number <= red_ball_odds:
        return RedBall(IMAGE_RED_BALL, game_window, variables.game_time)
    else:
        return Coily(IMAGE_PURPLE_BALL, game_window, variables.game_time)


# initialize window

pygame.init()

game_window = pygame.display.set_mode((GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT), 0, 32)
font = pygame.font.Font(None, FONT_SIZE)

caption = 'Q*bert'
pygame.display.set_caption(caption)

# running loop

counter = 0
nextEnemyTime = 0
running = True

while running:
    pygame.time.delay(speed)
    variables.game_time += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if variables.state == START:
        if pygame.mouse.get_pressed()[0]:
            variables.state = PLAYING
            nextEnemyTime = (next_enemy_appearance() // 2)
            initialize_game(game_window)
            counter = 0

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

        if variables.round_completed:
            (variables.player.x, variables.player.y, variables.player.image,
             variables.player.cubeNumber, variables.player.rowNumber,
             variables.player.leftPlatform, variables.player.rightPlatform) = (
                X_CENTER - CUBE_SIZE * 3 // 8,
                Y_CENTER - CUBE_SIZE * 3 // 8,
                IMAGE_PLAYER_LEFT_DOWN, 0, 1, True, True)
            variables.enemies = []
            nextEnemyTime = next_enemy_appearance()

            variables.score += 250
            if variables.level_completed:
                variables.score += 250
                variables.level_completed = False

            variables.round_completed = False
            variables.state = ONE_SECOND_PAUSE

        if nextEnemyTime == variables.game_time:
            variables.enemies.append(generate_enemy())
            nextEnemyTime = next_enemy_appearance()

        for enemy in variables.enemies:
            if enemy.detect_collision(variables.player):
                variables.player.lives -= 1
                variables.state = ONE_SECOND_PAUSE
                break

        if variables.player.lives == 0:
            initialize_game(game_window)
            variables.score = 0
            variables.state = GAME_OVER

    elif variables.state == ONE_SECOND_PAUSE:
        counter += 1
        if counter * speed >= 1000:
            variables.state = PLAYING
            variables.enemies = []
            counter = 0
            nextEnemyTime = next_enemy_appearance()

    elif variables.state == GAME_OVER:
        keys = pygame.key.get_pressed()
        variables.game_time = 0
        if keys[pygame.K_r] or keys[pygame.K_ESCAPE]:
            variables.state = START
            variables.enemies = []

    draw(game_window, font)

    pygame.display.flip()

pygame.quit()
