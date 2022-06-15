import clasificador_debil as cd, math, numpy as np, matplotlib.pyplot as plt

def entrenar(X, Y, T, A):
    clasificadores_debiles = []
    alphas = []
    D = np.full(len(X), 1.0/len(X))

    for t in range(T):
        conjuntos = []
        for k in range(A):
            c_d = cd.generar_clasificador_debil(28*28)                  # Obtenemos un clasificador debil
            clas = cd.aplicar_clasificador_debil(c_d, X)         # Guardamos las clasificaciones de las imagenes
            eps = np.sum(cd.obtener_error(c_d, X, Y, D))      # Calculamos el error 
            conjuntos.append((c_d, eps, clas))
        pri = True
        for elem in conjuntos:
            if pri:
                fc = elem
                pri = False
                continue
            if elem[1] < fc[1]:           # Guardamos el conjunto con menor error
                fc = elem  
        alph = 0.5*math.log2((1-fc[1])/fc[1])
        alphas.append(alph)
        clasificadores_debiles.append(fc[0])

        Z = np.sum(D)
        for i in range(len(D)):
            D[i] = (D[i]*(math.e**(-alph*Y[i] * fc[2][i])))/Z
        
    return (clasificadores_debiles, alphas)

