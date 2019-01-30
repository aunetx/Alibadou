import numpy as np

def derivee(x, activation='sigmoid'):
    activation_derivee = activation + '_der'
    return eval(activation_derivee)(x)


def sigmoid_der(x):
    return sigmoid(x) * (1 - sigmoid(x))


def sigmoid(x):
    return 1/(1+np.exp(-x))

a = [0.25]
p = [0.47584115]
activee = -0.09671072

print(sigmoid(activee))
print(derivee(sigmoid(activee)))
