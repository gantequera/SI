# Dimension con la que vamos a trabajar. En nuestro caso 28*28
import random

def generar_clasificador_debil(dimension_datos):
    return (random.randint(0, dimension_datos-1), random.randint(0, 255), random.choice((-1, 1)))

def aplicar_clasificador_debil(clasificador, imagen):
    v = imagen[:,clasificador[0]]
    return ((v >= clasificador[1]) * 1 + (v < clasificador[1]) * -1) * clasificador[2]

def obtener_error(clasificador, X, Y, D):
    return D * (aplicar_clasificador_debil(clasificador, X) != Y)