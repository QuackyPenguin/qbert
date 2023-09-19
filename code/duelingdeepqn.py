import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.optim.lr_scheduler import LambdaLR
import os
import numpy as np

class DuelingDeepQNetwork(nn.Module):
    def __init__(self, input_dims, output_size, lr, filename) -> None:
        super(DuelingDeepQNetwork, self).__init__()
        
        model_folder_path = 'model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        self.filename = os.path.join(model_folder_path, filename)

        self.conv_layers = nn.Sequential(
            nn.Conv2d(input_dims[0], 8, kernel_size=3),
            nn.ReLU(),
            nn.Conv2d(8, 16, kernel_size=3),
            nn.ReLU(),
            nn.Conv2d(16, 32, kernel_size=4),
            nn.ReLU()
        )
        
        # Calculate the input size for the fully connected layer
        conv_out_size = self.calculate_conv_output_dims(input_dims)
        
        self.V = nn.Sequential(
            nn.Linear(conv_out_size, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )
        
        self.A = nn.Sequential(
            nn.Linear(conv_out_size, 128),
            nn.ReLU(),
            nn.Linear(128, output_size)
        )
        
        self.lr = lr
        self.optimizer = optim.Adam(self.parameters(), lr=lr, eps=1.5e-4)
        self.loss = nn.MSELoss() 
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.to(self.device)

    def calculate_conv_output_dims(self, input_dims):
        x = torch.rand(1, *input_dims)
        conv_out = self.conv_layers(x)
        conv_out_size = conv_out.view(1, -1).size(1)
        return conv_out_size
    
    def forward(self, state):
        conv = self.conv_layers(state)
        conv_state = conv.view(conv.size(0), -1)
        V = self.V(conv_state)
        A = self.A(conv_state)
        return V, A

    def save(self):
        torch.save(self.state_dict(), self.filename)

    def load(self):
        self.load_state_dict(torch.load(self.filename))
