from initialize_game import initialize_window
from qbertai import QbertGameAI
from dqnagent import DQNAgent
from doubledqnagent import DoubleDQNAgent
from duelingdqnagent import DuelingDQNAgent
from plotter import plot
import variables
import numpy as np
        
def train():
    initialize_window()

    scores_array = []
    eps_history = []
    real_scores = []
    plot_real_scores = [0]
    max_score = 0
    game = QbertGameAI()
    agent = DuelingDQNAgent(game=game, input_dims=(2,8,8), n_actions=5, lr=0.00025/4, mem_size=1_000_000, batch_size=256, replace=32_000, eps_dec=1e-6, gamma=0.99, eps_min=0.05)
    benchmark = 1_000_000
    upper_bound = 50_025_000
    evaluate = False
    while agent.total_moves < upper_bound:
        if agent.total_moves > benchmark:
            if evaluate:
                plot_real_scores.append(np.mean(real_scores))
                real_scores = []
                benchmark = agent.total_moves + 1_000_000
                evaluate = False
            else:
                benchmark = agent.total_moves + 150_000
                upper_bound += 150_000
                evaluate = True
        game_over = False
        state_old = agent.get_state()
        steps = 0
        
        while not game_over:
            action = agent.get_action(state_old, evaluate)

            reward, game_over, score, life_lost = game.play_step(action, agent.n_games)
            state_new = agent.get_state()
            
            if not evaluate:
                agent.remember(state_old, action, reward, state_new, life_lost)
                if agent.total_moves % 8 == 0:
                    agent.train_long_memory()
            steps += 1
            state_old = state_new
            
        variables.score = 0
        
        scores_array.append(score)
        eps_history.append(1-agent.epsilon[0])
        avg_score = np.mean(scores_array[-100:])
        
        print(f'Game {agent.n_games} | Score: {score} | Record: {max_score}' +
            f'  | Steps: {steps} | Avg score: {avg_score:.2f}')
        
        if evaluate:
            with open('logs/duelingnon_random.txt', 'a') as f:
                f.write(f'Game {agent.n_games} | Score {score} | Record: {max_score} | Steps: {steps}\n')
                f.write(f'Frames: {agent.total_moves}\n')
            real_scores.append(score)

        agent.n_games += 1

        if score > max_score:
            max_score = score
            agent.save_models()
            
        
        if agent.n_games % 5_000 == 0:
            plot(scores_array, eps_history, 'logs/duelingplot', plot_real_scores)
    
    if len(real_scores) > 0:
        plot_real_scores.append(np.mean(real_scores))
    plot(scores_array, eps_history, 'logs/duelingplot', plot_real_scores)
    agent.save_models()
    np.save('logs/duelingscores.npy', np.array(scores_array))
    np.save('logs/duelingeps.npy', np.array(eps_history))
    np.save('logs/duelingrealscores.npy', np.array(plot_real_scores))

if __name__ == '__main__':
    train()