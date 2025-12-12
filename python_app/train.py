import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split
import os
import model

# Configuration
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'czech-coins')
MODEL_SAVE_PATH = 'coin_model.pth'
BATCH_SIZE = 32
EPOCHS = 40
LEARNING_RATE = 0.001
IMG_SIZE = (64, 64)

def train():
    # 1. Check if data exists
    if not os.path.exists(DATA_DIR):
        print(f"Error: Data directory '{DATA_DIR}' not found.")
        return

    print(f"Loading data from {DATA_DIR}...")

    # 2. Data Transforms
    transform = transforms.Compose([
        transforms.Resize(IMG_SIZE),
        transforms.ToTensor(),
        # Normalize? Using standard ImageNet means or just 0-1 (ToTensor does 0-1)
        # For simplicity, keeping it 0-1 for now or we can compute mean/std.
        # Let's add simple augmentation for robustness
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
    ])

    # 3. Load Dataset
    full_dataset = datasets.ImageFolder(root=DATA_DIR, transform=transform)
    print(f"Classes found: {full_dataset.classes}")
    
    # Split Train/Val
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

    print(f"Training on {len(train_dataset)} images, Validating on {len(val_dataset)} images.")

    # 4. Initialize Model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    net = model.CoinCNN(num_classes=len(full_dataset.classes)).to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(net.parameters(), lr=LEARNING_RATE)

    # 5. Training Loop
    best_acc = 0.0
    
    for epoch in range(EPOCHS):
        net.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for i, (inputs, labels) in enumerate(train_loader):
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        train_acc = 100 * correct / total
        print(f"Epoch {epoch+1}/{EPOCHS}, Loss: {running_loss/len(train_loader):.4f}, Train Acc: {train_acc:.2f}%")

        # Validation
        net.eval()
        correct_val = 0
        total_val = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = net(inputs)
                _, predicted = torch.max(outputs.data, 1)
                total_val += labels.size(0)
                correct_val += (predicted == labels).sum().item()
        
        val_acc = 100 * correct_val / total_val
        print(f"Validation Acc: {val_acc:.2f}%")

        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(net.state_dict(), MODEL_SAVE_PATH)
            print("Model saved!")

    print("Training Finished.")
    print(f"Best Validation Accuracy: {best_acc:.2f}%")
    print(f"Model saved to {os.path.abspath(MODEL_SAVE_PATH)}")

if __name__ == "__main__":
    train()
