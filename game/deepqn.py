import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.optim.lr_scheduler import LambdaLR
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class QNet(nn.Module):
    def __init__(self, input_size, hidden_size1, hidden_size2, hidden_size3, hidden_size4, hidden_size5, output_size) -> None:
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size1).to(device)
        self.linear2 = nn.Linear(hidden_size1, hidden_size2).to(device)
        self.linear3 = nn.Linear(hidden_size2, hidden_size3).to(device)
        self.linear4 = nn.Linear(hidden_size3, hidden_size4).to(device)
        self.linear5 = nn.Linear(hidden_size4, hidden_size5).to(device)
        self.linear6 = nn.Linear(hidden_size5, output_size).to(device)

        self.to(device)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        x = F.relu(self.linear3(x))
        x = F.relu(self.linear4(x))
        x = F.relu(self.linear5(x))
        x = self.linear6(x)
        return x

    def save(self, file_name='deepqn.pth'):
        model_folder_path = '../model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, model, lr, gamma) -> None:
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.scheduler = LambdaLR(self.optimizer, lr_lambda=lambda epoch: self.lr + (0.005 - 0.0001) * epoch / 100_000)
        self.criterium = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, game_over, step=False):
        state = torch.tensor(state, dtype=torch.float, device=device)
        next_state = torch.tensor(next_state, dtype=torch.float, device=device)
        action = torch.tensor(action, dtype=torch.float, device=device)
        reward = torch.tensor(reward, dtype=torch.float, device=device)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            game_over = (game_over, )

        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(game_over)):
            Q_new = reward[idx].to(device)
            if not game_over[idx]:
                Q_new = (reward[idx] + self.gamma * \
                    torch.max(self.model(next_state[idx].unsqueeze(0))))

            target[idx][torch.argmax(action).item()] = Q_new

        self.optimizer.zero_grad()
        loss = self.criterium(target, pred)
        loss.backward()

        self.optimizer.step()

        if step:
            self.scheduler.step()
            self.gamma = min(0.99, self.gamma + 0.99 / 20_000)