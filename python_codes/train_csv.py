import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import cv2
import csv
import os

# ---------------- LOAD DATA ----------------
images = []
labels = []

with open("labels.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # skip header

    for row in reader:
        filename, label = row
        path = os.path.join("dataset", filename)

        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            continue

        img = img / 255.0

        images.append(img)
        labels.append(int(label))

X = np.array(images)
y = np.array(labels)

X = X.reshape(-1, 1, 32, 32)

X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y, dtype=torch.float32).view(-1, 1)

print("Dataset size:", X.shape)

# ---------------- MODEL ----------------
class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Conv2d(1, 4, 3)   # more filters
        self.relu = nn.ReLU()
        self.fc = nn.Linear(4*30*30, 1)

    def forward(self, x):
        x = self.conv(x)
        x = self.relu(x)
        x = x.view(-1, 4*30*30)
        x = self.fc(x)
        return x

model = CNN()

# ---------------- TRAINING ----------------
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(10):
    outputs = model(X)
    loss = criterion(outputs, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    print(f"Epoch {epoch+1}, Loss: {loss.item()}")

# ---------------- SAVE MODEL ----------------
torch.save(model.state_dict(), "model.pth")

print("Training Complete!")
torch.save(model.state_dict(), "model.pth")
print("Model saved!")
