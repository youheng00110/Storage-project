<<<<<<< HEAD
import numpy as np
import matplotlib.pyplot as plt
# 步骤1：创建x值的数组
x = np.linspace(-10, 10, 1000)  # 从-10到10生成1000个点

# 步骤2：定义函数解析式
def f(x):
    return x**2 + 2*x + 1  # 示例：二次函数 y = x² + 2x + 1

# 步骤3：计算对应的y值
y = f(x)

# 步骤4：绘制图形
plt.figure(figsize=(8, 6))  # 设置图形大小
plt.plot(x, y, label='y = x² + 2x + 1')  # 绘制曲线
plt.xlabel('x')  # x轴标签
plt.ylabel('y')  # y轴标签
plt.title('二次函数图像')  # 标题
plt.grid(True)  # 显示网格
plt.legend()  # 显示图例
plt.show()  # 显示图形
=======
import numpy as np
import matplotlib.pyplot as plt
# 步骤1：创建x值的数组
x = np.linspace(-10, 10, 1000)  # 从-10到10生成1000个点

# 步骤2：定义函数解析式
def f(x):
    return x**2 + 2*x + 1  # 示例：二次函数 y = x² + 2x + 1

# 步骤3：计算对应的y值
y = f(x)

# 步骤4：绘制图形
plt.figure(figsize=(8, 6))  # 设置图形大小
plt.plot(x, y, label='y = x² + 2x + 1')  # 绘制曲线
plt.xlabel('x')  # x轴标签
plt.ylabel('y')  # y轴标签
plt.title('二次函数图像')  # 标题
plt.grid(True)  # 显示网格
plt.legend()  # 显示图例
plt.show()  # 显示图形
>>>>>>> b6f6c6d4bd78d0c45678438642b709b0eba48ced
