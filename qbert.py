import variables
from draw import draw
from initialize_game import *
from valid_cube_number_and_row import valid_cube_number_and_row

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
    pygame.time.delay(variables.speed)
    variables.game_time += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if variables.state == START:
        if pygame.mouse.get_pressed()[0]:
            SOUND_GAMESTART.play()
            variables.state = ONE_SECOND_PAUSE
            initialize_game(game_window)
            counter = 0
            variables.round_completed = True
            variables.game_time = 0

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
            variables.state = ONE_SECOND_PAUSE
            variables.rainbow_color = 0
            variables.game_time = 0

        if nextEnemyTime == variables.game_time:
            enemy = variables.level.generate_enemy(game_window)
            if enemy is not None:
                variables.enemies.append(enemy)
            nextEnemyTime = variables.level.next_enemy_appearance()

        if not variables.freeze:
            for enemy in variables.enemies:
                if enemy.detect_collision(variables.player):
                    variables.player.lives -= 1
                    variables.state = ONE_SECOND_PAUSE
                    break
        else:
            nextEnemyTime = -1
            variables.freeze_timer += 1
            if variables.freeze_timer * variables.speed >= 1500:
                variables.freeze = False
                variables.freeze_timer = 0
                nextEnemyTime = variables.level.next_enemy_appearance()

        if not valid_cube_number_and_row(variables.player.cubeNumber, variables.player.rowNumber):
            variables.state = ONE_SECOND_PAUSE
            variables.player.lives -= 1
            variables.player.cubeNumber = 0
            variables.player.rowNumber = 1
        else:
            for disc in variables.discs:
                if disc.cube == variables.player.cubeNumber and disc.row == variables.player.rowNumber and not disc.inuse:
                    if disc.side == 1:
                        variables.player.jumpDirection = LEFT_SPIN
                    else:
                        variables.player.jumpDirection = RIGHT_SPIN

                    variables.jump_direction_player = variables.player.jumpDirection
                    variables.player.image = IMAGE_PLAYER_SPINS[variables.player.jumpDirection - LEFT_SPIN]
                    variables.player.jumpCount = 45
                    disc.inuse = True
                    variables.helpx = variables.player.x
                    variables.helpy = variables.player.y
                    variables.player.cubeNumber = disc.cube
                    variables.player.rowNumber = disc.row
                    break

        if variables.player.lives == 0:
            initialize_game(game_window)
            variables.score = 0
            variables.state = GAME_OVER

    elif variables.state == ONE_SECOND_PAUSE:
        counter += 1
        if counter * variables.speed >= 1000:
            variables.state = PLAYING
            variables.enemies = []
            counter = 0
            variables.celebrate = False
            if variables.round_completed:
                variables.level.init_next_level()
            variables.game_time = 0
            nextEnemyTime = variables.level.next_enemy_appearance()

    elif variables.state == GAME_OVER:
        keys = pygame.key.get_pressed()
        variables.game_time = 0
        if keys[pygame.K_r] or keys[pygame.K_ESCAPE]:
            variables.state = START
            variables.enemies = []

    draw(game_window, font)

    pygame.display.flip()

pygame.quit()
