import torch
import torch.nn as nn
import torch.nn.functional as F

import torchvision.models as models

class CoinCNN(nn.Module):
    """
    A simple Convolutional Neural Network for coin classification.
    Input: 3x128x128 image (RGB)
    Output: Class probabilities (e.g., 1, 2, 5, 10, 20, 50 CZK)
    """
    def __init__(self, num_classes=6):
        super(CoinCNN, self).__init__()
        # 1. Convolutional Block
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2) 

        # 2. Convolutional Block
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)

        # 3. Convolutional Block
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        
        # 4. Convolutional Block (Added for extra capacity)
        self.conv4 = nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm2d(128)

        # Fully Connected Layers
        # Input image is 128x128.
        # After pool1 (2x2): 64x64
        # After pool2 (2x2): 32x32
        # After pool3 (2x2): 16x16
        # After pool4 (2x2): 8x8
        self.fc1 = nn.Linear(128 * 8 * 8, 512)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(512, num_classes)

    def forward(self, x):
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        x = self.pool(F.relu(self.bn3(self.conv3(x))))
        x = self.pool(F.relu(self.bn4(self.conv4(x))))
        
        # Flatten
        x = x.view(-1, 128 * 8 * 8)
        
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        
        return x

def load_model(model_path=None, num_classes=6):
    """
    Loads the model architecture and weights (if provided).
    """
    model = CoinCNN(num_classes=num_classes)
    if model_path:
        try:
            model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
            print(f"Model loaded from {model_path}")
        except FileNotFoundError:
            print(f"Model file {model_path} not found, using initialized weights.")
    model.eval()
    return model
