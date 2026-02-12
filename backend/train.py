import numpy as np
import mindspore as ms
from mindspore import nn
from mindspore import Tensor
from model import AutoEncoder
from mindspore.train.serialization import save_checkpoint, load_checkpoint, load_param_into_net

import sys
import os
sys.path.insert(0,('/home/rouge/AI/IDPS'))
#print("Current working directory:", os.getcwd())
#print("sys.path contents:")
#for i, path in enumerate(sys.path):
    #print(f"  {i}: {path}")
#print("Looking for datasets folder...")
#print("datasets/ exists?", os.path.exists('/home/rouge/AI/IDPS/datasets'))
#print("datasets/dataprocessor.py exists?", os.path.exists('/home/rouge/AI/IDPS/datasets/dataprocessor.py'))

from datasets.dataprocessor import load_nslkdd


ms.context.set_context(mode=ms.context.PYNATIVE_MODE)
ms.set_device("CPU")

data = load_nslkdd()
data = Tensor(data)
print(f"Training on NSL-KDD: {data.shape}")

model = AutoEncoder(input_dim=data.shape[1])
loss_fn = nn.MSELoss()
optimizer = nn.Adam(model.trainable_params(),learning_rate= 0.001)

def forward(X):
    recon = model(X)
    return loss_fn(recon, X)


grad_fn = ms.value_and_grad(forward, None, optimizer.parameters)

print("Training AutoEncoder")
for epoch in range(50):
    loss, grads = grad_fn(data)
    optimizer(grads)
    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch+1}, Loss: {loss}")

save_checkpoint(model, "autoencoder_nslkdd.ckpt")
print("Model trained and saved")