# 环境检查：PyTorch、设备、Python 版本
import sys, torch
print("Python:", sys.version.splitlines()[0])
print("torch:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())

#导入库：torchvision、matplotlib、random
import torch
import torchvision
import torchvision.transforms as transforms
from torchvision.transforms import ToPILImage
show = ToPILImage()
import matplotlib.pyplot as plt
import random
import os

# ========== 验证库导入成功 ==========
print("\n========== 库导入检验 ==========")
try:
    print(f"✓ torch 版本: {torch.__version__}")
    print(f"✓ torchvision 版本: {torchvision.__version__}")
    print(f"✓ matplotlib 导入成功")
    print(f"✓ random 导入成功")
    print(f"✓ os 导入成功")
    print(f"✓ CUDA 可用: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        try:
            print(f"✓ GPU 设备: {torch.cuda.get_device_name(0)}")
        except Exception:
            pass
    print("所有库导入成功！\n")
except Exception as e:
    print(f"✗ 库导入失败: {e}")
    sys.exit(1)

# ================= 数据集与变换 =================
# 注意：AlexNet 期望更大的输入尺寸（通常 224x224），为最小改动这里对 CIFAR-10 图像做 Resize
transform = transforms.Compose([
    transforms.Resize(224),               # AlexNet 输入要求较大图像，最小修改：resize 到 224
    transforms.ToTensor(),
    # 保留你原有的归一化风格；如使用 pretrained=True 建议换成 ImageNet 的均值/方差
    transforms.Normalize((0.5,0.5,0.5), (0.5,0.5,0.5))
])

batch_size = 64

trainset = torchvision.datasets.CIFAR10(root='./dataset', train=True,
                                        download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                          shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR10(root='./dataset', train=False,
                                       download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                         shuffle=False, num_workers=2)

classes = ('plane','car','bird','cat','deer','dog','frog','horse','ship','truck')

# ================= 网络结构：用 AlexNet（仅在这里替换） =================
# 我做的“最小修改”：使用 torchvision.models.alexnet，并把最后的分类输出改为 10 类
import torch.nn as nn
from torchvision import models

def make_alexnet(num_classes=10, pretrained=False):
    model = models.alexnet(pretrained=pretrained)
    # 最后一层改为 num_classes
    model.classifier[6] = nn.Linear(4096, num_classes)
    return model

# 创建模型（如果你想用预训练权重，把 pretrained=False 改为 True，并把Normalize替换为 ImageNet 的均值/方差）
net = make_alexnet(num_classes=10, pretrained=False)
print(net)

# ========== 损失和优化器（保留原来的超参风格） ==========
from torch import optim
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.011, momentum=0.9, weight_decay=1e-4)
num_epochs = 10 # 训练 10个 epoch

# 训练函数
def train(trainloader, net, num_epochs, criterion, optimizer, save_path=None):
    loss_history = []
    if save_path:
        os.makedirs(save_path, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net.to(device)  # 模型移到GPU

    for epoch in range(num_epochs):
        net.train()  # 切换到训练模式
        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            inputs, labels = data
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            loss_history.append(loss.item())
            running_loss += loss.item()
            # 每 200 个 mini-batches 打印一次 loss（保持你原有的打印习惯）
            if i % 200 == 199:
                print('epoch %d: batch %5d loss: %.3f'
                      % (epoch + 1, i + 1, running_loss / 200))
                running_loss = 0.0

        # 每个 epoch 保存一次模型（如你之前所写）
        if save_path:
            torch.save(net.state_dict(), f"{save_path}/epoch_{epoch + 1}_model.pth")

    print('Finished Training')
    return loss_history

# 简单画图函数（保持原注释与功能）
def draw(values):
    plt.plot(values)
    plt.xlabel("Iteration")
    plt.ylabel("Loss")
    plt.title("Training Loss Curve")
    plt.grid(True)
    plt.show()

# 评估函数（保留原有注释风格）
def predict(testloader, net):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net.to(device)
    net.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in testloader:
            images, labels = images.to(device), labels.to(device)
            outputs = net(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    accuracy = 100 * correct / total
    print('\n' + '='*50)
    print(f'测试集准确率: {accuracy:.2f}%')
    print('='*50 + '\n')
    return accuracy

# ========== 主程序入口（保留你原来的超参与保存目录） ==========
if __name__ == "__main__":
    # 如果你想从头开始或加载预训练权重，都可以在这里调整
    net = make_alexnet(num_classes=10, pretrained=False)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.011, momentum=0.9, weight_decay=1e-4)
    num_epochs = 10
    save_path = "./checkpoints_with_regularization"

    losses = train(trainloader, net, num_epochs, criterion, optimizer, save_path)

    # 如果 loss 很多，做简单滑动平均再画图（保留原来展示逻辑）
    if len(losses) >= 250:
        smoothed = [sum(losses[i:i+250])/250 for i in range(0, len(losses)-250, 250)]
        draw(smoothed)
    else:
        draw(losses)

    predict(testloader, net)
