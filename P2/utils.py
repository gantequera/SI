import matplotlib.pyplot as plt
import numpy as np
import clasificador_debil as cd

DIV = 40000

def adaptar_conjuntos_t(mnist_X, mnist_Y, n):
    X = mnist_X[:DIV].reshape(DIV, 784)
    Y = []
    for i in range(len(mnist_Y[:DIV])):
        if mnist_Y[i] == n:
            Y.append(1)
        else:
            Y.append(-1)
    
    return (X, Y)

def adaptar_conjuntos_test(mnist_X, mnist_Y):
  X = mnist_X.copy()
  X = np.reshape(X[DIV:], (60000 - DIV, 784))

  return (X, mnist_Y)

def aplicar_clasificador_fuerte(clasificadores, alphas, imagen):
    clasificacion = 0
    for i in range(len(clasificadores)):
      clasificacion += alphas[i] * cd.aplicar_clasificador_debil(clasificadores[i], np.array([imagen]))
    
    return clasificacion

def mostrar_imagen(imagen):
    plt.figure()
    plt.imshow(imagen)
    plt.show()

def plot_arrays(X, Y, title):
    plt.title(title)
    plt.plot(X, Y)
    plt.show()