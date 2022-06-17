import utils
import adaboost
import math
import numpy as np

def test(X, Y, clasificadores, alphas):
    correct = np.full(10, 0)
    total = np.full(10, 0)

    for i in range(len(X)):
        total[Y[i]] += 1
        clasif = (-1, 0)
        for j in range(10):
            punt = (utils.aplicar_clasificador_fuerte(clasificadores[j], alphas[j], X[i]))
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
            punt = (utils.aplicar_clasificador_fuerte(clasificadores[j], alphas[j], X[i]))
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

def valorarAT(X, Y, A, T, At, Ta):
    resultsA = []
    for i in At:
        (clasificadores, alphas) = entrenar_sistema(X, Y, T, i)
        (testX, testY) = utils.adaptar_conjuntos_test(X, Y)
        resultsA.append(test(testX, testY, clasificadores, alphas))    

    resultsT = []
    for i in Ta:
        (clasificadores, alphas) = entrenar_sistema(X, Y, i, A)
        (testX, testY) = utils.adaptar_conjuntos_test(X, Y)
        resultsT.append(test(testX, testY, clasificadores, alphas))
    return (resultsA, resultsT)    