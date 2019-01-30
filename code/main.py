import extraction as load_ressources
from xNn.acht import *
import numpy as np
#import matplotlib.pyplot as plt

#       Définition des hyperparamètres
#   Architecture du NN
entrees = 784
architecture = [
    {"neurones": 100, "activation": "sigmoid"}, # couche d'entrée
    {"neurones": 10, "activation": "sigmoid"},
    {"neurones": 1, "activation": "sigmoid"}, # couche de sorties
]
epochs = 100000
learning_rate = 0.1

X = load_ressources.return_this('X_train')
Y = load_ressources.return_this('y_train')
X = X[0]
X = X[0]
X = X.flatten()
print(np.shape(X))
y=np.array([Y]).T
print(y[0])

train(X, 0.5, learning_rate, architecture, entrees, epochs)



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
