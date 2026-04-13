import torch
import numpy as np

# SAME MODEL AS TRAINING
import torch.nn as nn

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Conv2d(1, 4, 3)
        self.relu = nn.ReLU()
        self.fc = nn.Linear(4*30*30, 1)

    def forward(self, x):
        x = self.conv(x)
        x = self.relu(x)
        x = x.view(-1, 4*30*30)
        x = self.fc(x)
        return x

# Load model
model = CNN()
model.load_state_dict(torch.load("model.pth"))
model.eval()

# Extract weights
conv_w = model.conv.weight.data.numpy()
conv_b = model.conv.bias.data.numpy()

fc_w = model.fc.weight.data.numpy()
fc_b = model.fc.bias.data.numpy()

print("Conv shape:", conv_w.shape)
print("FC shape:", fc_w.shape)
def quantize(w):
    max_val = np.max(np.abs(w))
    scale = 127 / max_val
    return (w * scale).astype(int)

conv_w_q = quantize(conv_w)
fc_w_q = quantize(fc_w)

np.savetxt("conv_weights.txt", conv_w_q.flatten(), fmt='%d')
np.savetxt("fc_weights.txt", fc_w_q.flatten(), fmt='%d')

print("Weights saved!")
