
import numpy as np

# 权重矩阵 W：4×3
W = np.array([
    [0.2, 0.5, -0.3],
    [-0.4, 0.1, 0.6],
    [0.7, -0.2, 0.3],
    [0.5, 0.8, -0.1]
])

# 偏置向量 b：4×1
b = np.array([[0.1], [0.2], [0.3], [0.4]])

# 输入样本矩阵 X：3×5，每列是一个样本
X = np.array([
    [1.0, 0.5, 2.0, 1.5, -1.0],
    [0.2, -0.3, 0.8, 1.0, 0.0],
    [0.5, 1.0, -0.5, 0.0, 2.0]
])

# （1）循环版本：逐个样本计算
Z_loop = np.zeros((4, 5))
for i in range(X.shape[1]):
    x_i = X[:, [i]]   # 第 i 个样本 (3×1)
    Z_loop[:, [i]] = np.dot(W, x_i) + b


Z_vec=np.dot(W,X)
print(Z_loop)
print(Z_vec)
print(np.allclose(Z_loop, Z_vec))  # True
