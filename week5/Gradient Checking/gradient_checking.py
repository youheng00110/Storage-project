import numpy as np

def sigmoid(x):
    """计算 sigmoid 激活函数"""
    return 1 / (1 + np.exp(-x))

def relu(x):
    """计算 ReLU 激活函数"""
    return np.maximum(0, x)

def forward_propagation(x, theta):
    """
    实现简单的线性前向传播 J(theta) = theta * x
    
    参数:
    x -- 实数输入
    theta -- 参数,实数
    
    返回:
    J -- 函数值
    """
    J = theta * x
    return J

def backward_propagation(x, theta):
    """
    计算 J 关于 theta 的导数
    
    参数:
    x -- 实数输入
    theta -- 参数,实数
    
    返回:
    dtheta -- 关于 theta 的梯度
    """
    dtheta = x
    return dtheta

def gradient_check(x, theta, epsilon=1e-7):
    """
    实现一维梯度检查
    
    参数:
    x -- 实数输入
    theta -- 参数,实数
    epsilon -- 计算近似梯度的微小偏移量
    
    返回:
    difference -- 近似梯度与反向传播梯度之间的差异
    """
    # 计算近似梯度
    thetaplus = theta + epsilon
    thetaminus = theta - epsilon
    J_plus = forward_propagation(x, thetaplus)
    J_minus = forward_propagation(x, thetaminus)
    gradapprox = (J_plus - J_minus) / (2 * epsilon)
    
    # 使用反向传播计算梯度
    grad = backward_propagation(x, theta)
    
    # 计算相对差异
    numerator = np.linalg.norm(grad - gradapprox)
    denominator = np.linalg.norm(grad) + np.linalg.norm(gradapprox)
    difference = numerator / denominator
    
    if difference < 1e-7:
        print("梯度计算正确!")
    else:
        print("梯度计算错误!")
    
    return difference

def dictionary_to_vector(parameters):
    """将参数字典转换为向量"""
    keys = []
    count = 0
    for key in ["W1", "b1", "W2", "b2", "W3", "b3"]:
        new_vector = np.reshape(parameters[key], (-1, 1))
        keys.append(key)
        
        if count == 0:
            theta = new_vector
        else:
            theta = np.concatenate((theta, new_vector), axis=0)
        count += 1
    
    return theta, keys

def vector_to_dictionary(theta, keys=["W1", "b1", "W2", "b2", "W3", "b3"]):
    """将向量转换回参数字典"""
    parameters = {}
    # 这里需要根据实际的参数形状进行还原
    return parameters

def gradients_to_vector(gradients):
    """将梯度字典转换为向量"""
    count = 0
    for key in ["dW1", "db1", "dW2", "db2", "dW3", "db3"]:
        new_vector = np.reshape(gradients[key], (-1, 1))
        
        if count == 0:
            theta = new_vector
        else:
            theta = np.concatenate((theta, new_vector), axis=0)
        count += 1
    
    return theta

def forward_propagation_n(X, Y, parameters):
    """
    实现 N 维前向传播
    
    参数:
    X -- 训练集
    Y -- 标签
    parameters -- 包含 W1, b1, W2, b2, W3, b3 的参数字典
    
    返回:
    cost -- 代价函数值
    cache -- 缓存的中间值
    """
    m = X.shape[1]
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]
    W3 = parameters["W3"]
    b3 = parameters["b3"]

    Z1 = np.dot(W1, X) + b1
    A1 = relu(Z1)
    Z2 = np.dot(W2, A1) + b2
    A2 = relu(Z2)
    Z3 = np.dot(W3, A2) + b3
    A3 = sigmoid(Z3)

    logprobs = np.multiply(-np.log(A3), Y) + np.multiply(-np.log(1 - A3), 1 - Y)
    cost = 1. / m * np.sum(logprobs)
    
    cache = (Z1, A1, W1, b1, Z2, A2, W2, b2, Z3, A3, W3, b3)
    
    return cost, cache

def backward_propagation_n(X, Y, cache):
    """
    实现 N 维反向传播
    
    参数:
    X -- 输入数据
    Y -- 真实标签
    cache -- 前向传播的缓存
    
    返回:
    gradients -- 梯度字典
    """
    m = X.shape[1]
    (Z1, A1, W1, b1, Z2, A2, W2, b2, Z3, A3, W3, b3) = cache
    
    dZ3 = A3 - Y
    dW3 = 1. / m * np.dot(dZ3, A2.T)
    db3 = 1. / m * np.sum(dZ3, axis=1, keepdims=True)
    
    dA2 = np.dot(W3.T, dZ3)
    dZ2 = np.multiply(dA2, np.int64(A2 > 0))
    dW2 = 1. / m * np.dot(dZ2, A1.T)
    db2 = 1. / m * np.sum(dZ2, axis=1, keepdims=True)
    
    dA1 = np.dot(W2.T, dZ2)
    dZ1 = np.multiply(dA1, np.int64(A1 > 0))
    dW1 = 1. / m * np.dot(dZ1, X.T)
    db1 = 1. / m * np.sum(dZ1, axis=1, keepdims=True)
    
    gradients = {"dZ3": dZ3, "dW3": dW3, "db3": db3,
                 "dA2": dA2, "dZ2": dZ2, "dW2": dW2, "db2": db2,
                 "dA1": dA1, "dZ1": dZ1, "dW1": dW1, "db1": db1}
    
    return gradients

def gradient_check_n(parameters, gradients, X, Y, epsilon=1e-7):
    """
    实现 N 维梯度检查
    
    参数:
    parameters -- 参数字典
    gradients -- 梯度字典
    X -- 输入数据
    Y -- 真实标签
    epsilon -- 微小偏移量
    
    返回:
    difference -- 梯度差异
    """
    parameters_values, _ = dictionary_to_vector(parameters)
    grad = gradients_to_vector(gradients)
    num_parameters = parameters_values.shape[0]
    J_plus = np.zeros((num_parameters, 1))
    J_minus = np.zeros((num_parameters, 1))
    gradapprox = np.zeros((num_parameters, 1))
    
    for i in range(num_parameters):
        thetaplus = np.copy(parameters_values)
        thetaplus[i][0] = thetaplus[i][0] + epsilon
        J_plus[i], _ = forward_propagation_n(X, Y, vector_to_dictionary(thetaplus))
        
        thetaminus = np.copy(parameters_values)
        thetaminus[i][0] = thetaminus[i][0] - epsilon
        J_minus[i], _ = forward_propagation_n(X, Y, vector_to_dictionary(thetaminus))
        
        gradapprox[i] = (J_plus[i] - J_minus[i]) / (2 * epsilon)
    
    numerator = np.linalg.norm(grad - gradapprox)
    denominator = np.linalg.norm(grad) + np.linalg.norm(gradapprox)
    difference = numerator / denominator

    if difference > 2e-7:
        print("\033[93m" + "反向传播存在错误! difference = " + str(difference) + "\033[0m")
    else:
        print("\033[92m" + "反向传播完全正确! difference = " + str(difference) + "\033[0m")
    
    return difference

if __name__ == "__main__":
    # 测试一维梯度检查
    print("=== 一维梯度检查测试 ===")
    x, theta = 2, 4
    difference = gradient_check(x, theta)
    print(f"difference = {difference}\n")
    
    print("梯度检查是验证反向传播实现正确性的重要工具!")