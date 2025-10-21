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
        print(f"✓ GPU 设备: {torch.cuda.get_device_name(0)}")
    print("所有库导入成功！\n")
except Exception as e:
    print(f"✗ 库导入失败: {e}")
    sys.exit(1)

# 设定对图片的归一化处理方式，并且下载数据集
transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
     ])

batch_size = 64 # 设置批处理大小

trainset = torchvision.datasets.CIFAR10(root='./dataset', train=True,
                                        download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                          shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR10(root='./dataset', train=False,
                                       download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                         shuffle=False, num_workers=2)
# 观察一下数据集的内容
classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck') # 类别名称

# 导入框架
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        # nn.Module子类的函数必须在构造函数中执行父类的构造函数
        super(Net, self).__init__()

        # 卷积层 '3'表示输入图片为单通道, '6'表示输出通道数，'5'表示卷积核为5*5
        self.conv1 = nn.Conv2d(3, 6, 5) 
        # 卷积层
        self.conv2 = nn.Conv2d(6, 16, 5) 
        # 仿射层/全连接层，y = Wx + b
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.dropout = nn.Dropout(p=0.5)  # Dropout 用于降低过拟合
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)


#########################
#
#  TASK2:添加了dropout层
#
#########################
    def forward(self, x): 
        # 卷积 -> 激活 -> 池化 (relu激活函数不改变输入的形状)
        # [batch size, 3, 32, 32] -- conv1 --> [batch size, 6, 28, 28] -- maxpool --> [batch size, 6, 14, 14]
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        # [batch size, 6, 14, 14] -- conv2 --> [batch size, 16, 10, 10] --> maxpool --> [batch size, 16, 5, 5]
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        # 把 16 * 5 * 5 的特征图展平，变为 [batch size, 16 * 5 * 5]，以送入全连接层
        x = x.view(x.size()[0], -1) 
        # [batch size, 16 * 5 * 5] -- fc1 --> [batch size, 120]
        x = F.relu(self.fc1(x))
        x = self.dropout(x)  # 训练时随机屏蔽一部分神经元
        # [batch size, 120] -- fc2 --> [batch size, 84]
        x = F.relu(self.fc2(x))
        # [batch size, 84] -- fc3 --> [batch size, 10]
        x = self.fc3(x)        
        return x

net = Net()
print(net)


##########################
#                        #
#   TASK2:正则化已启用    #
#                        #
##########################
# 设定损失函数和优化器
from torch import optim
criterion = nn.CrossEntropyLoss() # 交叉熵损失函数
optimizer = optim.SGD(
    net.parameters(),
    lr=0.009,
    momentum=0.9,
    weight_decay=1e-4  # L2 权重衰减（正则化项）- 已启用
) # 使用SGD（随机梯度下降）优化
num_epochs = 15 # 训练 15个 epoch


# 训练函数
def train(trainloader, net, num_epochs, criterion, optimizer, save_path=None):
    loss_history = []
    if save_path:
        os.makedirs(save_path, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net.to(device)  # 模型移到GPU

    for epoch in range(num_epochs):
        net.train()  # 设置为训练模式，启用 Dropout
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
            if i % 200 == 199:
                print('epoch %d: batch %5d loss: %.3f'
                      % (epoch + 1, i + 1, running_loss / 200))
                running_loss = 0.0

        if save_path:
            torch.save(net.state_dict(), f"{save_path}/epoch_{epoch + 1}_model.pth")

    print('Finished Training')
    return loss_history

# 定义 draw 函数（保持原样）
def draw(values):
    plt.plot(values)
    plt.xlabel("Iteration")
    plt.ylabel("Loss")
    plt.title("Training Loss Curve")
    plt.grid(True)
    plt.show()

# 测试函数
def predict(testloader, net):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net.to(device)
    net.eval()  # 切换到评估模式，关闭 Dropout
    
    correct = 0
    total = 0
    with torch.no_grad():
        for data in testloader:
            images, labels = data
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

# ========== 主程序入口 ==========
if __name__ == "__main__":
    net = Net()
    print(net)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(
        net.parameters(), 
        lr=0.011,
        momentum=0.9, 
        weight_decay=1e-4
    )
    num_epochs = 15
    save_path = "./checkpoints_with_regularization"

    losses = train(trainloader, net, num_epochs, criterion, optimizer, save_path)
    smoothed = [sum(losses[i:i+250])/250 for i in range(0, len(losses)-250, 250)]
    draw(smoothed)
    
    predict(testloader, net)