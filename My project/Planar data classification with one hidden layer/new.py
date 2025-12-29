# 导入依赖包
import numpy as np
import matplotlib.pyplot as plt
from testCases_v2 import *
import sklearn
import sklearn.datasets
import sklearn.linear_model
from planar_utils import plot_decision_boundary, sigmoid, load_planar_dataset, load_extra_datasets

# %matplotlib inline
np.random.seed(1) # 设置随机种子以保证结果可复现

# 2 - 数据集 ##
# 下面的代码会把一个“两类花朵”数据集加载到变量 X 和 Y 中。
X, Y = load_planar_dataset()

# 使用 matplotlib 可视化数据。数据看起来像一朵“花”，部分为红色（标签 y=0），部分为蓝色（y=1）。
# 你的目标是构建一个能拟合这些数据的模型。
# 可视化数据：
plt.scatter(X[0, :], X[1, :], c=Y, s=40, cmap=plt.cm.Spectral);

# 你现在有：
#     - 一个 numpy 数组（矩阵）X，包含特征 (x1, x2)
#     - 一个 numpy 数组（向量）Y，包含标签（红:0，蓝:1）
# 先了解一下我们数据的形状。
# 练习：你有多少个训练样本？同时打印 X 和 Y 的形状。
### START CODE HERE ### (≈ 3 lines of code)
# 中文说明：在此处填写代码
shape_X = np.shape(X)
shape_Y = np.shape(Y)
m = shape_X[1]  # 训练集大小
### END CODE HERE ###
print ('The shape of X is: ' + str(shape_X))
print ('The shape of Y is: ' + str(shape_Y))
print ('I have m = %d training examples!' % (m))

# 3 - 简单的逻辑回归
# 训练逻辑回归分类器
clf = sklearn.linear_model.LogisticRegressionCV();
clf.fit(X.T, Y.T);

# 现在你可以绘制这些模型的决策边界了。运行下面的代码。
# 绘制逻辑回归的决策边界
plot_decision_boundary(lambda x: clf.predict(x), X, Y)
plt.title("Logistic Regression")

# 打印准确率
LR_predictions = clf.predict(X.T)
print ('Accuracy of logistic regression: %d ' % float((np.dot(Y,LR_predictions) + np.dot(1-Y,1-LR_predictions))/float(Y.size)*100) +
       '% ' + "(percentage of correctly labelled datapoints)")

# 4 - 神经网络模型
# GRADED FUNCTION: layer_sizes
def layer_sizes(X, Y):
    """
    说明：
    计算每一层的大小（输入层、隐藏层、输出层）

    参数：
    X -- 形状为 (输入特征数, 样本数量) 的输入数据集
    Y -- 形状为 (输出维度, 样本数量) 的标签

    返回：
    n_x -- 输入层大小
    n_h -- 隐藏层大小
    n_y -- 输出层大小
    """
    ### START CODE HERE ### (≈ 3 lines of code)
    # 中文说明：这里取输入/输出维度并固定隐藏层为 4
    n_x = X.shape[0] # 输入层大小
    n_h = 4    # 隐藏层大小（硬编码）
    n_y = Y.shape[0] # 输出层大小
    ### END CODE HERE ###
    return (n_x, n_h, n_y)

# 快速测试
X_assess, Y_assess = layer_sizes_test_case()
(n_x, n_h, n_y) = layer_sizes(X_assess, Y_assess)
print("The size of the input layer is: n_x = " + str(n_x))
print("The size of the hidden layer is: n_h = " + str(n_h))
print("The size of the output layer is: n_y = " + str(n_y))

# GRADED FUNCTION: initialize_parameters
def initialize_parameters(n_x, n_h, n_y):
    """
    说明：
    按给定的各层大小初始化参数

    参数：
    n_x -- 输入层大小
    n_h -- 隐藏层大小
    n_y -- 输出层大小
    
    返回：
    params -- 一个字典，包含参数：
              W1 -- 形状为 (n_h, n_x) 的权重矩阵
              b1 -- 形状为 (n_h, 1) 的偏置向量
              W2 -- 形状为 (n_y, n_h) 的权重矩阵
              b2 -- 形状为 (n_y, 1) 的偏置向量
    """
    
    np.random.seed(2) # 固定随机种子以保证即使随机初始化也能和参考输出一致
    
    ### START CODE HERE ### (≈ 4 lines of code)
    # 中文说明：小随机值初始化权重，偏置为 0
    W1 = np.random.randn(n_h, n_x) * 0.01
    b1 = np.zeros((n_h, 1))
    W2 = np.random.randn(n_y, n_h) * 0.01
    b2 = np.zeros((n_y, 1))
    ### END CODE HERE ###
    
    assert (W1.shape == (n_h, n_x))
    assert (b1.shape == (n_h, 1))
    assert (W2.shape == (n_y, n_h))
    assert (b2.shape == (n_y, 1))
    
    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2}
    
    return parameters

# 测试 initialize_parameters
n_x, n_h, n_y = initialize_parameters_test_case()
parameters = initialize_parameters(n_x, n_h, n_y)
print("W1 = " + str(parameters["W1"]))
print("b1 = " + str(parameters["b1"]))
print("W2 = " + str(parameters["W2"]))
print("b2 = " + str(parameters["b2"]))

# GRADED FUNCTION: forward_propagation
def forward_propagation(X, parameters):
    """
    说明：
    前向传播

    参数：
    X -- 形状为 (n_x, m) 的输入数据
    parameters -- 包含参数的字典（初始化函数的输出）
    
    返回：
    A2 -- 第二层激活的 sigmoid 输出
    cache -- 包含 "Z1"、"A1"、"Z2"、"A2" 的缓存字典
    """
    # 从参数字典中取出各参数
    ### START CODE HERE ### (≈ 4 lines of code)
    # 中文说明：按键名读取
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]
    ### END CODE HERE ###
    
    # 实现前向传播以计算 A2（类别概率）
    ### START CODE HERE ### (≈ 4 lines of code)
    # 中文说明：第一层使用 tanh，第二层使用 sigmoid
    Z1 = np.dot(W1, X) + b1
    A1 = np.tanh(Z1)
    Z2 = np.dot(W2, A1) + b2    
    A2 = sigmoid(Z2)
    ### END CODE HERE ###
    
    assert(A2.shape == (1, X.shape[1]))
    
    cache = {"Z1": Z1,
             "A1": A1,
             "Z2": Z2,
             "A2": A2}
    
    return A2, cache

# 测试 forward_propagation
X_assess, parameters = forward_propagation_test_case()
A2, cache = forward_propagation(X_assess, parameters)
# 备注：这里取均值只是为了确保你的输出与我们的参考结果一致
print(np.mean(cache['Z1']) ,np.mean(cache['A1']),np.mean(cache['Z2']),np.mean(cache['A2']))

# GRADED FUNCTION: compute_cost
def compute_cost(A2, Y, parameters):
    """
    说明：
    计算交叉熵损失（讲义中的等式 13）

    参数：
    A2 -- 第二层激活的 sigmoid 输出，形状 (1, 样本数)
    Y -- “真实”标签向量，形状 (1, 样本数)
    parameters -- 包含参数 W1, b1, W2, b2 的字典（未直接使用，仅作接口一致）
    
    返回：
    cost -- 交叉熵损失
    """
    
    m = Y.shape[1] # 样本数量

    # 计算交叉熵损失
    ### START CODE HERE ### (≈ 2 lines of code)
    # 中文说明：逐样本求和后取平均
    logprobs = -np.multiply(np.log(A2), Y) - np.multiply(np.log(1 - A2), (1 - Y))
    cost = np.sum(logprobs) / m
    ### END CODE HERE ###
    
    cost = np.squeeze(cost)     # 确保维度符合预期，例如把 [[17]] 变成 17 
    assert(isinstance(cost, float))
    
    return cost

# 测试 compute_cost
A2, Y_assess, parameters = compute_cost_test_case()
print("cost = " + str(compute_cost(A2, Y_assess, parameters)))

# GRADED FUNCTION: backward_propagation
def backward_propagation(parameters, cache, X, Y):
    """
    说明：
    按上面的推导实现反向传播

    参数：
    parameters -- 包含参数的字典
    cache -- 包含 "Z1"、"A1"、"Z2"、"A2" 的缓存字典
    X -- 输入数据，形状 (2, 样本数)
    Y -- “真实”标签向量，形状 (1, 样本数)
    
    返回：
    grads -- 包含各参数梯度的字典
    """
    m = X.shape[1]
    
    # 首先，从参数字典中取出 W1 和 W2
    ### START CODE HERE ### (≈ 2 lines of code)
    # 中文说明：在此处填写代码
    W1 = None
    W2 = None
    ### END CODE HERE ###
        
    # 同样从缓存中取出 A1 和 A2
    ### START CODE HERE ### (≈ 2 lines of code)
    # 中文说明：在此处填写代码
    A1 = None
    A2 = None
    ### END CODE HERE ###
    
    # 反向传播：计算 dW1、db1、dW2、db2
    ### START CODE HERE ### (≈ 6 lines of code, corresponding to 6 equations on slide above)
    # 中文说明：在此处填写代码
    dZ2 = None
    dW2 = None
    db2 = None
    dZ1 = None
    dW1 = None
    db1 = None
    ### END CODE HERE ###
    
    grads = {"dW1": dW1,
             "db1": db1,
             "dW2": dW2,
             "db2": db2}
    
    return grads

# 测试 backward_propagation
parameters, cache, X_assess, Y_assess = backward_propagation_test_case()
grads = backward_propagation(parameters, cache, X_assess, Y_assess)
print ("dW1 = "+ str(grads["dW1"]))
print ("db1 = "+ str(grads["db1"]))
print ("dW2 = "+ str(grads["dW2"]))
print ("db2 = "+ str(grads["db2"]))

# GRADED FUNCTION: update_parameters
def update_parameters(parameters, grads, learning_rate = 1.2):
    """
    说明：
    使用梯度下降更新参数（见上面的更新规则）

    参数：
    parameters -- 包含当前参数的字典
    grads -- 包含各梯度的字典
    learning_rate -- 学习率（默认 1.2）
    
    返回：
    parameters -- 更新后的参数字典
    """
    # 从参数字典中取出各参数
    ### START CODE HERE ### (≈ 4 lines of code)
    # 中文说明：在此处填写代码
    W1 = None
    b1 = None
    W2 = None
    b2 = None
    ### END CODE HERE ###
    
    # 从梯度字典中取出各梯度
    ### START CODE HERE ### (≈ 4 lines of code)
    # 中文说明：在此处填写代码
    dW1 = None
    db1 = None
    dW2 = None
    db2 = None
    ## END CODE HERE ###
    
    # 使用更新规则更新每个参数
    ### START CODE HERE ### (≈ 4 lines of code)
    # 中文说明：在此处填写代码
    W1 = None
    b1 = None
    W2 = None
    b2 = None
    ### END CODE HERE ###
    
    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2}
    
    return parameters

# 测试 update_parameters
parameters, grads = update_parameters_test_case()
parameters = update_parameters(parameters, grads)
print("W1 = " + str(parameters["W1"]))
print("b1 = " + str(parameters["b1"]))
print("W2 = " + str(parameters["W2"]))
print("b2 = " + str(parameters["b2"]))

# GRADED FUNCTION: nn_model
def nn_model(X, Y, n_h, num_iterations = 10000, print_cost=False):
    """
    参数：
    X -- 形状为 (2, 样本数) 的数据集
    Y -- 形状为 (1, 样本数) 的标签
    n_h -- 隐藏层单元数
    num_iterations -- 梯度下降的迭代次数
    print_cost -- 若为 True，每 1000 次迭代打印一次损失
    
    返回：
    parameters -- 模型学到的参数，可用于后续预测
    """
    
    np.random.seed(3)
    n_x = layer_sizes(X, Y)[0]
    n_y = layer_sizes(X, Y)[2]
    
    # 初始化参数，然后取回 W1, b1, W2, b2。输入："n_x, n_h, n_y"；输出："W1, b1, W2, b2, parameters"
    ### START CODE HERE ### (≈ 5 lines of code)
    # 中文说明：在此处填写代码
    parameters = None
    W1 = None
    b1 = None
    W2 = None
    b2 = None
    ### END CODE HERE ###
    
    # 迭代（梯度下降）
    for i in range(0, num_iterations):
        
        ### START CODE HERE ### (≈ 4 lines of code)
        # 前向传播。输入："X, parameters"；输出："A2, cache"
        A2, cache = None
        
        # 损失函数。输入："A2, Y, parameters"；输出："cost"
        cost = None

        # 反向传播。输入："parameters, cache, X, Y"；输出："grads"
        grads = None

        # 梯度下降参数更新。输入："parameters, grads"；输出："parameters"
        parameters = None
        ### END CODE HERE ###
        
        # 每 1000 次迭代打印一次损失
        if print_cost and i % 1000 == 0:
            print ("Cost after iteration %i: %f" %(i, cost))

    return parameters

# 测试 nn_model
X_assess, Y_assess = nn_model_test_case()
parameters = nn_model(X_assess, Y_assess, 4, num_iterations=10000, print_cost=True)
print("W1 = " + str(parameters["W1"]))
print("b1 = " + str(parameters["b1"]))
print("W2 = " + str(parameters["W2"]))
print("b2 = " + str(parameters["b2"]))

# 4.5 预测
# GRADED FUNCTION: predict
def predict(parameters, X):
    """
    使用训练好的参数，对 X 中的每个样本进行二分类预测

    参数：
    parameters -- 包含参数的字典
    X -- 输入数据，形状 (n_x, m)
    
    返回：
    predictions -- 模型的预测结果向量（红:0 / 蓝:1）
    """
    
    # 使用前向传播计算概率，并以 0.5 为阈值将其转化为 0/1
    ### START CODE HERE ### (≈ 2 lines of code)
    # 中文说明：在此处填写代码
    A2, cache = None
    predictions = None
    ### END CODE HERE ###
    
    return predictions

# 测试 predict
parameters, X_assess = predict_test_case()
predictions = predict(parameters, X_assess)
print("predictions mean = " + str(np.mean(predictions)))

# 现在可以在平面数据集上运行模型，看看它的效果。
# 使用包含 n_h 个隐藏单元的单隐藏层模型
parameters = nn_model(X, Y, n_h = 4, num_iterations = 10000, print_cost=True)

# 绘制决策边界
plot_decision_boundary(lambda x: predict(parameters, x.T), X, Y)
plt.title("Decision Boundary for hidden layer size " + str(4))

# 打印准确率
predictions = predict(parameters, X)
print ('Accuracy: %d' % float((np.dot(Y,predictions.T) + np.dot(1-Y,1-predictions.T))/float(Y.size)*100) + '%')

