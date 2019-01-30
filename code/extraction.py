'''Module d'extraction des images et labels de la base de données MNIST.'''
import sys
import os
import numpy as np
import time
import gzip
from urllib.request import urlretrieve

def load_images():
    def download_images(filename, source='http://yann.lecun.com/exdb/mnist/'):
        if not os.path.exists(filename):
            print("Downloading %s" % filename)
            urlretrieve(source + filename, filename)
        with gzip.open(filename, 'rb') as f:
            data = np.frombuffer(f.read(), np.uint8, offset=16)
        data = data.reshape(-1, 1, 28, 28)
        return data / np.float32(256)
    X_train = download_images('train-images-idx3-ubyte.gz')
    X_test = download_images('t10k-images-idx3-ubyte.gz')
    X_train, X_val = X_train[:-10000], X_train[-10000:]
    return X_train, X_val, X_test

def load_labels():
    def download_labels(filename, source='http://yann.lecun.com/exdb/mnist/'):
        if not os.path.exists(filename):
            print("Downloading %s" % filename)
            urlretrieve(source + filename, filename)
        with gzip.open(filename, 'rb') as f:
            data = np.frombuffer(f.read(), np.uint8, offset=8)
        return data
    y_train = download_labels('train-labels-idx1-ubyte.gz')
    y_test = download_labels('t10k-labels-idx1-ubyte.gz')
    y_train, y_val = y_train[:-10000], y_train[-10000:]
    return y_train, y_val, y_test

def return_this(value):
    X_train, X_val, X_test = load_images()
    y_train, y_val, y_test = load_labels()
    return eval(value)

if __name__ == '__main__':
    print(load_images(),load_labels())

# Copyright aunetx 2018
