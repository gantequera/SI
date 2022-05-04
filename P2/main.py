# Importamos las librerias que necesitaremos
import numpy as np
import matplotlib.pyplot as plt
import utils
import adaboost

# Cargamos la base de datos
npzfile = np.load("mnist.npz")
mnist_X = npzfile['x']
mnist_Y = npzfile['y']

# Mostrar una imagen y su etiqueta
utils.mostrar_imagen(mnist_X[0])
print(mnist_Y[0])

# Adaptar los conjuntos X e Y a AdaBoost
(X, Y) = utils.adaptar_conjuntos(mnist_X, mnist_Y)

# Lanzar Adaboost
T = A = 1
c_f = adaboost.entrenar(X, Y, T, A)

# Analisis y resultados de las pruebas realizadas
T = [0, 100, 200, 300, 400]      # Numero de clasificadores 
resultados = [0, 20, 35, 56, 68] # Resultados obtenidos de clasificacion
utils.plot_arrays(T, resultados, "Porcentajes con valores de T")