import torch.nn as nn


class Model(nn.Module):
    def __init__(self, vocab_size, N_HIDDEN):
        super(Model, self).__init__()

        self.linear1 = nn.Linear(vocab_size, N_HIDDEN)
        self.relu1 = nn.ReLU()

        self.linear3 = nn.Linear(N_HIDDEN, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.linear1(x)
        x = self.relu1(x)
        x = self.linear3(x)
        x = self.sigmoid(x)
        return x