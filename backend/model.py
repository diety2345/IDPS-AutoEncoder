import mindspore as ms
from mindspore import nn

class AutoEncoder(nn.Cell):
    def __init__(self, input_dim=39):
        super().__init__()
        self.encoder = nn.SequentialCell([
            nn.Dense(input_dim, 128), nn.ReLU(),
            nn.Dense(128, 64), nn.ReLU(),
            nn.Dense(64,32), nn.ReLU(),
            nn.Dense(32, 16)
        ])
        self.decoder = nn.SequentialCell([
            nn.Dense(16, 32), nn.ReLU(),
            nn.Dense(32, 64), nn.ReLU(),
            nn.Dense(64, 128), nn.ReLU(),
            nn.Dense(128, input_dim)
        ])

    def construct (self, X):
        z = self.encoder(X)
        return self.decoder(z)    
      
