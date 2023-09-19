from collections import deque
from copy import deepcopy
from sklearn import logger
from draw import draw, move
from initialize_game import *
from valid_cube_number_and_row import valid_cube_number_and_row
import pygame
from characters.coily import Coily
import variables

class QbertGameAI:
    def __init__(self) -> None:
        self.reset(True, 1)
        variables.speed = 15
        self.mark = 6000
        self.game_moves = 0

    def reset(self, game_over, games):
        self.moves = 0
        variables.game_time = 0
        variables.state = PLAYING
        variables.enemies = []
        if game_over:
            self.mark = 6000
            initialize_game()
            self.game_moves = 0
        if game_over or variables.round_completed:
            variables.level.init_next_level()
            variables.player.cubeNumber = 0
            variables.player.rowNumber = variables.cubes[variables.player.cubeNumber].row
            variables.player.x = variables.cubes[variables.player.cubeNumber].x
            variables.player.y = variables.cubes[variables.player.cubeNumber].y
        variables.jump_direction_player = STANDING
        variables.player.jumpDirection = STANDING
        self.nextEnemyTime = variables.level.next_enemy_appearance()
        variables.round_completed = False
        variables.level_completed = False
        draw()
        if (games+1) % 5000 == 0:
            variables.real_window.blit(variables.game_window, variables.game_window.get_rect())
            pygame.event.pump()
            pygame.display.flip()
        

    def play_step(self, action, games):
        self.game_moves += 1
        
        reward = -variables.score #- 1000
        game_over = False
        lost_life = False
        disc_used = False
        coily_destroyed = False
        
        cubes_copy = deepcopy(variables.cubes)
        
        counter = 0
        
        actions = self.get_possible_actions()

        if action == 0 and 0 in actions:
            variables.jump_direction_player = UP_LEFT
            self.moves = 31
        elif action == 1 and 1 in actions:
            variables.jump_direction_player = DOWN_RIGHT
            self.moves = 31
        elif action == 2 and 2 in actions:
            variables.jump_direction_player = UP_RIGHT
            self.moves = 31
        elif action == 3 and 3 in actions:
            variables.jump_direction_player = DOWN_LEFT
            self.moves = 31
        else:
            counter = 6
            self.moves += 1
        
        if self.moves == 30:
            variables.player.lives -= 1
            counter = 0
        
        if self.game_moves == 25_000:
            variables.player.lives = 0
        
        while True:
            counter = max(0, counter-1)
            if games % 5000 == 0:
                pygame.time.delay(variables.speed)
            variables.game_time += 1
            
            
            if variables.round_completed:
                round_end = True
                self.reset(False, games)
                break

            if self.nextEnemyTime == variables.game_time:
                enemy = variables.level.generate_enemy()
                if enemy is not None:
                    variables.enemies.append(enemy)
                self.nextEnemyTime = variables.level.next_enemy_appearance()

            if not variables.freeze:
                for enemy in variables.enemies:
                    if abs(enemy.rowNumber - variables.player.rowNumber) <= 1 and enemy.detect_collision(variables.player) :
                        variables.player.lives -= 1
                        lost_life = True
                        self.reset(False, games)
                        break
            else:
                self.nextEnemyTime = -1
                variables.freeze_timer += 1
                if variables.freeze_timer >= 120:
                    variables.freeze = False
                    variables.freeze_timer = 0
                    self.nextEnemyTime = variables.level.next_enemy_appearance()
                
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
                    disc_used = True
                    break

            if variables.player.lives <= 0:
                game_over = True
                self.reset(True, games)
            for enemy in variables.enemies:
                if enemy.destroy:
                    variables.enemies.remove(enemy)
                    if isinstance(enemy, Coily):
                        coily_destroyed = True
                    
            if games % 5000 == 0:
                draw()
                variables.real_window.blit(variables.game_window, variables.game_window.get_rect())
                pygame.event.pump()
                pygame.display.flip()
            else:
                move()

            if variables.jump_direction_player == STANDING and counter == 0:
                variables.player.jumpCount = 0
                break
        
        reward += variables.score
        
        if disc_used and not coily_destroyed:
            reward -= 6.25
            
        if variables.cubes[variables.player.cubeNumber].color in variables.level.colors and cubes_copy[variables.player.cubeNumber].color in variables.level.colors:
            if variables.level.colors.index(variables.cubes[variables.player.cubeNumber].color) < variables.level.colors.index(cubes_copy[variables.player.cubeNumber].color):
                reward -= 15
        
        if not game_over:
            if variables.score >= self.mark:
                variables.player.lives += 1
                self.mark += 12000
        
        return reward/25, game_over, variables.score, lost_life
    
    
    def get_possible_actions(self):
        
        actions = []
        if valid_cube_number_and_row(variables.player.cubeNumber - variables.player.rowNumber, variables.player.rowNumber - 1):
            actions.append(0)
        if valid_cube_number_and_row(variables.player.cubeNumber + variables.player.rowNumber + 1, variables.player.rowNumber + 1):
            actions.append(1)
        if valid_cube_number_and_row(variables.player.cubeNumber - variables.player.rowNumber + 1, variables.player.rowNumber - 1):
            actions.append(2)
        if valid_cube_number_and_row(variables.player.cubeNumber + variables.player.rowNumber, variables.player.rowNumber + 1):
            actions.append(3)
        actions.append(4)
        return actions