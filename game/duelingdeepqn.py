import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.optim.lr_scheduler import LambdaLR
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class DuelingQNet(nn.Module):
    def __init__(self, input_size, hidden_size1, hidden_size2, hidden_size3, hidden_size4, hidden_size5, output_size) -> None:
        super().__init__()
        self.shared_layers = nn.Sequential(
            nn.Linear(input_size, hidden_size1).to(device),
            nn.ReLU(),
            nn.Linear(hidden_size1, hidden_size2).to(device),
            nn.ReLU(),
            nn.Linear(hidden_size2, hidden_size3).to(device),
            nn.ReLU()
        ).to(device)
        
        self.value_stream = nn.Sequential(
            nn.Linear(hidden_size3, hidden_size4).to(device),
            nn.ReLU(),
            nn.Linear(hidden_size4, 1).to(device)
        ).to(device)
        
        self.advantage_stream = nn.Sequential(
            nn.Linear(hidden_size3, hidden_size4).to(device),
            nn.ReLU(),
            nn.Linear(hidden_size4, output_size).to(device)
        ).to(device)
        
        self.to(device)

    def forward(self, x):
        shared_out = self.shared_layers(x)
        value = self.value_stream(shared_out)
        advantage = self.advantage_stream(shared_out)
        
        # Combine value and advantage to get Q-values
        q_values = value + (advantage - advantage.mean(dim=1, keepdim=True))
        
        return q_values

    def save(self, file_name='duelingdeepqn.pth'):
        model_folder_path = '../model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class DuelingQTrainer:
    def __init__(self, model, lr, gamma) -> None:
        self.lr = lr
        self.gamma = gamma
        self.model = model  # Move the model to GPU if available
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterium = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, game_over):
        state = torch.tensor(state, dtype=torch.float, device=device)
        next_state = torch.tensor(next_state, dtype=torch.float, device=device)
        action = torch.tensor(action, dtype=torch.float, device=device)
        reward = torch.tensor(reward, dtype=torch.float, device=device)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0).to(device)
            next_state = torch.unsqueeze(next_state, 0).to(device)
            action = torch.unsqueeze(action, 0).to(device)
            reward = torch.unsqueeze(reward, 0).to(device)
            game_over = (game_over, )

        pred = self.model(state)

        target = pred.clone().to(device)
        for idx in range(len(game_over)):
            Q_new = reward[idx].to(device)
            if not game_over[idx]:
                Q_new = (reward[idx] + self.gamma * \
                    torch.max(self.model(next_state[idx].unsqueeze(0)))).to(device)

            target[idx][torch.argmax(action).item()] = Q_new

        self.optimizer.zero_grad()
        loss = self.criterium(target, pred)
        loss.backward()

        self.optimizer.step()
