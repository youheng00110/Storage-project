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

# 设定对图片的归一化处理方式，并且下载数据集
transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
     ])

batch_size = 4

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


# 测试导入库与提取
print("\n测试是否导入库")
while(True):
    random_test=random.randint(0,len(testset)-1) # 随机选一个测试集的样本
    (data, label) = trainset[random_test] 
    print(len(trainset))
    print(data.size()) 
    print(label) # label是整数
    print(classes[label])

    img = ((data + 1) / 2).permute(1, 2, 0)  # CHW -> HWC
    plt.imshow(img)
    plt.title(classes[label])
    plt.axis('off')
    plt.show()
    if input("是否继续测试？y/n:") != 'y':
        break