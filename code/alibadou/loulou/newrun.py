import numpy as np
from rnn import *
import mnist
import matplotlib.pyplot as plt
import matplotlib.image as image
from PIL import Image

learn = False
save_it = True
filename = 'saved.npy'
trX, trY, teX, teY = mnist.load_data() # Load model
weights = np.load(filename)

def predire(X, weights):
    a = [X]
    for w in weights:
        a.append(np.maximum(a[-1].dot(w),0))
    return a

x=Image.open('thisisa7.png','r')
x=x.convert('LA')
print(x)
x=np.asarray(x.getdata(),dtype=np.float64).reshape((x.size[1],x.size[0]))
plt.imshow(x, cmap='gray')
plt.show()
print("Let's predict it")
prediction = np.argmax(predire(x, weights)[-1])
print(prediction)
