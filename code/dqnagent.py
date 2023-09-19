from sklearn import logger
import torch
import random
import numpy as np
from characters.coily import Coily
from characters.green_ball import GreenBall
from characters.red_ball import RedBall
from characters.sam import Sam
from characters.slick import Slick
from characters.ugg import Ugg
from characters.wrongway import Wrongway
from qbertai import QbertGameAI
from constants import *
import variables
from deepqn import DeepQNetwork
from duelingdeepqn import DuelingDeepQNetwork
from replaybuffer import ReplayBuffer

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def color_to_number(color) -> int:
    if color == variables.level.colors[len(variables.level.colors)-1]:
        return 1
    elif color == variables.level.colors[len(variables.level.colors)-2]:
        return 0.5
    elif color == variables.level.colors[0]:
        return 0
    else:
        return -1


class DQNAgent:
    def __init__(self, game: QbertGameAI, input_dims, n_actions, batch_size = 32, epsilon = 1.0, gamma = 0.9, 
                 mem_size = 100_000, lr = 0.001, eps_min=0.001, eps_dec=1e-2, replace = 1000):
        self.n_games = 1
        self.epsilon = [epsilon, epsilon * 1 / 2, epsilon * 1 / 4, epsilon * 1 / 8, epsilon * 1 / 4, epsilon * 1 / 8, epsilon * 1 / 16, epsilon * 1 / 32, epsilon * 1 / 8]

        self.eps_end = eps_min
        self.eps_dec = eps_dec
        self.gamma = gamma
        self.batch_size = batch_size
        self.lr = lr
        self.memory = ReplayBuffer(mem_size, input_dims, n_actions)
        self.q_eval = DeepQNetwork(input_dims, n_actions, lr=self.lr, filename='q_eval')
        self.q_next = DeepQNetwork(input_dims, n_actions, lr=self.lr, filename='q_next')
        self.replace_target_cnt = replace
        self.learn_counter = 0
        self.game = game
        self.index = 0
        self.random = False
        self.action_space = [i for i in range(n_actions)]
        self.total_moves = 0

    def save_models(self):
        self.q_eval.save()
        self.q_next.save()

    def load_models(self):
        self.q_eval.load()
        self.q_next.load()
        
    def get_state(self):
        state = np.zeros((2, 8, 8), dtype=np.float32)
        cube_state = np.zeros((8, 8), dtype=np.float32)
        cube_state.fill(-1)
        
        if variables.level.level == 0:
            cube_state[7, 7] = min(4,variables.level.round) / 4
        else:
            cube_state[7, 7] = min(variables.level.level - 1, 4) / 4
            
        for i, cube in enumerate(variables.cubes):
            value = color_to_number(cube.color)
            offset = i - cube.row * (cube.row - 1) // 2
            row = cube.row - offset
            column = cube.row - row + 1
            cube_state[row, column] = value
        
        for i, disc in enumerate(variables.discs):
            value = -1 if disc.used else 2
            if disc.side == 1: 
                row, column = disc.row + 1, 0 
            else:
                row, column = 0, disc.row + 1
            cube_state[row, column] = value
        
        state[0] = cube_state
        
        character_state = np.zeros((8, 8), dtype=np.float32)
        
        if variables.freeze:
            character_state[0, 0] = (120 - variables.freeze_timer) / 120
        
        offset = variables.player.cubeNumber - variables.player.rowNumber * (variables.player.rowNumber - 1) // 2
        row = variables.player.rowNumber - offset
        column = variables.player.rowNumber - row + 1
        character_state[row, column] = 2
        
        for i, enemy in enumerate(variables.enemies):
            if enemy.destroy:
                continue
            
            offset = enemy.cubeNumber - enemy.rowNumber * (enemy.rowNumber - 1) // 2
            row = enemy.rowNumber - offset
            column = enemy.rowNumber - row + 1
            
            if isinstance(enemy, Coily) and enemy.version == 2:
                value = -1
                if row + 1 < 8 and enemy.jumpDirection == DOWN_LEFT:
                    character_state[row + 1, column] += value
                if column + 1 < 8 and enemy.jumpDirection == DOWN_RIGHT:  
                    character_state[row, column + 1] += value
                if row - 1 >= 0 and enemy.jumpDirection == UP_LEFT:   
                    character_state[row - 1, column] += value
                if column - 1 >= 0 and enemy.jumpDirection == UP_RIGHT:   
                    character_state[row, column - 1] += value
                character_state[row, column] += value
            elif isinstance(enemy, Ugg):
                value = -0.75
                if row + 1 < 8 and enemy.jumpDirection == LEFT:    
                    character_state[row + 1, column] += value
                if enemy.jumpDirection == RIGHT:
                    character_state[row, column] += value
                if column + 1 < 8:
                    character_state[row, column + 1] += value
            elif isinstance(enemy, Wrongway):
                value = -0.75
                if column + 1 < 8 and enemy.jumpDirection == RIGHT:    
                    character_state[row, column + 1] += value
                if enemy.jumpDirection == LEFT:
                    character_state[row, column] += value
                if row + 1 < 8:
                    character_state[row + 1, column] += value
            elif isinstance(enemy, Sam) or isinstance(enemy, Slick):
                value = 0.75
                character_state[row, column] += value
                if row + 1 < 8 and enemy.jumpDirection == DOWN_LEFT:
                    character_state[row + 1, column] += value
                if column + 1 < 8 and enemy.jumpDirection == DOWN_RIGHT:
                    character_state[row, column + 1] += value
            elif isinstance(enemy, GreenBall):
                value = 1
                character_state[row, column] += value
                if row + 1 < 8 and enemy.jumpDirection == DOWN_LEFT:
                    character_state[row + 1, column] += value
                if column + 1 < 8 and enemy.jumpDirection == DOWN_RIGHT:
                    character_state[row, column + 1] += value
            elif isinstance(enemy, RedBall) or isinstance(enemy, Coily):
                value = -0.75
                character_state[row, column] += value
                if row + 1 < 8 and enemy.jumpDirection == DOWN_LEFT:
                    character_state[row + 1, column] += value
                if column + 1 < 8 and enemy.jumpDirection == DOWN_RIGHT:    
                    character_state[row, column + 1] += value
        
        state[1] = character_state
        
        return state
    
    def replace_target_network(self):
        if self.learn_counter >= self.replace_target_cnt:
            self.q_next.load_state_dict(self.q_eval.state_dict())
            self.learn_counter -= self.replace_target_cnt

            # Print or log Q-values for each action
            
            # with open('logs/q_values.txt', 'a') as f:
            #     for i, q_val in enumerate(q_values[0]):
            #         f.write(str(self.n_games))
            #         f.write(' ')
            #         f.write(str(i))
            #         f.write(' ')
            #         f.write(str(q_val.item()))
            #         f.write('\n')
            #     f.write('--------------------------------------------------\n')
    
    def remember(self, state, action, reward, next_state, game_over):
        self.memory.store_transition(state, action, reward, next_state, game_over)

    def sample_memory(self):
        state, action, reward, new_state, done = \
                                self.memory.sample_buffer(self.batch_size)

        states = torch.tensor(state).to(self.q_eval.device)
        rewards = torch.tensor(reward).to(self.q_eval.device)
        dones = torch.tensor(done).to(self.q_eval.device)
        actions = torch.tensor(action).to(self.q_eval.device)
        states_ = torch.tensor(new_state).to(self.q_eval.device)

        return states, actions, rewards, states_, dones

    def train_long_memory(self):
        if self.total_moves < 200_000:
            return
        
        self.q_eval.optimizer.zero_grad()
        self.q_next.optimizer.zero_grad()

        states, actions, rewards, states_, game_overs = self.sample_memory()
        
        self.replace_target_network()
        
        indices = np.arange(self.batch_size)

        q_pred = self.q_eval.forward(states)[indices, actions]
        q_next = self.q_next.forward(states_).max(dim=1)[0]

        q_next[game_overs] = 0.0
        q_target = rewards + self.gamma*q_next
        
        loss = self.q_eval.loss(q_target, q_pred).to(self.q_eval.device)
        loss.backward()
        self.q_eval.optimizer.step()
        self.learn_counter += 1
        
    def get_action(self, state, evaluate=False):
        
        self.index = min((variables.level.level - 1) * 4 + variables.level.round - 1, 8)

        if np.random.random() < self.epsilon[self.index] and not evaluate:
            action = np.random.choice(self.action_space)
            self.random = True
        else:
            state_array = np.array(state, dtype=np.float32)  # Convert list to a NumPy array
            state_tensor = torch.tensor(state_array, dtype=torch.float, device=device)
            prediction = self.q_eval(state_tensor.unsqueeze(0))
            action = torch.argmax(prediction).item()
            self.random = False
        
        if self.total_moves >= 200_000 and not evaluate:
            self.epsilon[self.index] = self.epsilon[self.index] - \
                    self.eps_dec if self.epsilon[self.index] > self.eps_end else self.eps_end
        self.total_moves += 1

        return action
