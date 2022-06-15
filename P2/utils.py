import matplotlib.pyplot as plt
import numpy as np

TRAIN = 20000
TEST = 30000

def adaptar_conjuntos_t(mnist_X, mnist_Y, n):
    X = mnist_X[:TRAIN].reshape(TRAIN, 784)
    Y = []
    for i in range(len(mnist_Y[:TRAIN])):
        if mnist_Y[i] == n:
            Y.append(1)
        else:
            Y.append(-1)
    
    return (X, Y)

def adaptar_conjuntos_test(mnist_X, mnist_Y):
  X = mnist_X.copy()
  X = np.reshape(X[TRAIN:TEST], (TEST - TRAIN, 784))

  return (X, mnist_Y)

def mostrar_imagen(imagen):
    plt.figure()
    plt.imshow(imagen)
    plt.show()

def plot_arrays(X, Y, title):
    plt.title(title)
    plt.plot(X, Y)
    plt.show()