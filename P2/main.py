# Importamos las librerias que necesitaremos
from email.utils import encode_rfc2231
import numpy as np
import matplotlib.pyplot as plt
import clasificador_debil as cd
import math
import utils
import adaboost

def aplicar_clasificador_fuerte(clasificadores, alphas, imagen):
    clasificacion = 0
    for i in range(len(clasificadores)):
      clasificacion += alphas[i] * cd.aplicar_clasificador_debil(clasificadores[i], np.array([imagen]))
    
    return clasificacion

def test(X, Y, clasificadores, alphas):
    correct = np.full(10, 0)
    total = np.full(10, 0)

    for i in range(len(X)):
        total[Y[i]] += 1
        clasif = (-1, 0)
        for j in range(10):
            punt = (aplicar_clasificador_fuerte(clasificadores[j], alphas[j], X[i]))
            if punt > clasif[1]:
                clasif = (j, punt)
        if Y[i] == clasif[0]: 
            correct[clasif[0]] += 1

    return correct/total

def testn(X, Y, clasificadores, alphas, n):
    correct = total = 0

    for i in range(len(X)):
        if (Y[i] != n):
            continue
        total += 1
        clasif = (-1, 0)
        for j in range(10):
            punt = (aplicar_clasificador_fuerte(clasificadores[j], alphas[j], X[i]))
            if punt > clasif[1]:
                clasif = (j, punt)
        if n == clasif[0]: 
            correct += 1

    return correct/total

def entrenar_sistema(mnist_X, mnist_Y, T, A):
    clasificadores = []
    alphas = []
    print("Proceso de entrenamiento")
    for clase in range(10):
        print(f"Clasificador de la clase \"{clase}\" en proceso de entrenamiento")
        (trainX, trainY) = utils.adaptar_conjuntos_t(mnist_X, mnist_Y, clase)
        (cl, al) = adaboost.entrenar(trainX, trainY, T, A)
        clasificadores.append(cl)
        alphas.append(al)
    return (clasificadores, alphas)

def valorarAT(X, Y, A, T):
    At = range(10, 1001, 30)
    resultsA = []
    for i in At:
        (clasificadores, alphas) = entrenar_sistema(X, Y, T, i)
        (testX, testY) = utils.adaptar_conjuntos_test(X, Y)
        resultsA.append(test(testX, testY, clasificadores, alphas))    

    Ta = range(10, 101, 10)
    resultsT = []
    for i in Ta:
        (clasificadores, alphas) = entrenar_sistema(X, Y, i, A)
        (testX, testY) = utils.adaptar_conjuntos_test(X, Y)
        resultsT.append(test(testX, testY, clasificadores, alphas))
    return (resultsA, resultsT)    

npzfile = np.load("mnist.npz")  # Datos
mnist_X = npzfile['x']
mnist_Y = npzfile['y']

T = 50
A = 200
(rA, rT) = valorarAT(mnist_X, mnist_Y, A, T)

At = range(10, 1001, 30)
Ta = range(10, 101, 10)

plt.figure()
plt.plot(rA, At, 'r-o')
plt.title("T = 50")
plt.savefig("valA.pdf", format="pdf")
plt.close()

plt.figure()
plt.plot(rT, Ta, 'b-o')
plt.title("A = 200")
plt.savefig("valT.pdf", format="pdf")

#(clasificadores, alphas) = entrenar_sistema(mnist_X, mnist_Y, T, A)
#(testX, testY) = utils.adaptar_conjuntos_test(mnist_X, mnist_Y)
#print(f"Porcentaje de aciertos del sistema para clase 0: {testn(testX, testY, clasificadores, alphas, 8) * 100}")
#precision = test(testX, testY, clasificadores, alphas)

#plt.figure()
#plt.plot(range(10), precision, 'r-o')
#for cordx,cordy in zip(range(10),precision):
#    label = "{:.2f}".format(cordy)
#    plt.annotate(label, (cordx,cordy), textcoords="offset points", xytext=(0,10), ha='center')
#plt.title('Aciertos sobre el total de imagenes por dígito (%)')
#plt.show()
#print(f"Media del sistema: {(np.average(precision) * 100)}%")
