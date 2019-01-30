import numpy as np
from rnn import *
import mnist
import matplotlib.pyplot as plt
import matplotlib.image as image

learn = False
save_it = True
filename = '5 layers.npy'
trX, trY, teX, teY = mnist.load_data() # Load model
weights = np.load(filename)

def predire(X, weights):
    a = [X]
    for w in weights:
        a.append(np.maximum(a[-1].dot(w),0))
    return a

topred = 1 - image.imread('zero.png').reshape(784,4).mean(axis=1)
img = topred.reshape(28,28)
plt.imshow(img, cmap='gray')
plt.show()
print("Let's predict it")
prediction = predire(topred, weights)[-1]
print(prediction)
print(np.argmax(prediction))
