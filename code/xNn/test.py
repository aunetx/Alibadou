import numpy as np
import mnist

def feed_forward(X, weights):
    a = [X]
    for w in weights:
        a.append(np.maximum(a[-1].dot(w),0)) # Calculer l'avancée
        # np.maximum(val, 0) -> relu
        # a[-1].dot(w) -> valeur * poids
        # a.append -> rajouter la valeur à la fin du tableau
    return a

def grads(X, Y, weights):
    grads = np.empty_like(weights) # grads représente la matrice de correction des poids
    a = feed_forward(X, weights) # on nourrit le réseau et on stocke les valeurs des neurones dans 'a'
    delta = a[-1] - Y # on calcule l'erreur totale
    grads[-1] = a[-2].T.dot(delta)
    for i in range(len(a)-2, 0, -1):
        delta = (a[i] > 0) * delta.dot(weights[i].T)
        grads[i-1] = a[i-1].T.dot(delta)
    return grads / len(X)

trX, trY, teX, teY = mnist.load_data() # Load model
weights = [np.random.randn(*w) * 0.1 for w in [(784, 100), (100, 10)]] # Initialiser les poids
num_epochs, batch_size, learn_rate = 30, 20, 0.1 # Initialiser les hyperparamètres

for i in range(num_epochs):
    for j in range(0, len(trX), batch_size):
        X, Y = trX[j:j+batch_size], trY[j:j+batch_size]
        weights -= learn_rate * grads(X, Y, weights)
    prediction = np.argmax(feed_forward(teX, weights)[-1], axis=1)
    print(i+1, np.mean(prediction == np.argmax(teY, axis=1)))
