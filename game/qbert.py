from draw import draw
from initialize_game import *
from valid_cube_number_and_row import valid_cube_number_and_row
import pygame
import variables


class QbertGame:
    def __init__(self) -> None:
        self.counter = 0
        self.nextEnemyTime = 0
        variables.speed = 35

    def play_step(self):
        pygame.time.delay(variables.speed)
        variables.game_time += 1
        keys = pygame.key.get_pressed()

        if variables.state == START:
            if pygame.mouse.get_pressed()[0]:
                SOUND_GAMESTART.play()
                variables.state = ONE_SECOND_PAUSE
                initialize_game()
                self.counter = 0
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

            if self.nextEnemyTime == variables.game_time:
                enemy = variables.level.generate_enemy()
                if enemy is not None:
                    variables.enemies.append(enemy)
                self.nextEnemyTime = variables.level.next_enemy_appearance()

            if not variables.freeze:
                for enemy in variables.enemies:
                    if enemy.detect_collision(variables.player):
                        variables.player.lives -= 1
                        variables.state = ONE_SECOND_PAUSE
                        break
            else:
                self.nextEnemyTime = -1
                variables.freeze_timer += variables.speed
                if variables.freeze_timer >= 120:
                    variables.freeze = False
                    variables.freeze_timer = 0
                    self.nextEnemyTime = variables.level.next_enemy_appearance()

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

            
            for enemy in variables.enemies:
                if enemy.destroy:
                    variables.enemies.remove(enemy)              

            if variables.player.lives == 0:
                initialize_game()
                variables.score = 0
                variables.state = GAME_OVER

        elif variables.state == ONE_SECOND_PAUSE:
            self.counter += 1
            if self.counter * variables.speed >= 1000:
                variables.state = PLAYING
                variables.enemies = []
                self.counter = 0
                variables.celebrate = False
                if variables.round_completed:
                    variables.level.init_next_level()
                variables.game_time = 0
                self.nextEnemyTime = variables.level.next_enemy_appearance()

        elif variables.state == GAME_OVER:
            keys = pygame.key.get_pressed()
            variables.game_time = 0
            if keys[pygame.K_r] or keys[pygame.K_ESCAPE]:
                variables.state = START
                variables.enemies = []

        draw()

        pygame.display.flip()


# running loop


running = True
game = QbertGame()
initialize_window()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game.play_step()
    
pygame.quit()
