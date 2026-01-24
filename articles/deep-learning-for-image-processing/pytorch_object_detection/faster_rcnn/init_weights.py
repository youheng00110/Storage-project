import torch
import os
from train_res50_fpn import create_model

def main():
    # 确保保存目录存在
    save_dir = "./save_weights"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 创建模型（类别数需要和您predict.py以及train.py中一致，这里默认使用了20+1）
    # 如果您的类别数不是20，请手动修改下面的 num_classes 参数
    # 例如：如果您有2个类，这里填3 (2+1)
    num_classes = 21 
    
    print(f"Creating model with {num_classes} classes...")
    model = create_model(num_classes=num_classes)
    
    # 构建保存字典
    save_files = {
        'model': model.state_dict(),
        'epoch': 0
    }
    
    # 保存为 resNetFpn-model-1.pth (模拟第2个epoch的结果)
    save_path = os.path.join(save_dir, "resNetFpn-model-1.pth")
    torch.save(save_files, save_path)
    print(f"Dummy weights saved to: {save_path}")

if __name__ == "__main__":
    main()
