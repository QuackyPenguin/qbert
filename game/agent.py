import torch
import random
import numpy as np
from qbertai import QbertGameAI
from collections import deque
from constants import *
import variables
from red_ball import RedBall
from coily import Coily
from ugg import Ugg
from wrongway import Wrongway
from green_ball import GreenBall
from sam import Sam
from slick import Slick
from deepqn import QNet, QTrainer
from duelingdeepqn import DuelingQNet, DuelingQTrainer
from plotter import plot
from initialize_game import initialize_window

MAX_MEMORY = 1_000_000
BATCH_SIZE = 1024
LR = 0.0001
GAMMA = 0.01

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def color_to_number(color) -> int:
    if color == COLOR_YELLOW or color == COLOR_DARK_BLUE or color == COLOR_MAROON or color == COLOR_LIME:
        return 3
    elif color == COLOR_BLUE or color == COLOR_GOLD or color == COLOR_SILVER or color == COLOR_LAVENDER or color == COLOR_RED or color == COLOR_PURPLE or color == COLOR_PINK or color == COLOR_SKY_BLUE:
        return 2
    elif color == COLOR_ORANGE or color == COLOR_CYAN or color == COLOR_GRAY or color == COLOR_BROWN:
        return 1
    else:
        return 0


def get_type(enemy):
    return_value = [0, 0, 0, 0, 0, 0]
    i = -1
    if isinstance(enemy, RedBall) or (isinstance(enemy, Coily) and enemy.version != 2):
        i = 0
    elif isinstance(enemy, Coily):
        i = 1
    elif isinstance(enemy, Ugg):
        i = 2
    elif isinstance(enemy, Wrongway):
        i = 3
    elif isinstance(enemy, GreenBall):
        i = 4
    elif isinstance(enemy, Sam) or isinstance(enemy, Slick):
        i = 5
    return_value[i] = 1
    return return_value


class Agent:
    def __init__(self, game: QbertGameAI, epsilon=1.0, eps_min=0.01, eps_dec=2e-5) -> None:
        self.n_games = 0
        self.epsilon = [epsilon] * 5
        for i in range(0, 5):
            self.epsilon.append(epsilon)
            self.epsilon.append(epsilon*1/2)
            self.epsilon.append(epsilon*1/4)
            self.epsilon.append(epsilon*1/8)
            epsilon = (epsilon*(8-i-1))/(8-i)

        self.eps_end = eps_min
        self.eps_dec = eps_dec
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = QNet(98, 1024, 512, 256, 128, 64, 5)
        self.trainer = QTrainer(self.model, LR, GAMMA)
        self.game = game
        self.index = 0

    def get_state(self, game):
        state = []

        if variables.level.level == 0:
            state.append(variables.level.round)
        else:
            state.append(min(variables.level.level - 1, 4))

        state.append((variables.player.x-176)/576)
        state.append((variables.player.y-144)/432)

        for cube in variables.cubes:
            color = cube.color
            state.append(color_to_number(color))

        help_list = []
        for i in range(0, 7):
            if i < len(variables.discs) and not variables.discs[i].used:
                help_list.append(variables.discs[i])
            else:
                help_list.append(None)

        random.shuffle(help_list)
        for x in help_list:
            if x is not None:
                offset = 1
                if x.side == 2:
                    offset = -1
                state.append(
                    (variables.cubes[x.cube + offset].x + CUBE_SIZE * offset * (-1)-176)/576)
                state.append(
                    (variables.cubes[x.cube + offset].y - CUBE_SIZE // 4-144)/432)
            else:
                state.append(0)
                state.append(0)

        help_list = []
        for i in range(0, 6):
            if i < len(variables.enemies):
                help_list.append(variables.enemies[i])
            else:
                help_list.append(None)

        random.shuffle(help_list)
        for x in help_list:
            if x is not None:
                state.append((x.x-176)/576)
                state.append((x.y-144)/432)
                state.extend(get_type(x))
            else:
                for _ in range(0, 8):
                    state.append(0)

        state.append(self.game.simulate_step(STANDING))
        state.append(self.game.simulate_step(UP_LEFT))
        state.append(self.game.simulate_step(UP_RIGHT))
        state.append(self.game.simulate_step(DOWN_LEFT))
        state.append(self.game.simulate_step(DOWN_RIGHT))

        # for i in range(5):
        #     state.append(0)

        return state

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        (states, actions, rewards, next_states, game_overs) = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards,
                                next_states, game_overs, True)

        i = 0
        while i <= self.index:
            self.epsilon[i] = self.epsilon[i] - \
                self.eps_dec if self.epsilon[i] > self.eps_end else self.eps_end
            i += 1

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        action = [0, 0, 0, 0, 0]

        self.index = min((variables.level.level)*4+(variables.level.round), 23)

        if np.random.random() < self.epsilon[self.index]:
            index = random.randint(0, 4)
            action[index] = 1
        else:
            state0 = torch.tensor(
                state, dtype=torch.float, device=device)
            state0 = state0.unsqueeze(0)  # for dueling
            prediction = self.model(state0)
            index = torch.argmax(prediction).item()
            action[index] = 1

        return action


def train():
    initialize_window()

    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    max_score = 0
    game = QbertGameAI()
    agent = Agent(game=game)

    while True:
        state_old = agent.get_state(game)
        action = agent.get_action(state_old)

        reward, game_over, score = game.play_step(action, agent.n_games)
        state_new = agent.get_state(game)

        agent.train_short_memory(
            state_old, action, reward, state_new, game_over)

        agent.remember(state_old, action, reward, state_new, game_over)

        if game_over:
            game = QbertGameAI()
            agent.n_games += 1
            agent.train_long_memory()

            if score > max_score:
                max_score = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', max_score)

            plot_scores.append(score)
            total_score += score
            if len(plot_mean_scores) >= 500:
                total_score -= plot_mean_scores[len(plot_mean_scores)-499]
            mean_score = total_score / min(agent.n_games, 500)
            plot_mean_scores.append(mean_score)

            if agent.n_games % 100 == 0:
                plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()
