import extraction as load_ressources
from snn import *
#import matplotlib.pyplot as plt
import numpy as np

#       Définition des hyperparamètres
#   Architecture du NN
sNn_arch = [
    {"entrees": 784, "neurons": 16, "activation": "relu"}, # input layer
    {"entrees": 16, "neurons": 12, "activation": "relu"},
    {"entrees": 12, "neurons": 12, "activation": "relu"},
    {"entrees": 12, "neurons": 10, "activation": "sigmoid"}, # output layer
]
epochs = 100
learning_rate = 0.01

X = load_ressources.return_this('X_train')
Y = load_ressources.return_this('y_train')
X = X[0]
X = X[0]
X = X.flatten()
Y = Y[0]
print(Y)
y = np.zeros(10).reshape(1,10)
print(y)
y[0][Y] = 1.
print(y)

train(X, y, sNn_arch, epochs, learning_rate)



def imgShow(index):
    X_train = load_ressources.return_this('X_train')
    i = 0
    for image in X_train:
        if i == index:
            img = image[0]
            print(image)
            plt.imshow(img, cmap='gray')
            plt.show()
            break
        i = i+1

#img = X_train[0]
#img = img[0]
#plt.imshow(img, cmap='gray')
#plt.show()

# Copyright aunetx 2018
