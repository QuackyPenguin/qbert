from draw import draw, move
from initialize_game import *
from valid_cube_number_and_row import valid_cube_number_and_row
import pygame
import numpy as np
import random
import copy
import variables

class QbertGameAI:
    def __init__(self) -> None:
        self.dont_reset = False
        initialize_game()
        self.reset()

    def reset(self):
        self.counter = 0
        self.moves=0
        variables.state = PLAYING
        variables.game_time = 0
        variables.enemies = []
        if not self.dont_reset:
            variables.level.init_next_level()
            variables.speed = 15
        variables.jump_direction_player = STANDING
        variables.player.jumpDirection = STANDING
        self.nextEnemyTime = variables.level.next_enemy_appearance()
        variables.round_completed = False
        variables.level_completed = False
        self.dont_reset = False

        variables.player.cubeNumber = random.randint(0,27)
        variables.player.rowNumber = variables.cubes[variables.player.cubeNumber].row
        variables.player.x = variables.cubes[variables.player.cubeNumber].x
        variables.player.y = variables.cubes[variables.player.cubeNumber].y
        

    def play_step(self, action, n_games):
    
        if n_games%100==0:
            variables.speed = 15
        else:
            variables.speed = 1

        self.moves +=12
        
        reward = -variables.score
        game_over = False

        enemy_reward = 0

        if np.array_equal(action, [1, 0, 0, 0, 0]):
            variables.jump_direction_player = UP_LEFT
        elif np.array_equal(action, [0, 1, 0, 0, 0]):
            variables.jump_direction_player = DOWN_RIGHT
        elif np.array_equal(action, [0, 0, 1, 0, 0]):
            variables.jump_direction_player = UP_RIGHT
        elif np.array_equal(action, [0, 0, 0, 1, 0]):
            variables.jump_direction_player = DOWN_LEFT
        else:
            self.moves -= 10

        while True:
            if n_games%100==0:
                pygame.time.delay(variables.speed)
            variables.game_time += 1
            if variables.round_completed:
                self.reset()
                break

            if self.nextEnemyTime == variables.game_time:
                enemy = variables.level.generate_enemy()
                if enemy is not None:
                    variables.enemies.append(enemy)
                self.nextEnemyTime = variables.level.next_enemy_appearance()

            if not variables.freeze:
                for enemy in variables.enemies:
                    if enemy.detect_collision(variables.player):
                        variables.player.lives -= 1
                        reward -= 1000
                        self.dont_reset = True
                        self.reset()
                        break
            else:
                self.nextEnemyTime = -1
                variables.freeze_timer += 1
                if variables.freeze_timer >= 120:
                    variables.freeze = False
                    variables.freeze_timer = 0
                    self.nextEnemyTime = variables.level.next_enemy_appearance()

            if not valid_cube_number_and_row(variables.player.cubeNumber, variables.player.rowNumber):
                reward -= 1000
                variables.player.lives -= 1
                variables.player.cubeNumber = 0
                variables.player.rowNumber = 1
                variables.player.x = variables.cubes[variables.player.cubeNumber].x
                variables.player.y = variables.cubes[variables.player.cubeNumber].y
                self.dont_reset = True
                self.reset()
                
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
                game_over = True
                
            for enemy in variables.enemies:
                if enemy.destroy:
                    variables.enemies.remove(enemy)
                    enemy_reward += 50
            if n_games%100==0:
                draw()   
                pygame.display.flip()
            else:
                move()

            if variables.jump_direction_player == STANDING:
                variables.player.jumpCount = 0
                break
        
        reward += variables.score

        if reward>0:
            self.moves = 0
            for cube in variables.cubes:
                if cube.color == variables.level.colors[len(variables.level.colors)-1]:
                    reward += 20
                if cube.color == variables.level.colors[0]:
                    reward -= 10
                if len(variables.cubes) == 2 and cube.color == variables.level.colors[1]:
                    reward += 10
                
        else:
            # reward -= min(500, self.moves/max(len(variables.enemies), 1))
            
            for cube in variables.cubes:
                if cube.color != variables.level.colors[len(variables.level.colors)-1]:
                    reward -= 10
                if len(variables.cubes) == 2 and cube.color == variables.level.colors[1]:
                    reward += 10
        
        reward += enemy_reward

        return reward, game_over, variables.score
    
    def simulate_step(self, action):
        score = variables.score
        jump_direction_player = variables.jump_direction_player
        game_time = variables.game_time
        counter = self.counter
        nextEnemyTime = self.nextEnemyTime
        enemies = copy.deepcopy(variables.enemies)
        level = copy.deepcopy(variables.level)
        player = copy.deepcopy(variables.player)
        cubes = copy.deepcopy(variables.cubes)
        discs = copy.deepcopy(variables.discs)
        freeze = variables.freeze
        freeze_timer = variables.freeze_timer
        round_completed = variables.round_completed
        level_completed = variables.level_completed

        reward = -variables.score
        game_over = False
        variables.jump_direction_player = action

        while True:
            variables.game_time += 1
            if variables.round_completed:
                self.reset()

            if self.nextEnemyTime == variables.game_time:
                enemy = variables.level.generate_enemy()
                if enemy is not None:
                    variables.enemies.append(enemy)
                self.nextEnemyTime = variables.level.next_enemy_appearance()

            if not variables.freeze:
                for enemy in variables.enemies:
                    if enemy.detect_collision(variables.player):
                        variables.player.lives -= 1
                        reward -= 1000
                        self.dont_reset = True
                        self.reset()
            else:
                self.nextEnemyTime = -1
                variables.freeze_timer += 1
                if variables.freeze_timer * variables.speed >= 1500:
                    variables.freeze = False
                    variables.freeze_timer = 0
                    self.nextEnemyTime = variables.level.next_enemy_appearance()

            if not valid_cube_number_and_row(variables.player.cubeNumber, variables.player.rowNumber):
                reward -= 1000
                variables.player.lives -= 1
                variables.player.cubeNumber = 0
                variables.player.rowNumber = 1
                variables.player.x = variables.cubes[variables.player.cubeNumber].x
                variables.player.y = variables.cubes[variables.player.cubeNumber].y
                self.dont_reset = True
                self.reset()
                
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
                game_over = True
                self.reset()
                
            for enemy in variables.enemies:
                if enemy.destroy:
                    variables.enemies.remove(enemy) 

            move()

            if variables.jump_direction_player == STANDING:
                variables.player.jumpCount = 0
                break
        
        reward += variables.score

        if reward>0:
            for cube in variables.cubes:
                if cube.color == variables.level.colors[len(variables.level.colors)-1]:
                    reward += 20
                if cube.color == variables.level.colors[0]:
                    reward -= 10
                if len(variables.cubes) == 2 and cube.color == variables.level.colors[1]:
                    reward += 10
        else:
            reward -= min(500, self.moves/max(len(variables.enemies), 1))
            
            for cube in variables.cubes:
                if cube.color == variables.level.colors[0]:
                    reward -= 10
                if len(variables.cubes) == 2 and cube.color == variables.level.colors[1]:
                    reward += 10
        
        variables.score = score
        variables.jump_direction_player = jump_direction_player
        variables.game_time = game_time
        self.counter = counter
        self.nextEnemyTime = nextEnemyTime
        variables.enemies = enemies
        variables.level = level
        variables.player = player
        variables.cubes = cubes
        variables.discs = discs
        variables.freeze = freeze
        variables.freeze_timer = freeze_timer
        variables.round_completed = round_completed
        variables.level_completed = level_completed

        return reward