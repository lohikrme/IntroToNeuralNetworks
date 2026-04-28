# Denoising_Autoencoder.py
# Denoising Autoencoders
# 
# Run on yolo_mps_v11

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import numpy as np

# Define the Autoencoder
class DenoisingAutoencoder(nn.Module):
    def __init__(self):
        super(DenoisingAutoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(28*28, 128),
            nn.ReLU(),
            nn.Linear(128, 32)
        )
        self.decoder = nn.Sequential(
            nn.Linear(32, 128),
            nn.ReLU(),
            nn.Linear(128, 28*28),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = x.view(-1, 28*28)
        z = self.encoder(x)
        out = self.decoder(z)
        return out

def add_noise(inputs, noise_factor=0.3):
    noisy = inputs + noise_factor * torch.randn_like(inputs)
    return torch.clip(noisy, 0., 1.)

transform = transforms.ToTensor()
train_data = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
train_loader = DataLoader(train_data, batch_size=128, shuffle=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = DenoisingAutoencoder().to(device)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(10):
    total_loss = 0
    for imgs, _ in train_loader:
        imgs = imgs.to(device)
        noisy_imgs = add_noise(imgs)
        outputs = model(noisy_imgs)
        loss = criterion(outputs, imgs.view(-1, 28*28))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss: {total_loss / len(train_loader):.4f}")

def show_denoising_reconstruction(model, n=10):
    model.eval()
    imgs, _ = next(iter(train_loader))
    imgs = imgs[:n].to(device)
    noisy_imgs = add_noise(imgs)
    with torch.no_grad():
        outputs = model(noisy_imgs)

    fig, axes = plt.subplots(3, n, figsize=(n, 3))
    for i in range(n):
        axes[0, i].imshow(imgs[i].cpu().squeeze(), cmap='gray')
        axes[1, i].imshow(noisy_imgs[i].cpu().squeeze(), cmap='gray')
        axes[2, i].imshow(outputs[i].cpu().view(28, 28), cmap='gray')
        for row in range(3):
            axes[row, i].axis('off')
    plt.suptitle("Top: Original | Middle: Noisy | Bottom: Reconstructed")
    plt.show()

show_denoising_reconstruction(model)



