from math import sqrt

from casilla import Casilla

def heuristicaDiagonal(c1, c2):
    return max(abs(c1.getFila() - c2.getFila()), abs(c1.getCol() - c2.getCol()))

def heuristicaManhattan(c1, c2):
    return abs(c2.getCol() - c1.getCol()) + abs(c2.getFila() - c1.getFila())

def heuristicaEuclidea(c1, c2):
    return sqrt((c2.getCol() - c1.getCol())**2 + (c2.getFila() - c1.getFila())**2)

def heuristicaMinkowski(c1, c2):    #generalización de la euclidea y manhattan, donde el exponente en lugar de ser 2 o 1,
    p = 3                           #respectivamente para las otras, se ha escogido 3
    return (abs(c2.getCol() - c1.getCol())**p + abs(c2.getFila() - c1.getFila())**p)**(1/p)

class Nodo:
    def __init__(self, casilla, padre, destino):
        self.casilla = casilla
        self.padre = padre
        self.calcular(destino)

    def getF(self):
        return self.f
    
    def getG(self):
        return self.g

    def getH(self):
        return self.h

    def getCasilla(self):
        return self.casilla
    
    def getPadre(self):
        return self.padre

    def calcG(self):
        g = 0
        if self.casilla != self.padre:
            if abs(self.casilla.getFila() - self.padre.getCasilla().getFila()) == 1:
                g = 1
            if abs(self.casilla.getCol() - self.padre.getCasilla().getCol()) == 1:
                if g == 1:
                    g = 1.5
                else:
                    g = 1
            g += self.padre.getG()
        self.g = g
    
    def calcH(self, destino):
        #self.h = max(heuristicaEuclidea(self.casilla, destino), heuristicaDiagonal(self.casilla, destino), heuristicaManhattan(self.casilla, destino))
        self.h = heuristicaMinkowski(self.casilla, destino)

    def calcular(self, destino):
        self.calcG()
        self.calcH(destino)
        self.f = self.g + self.h

class NodoAjustado(Nodo):
    w = 0.5
    def calcular(self, destino):
        self.calcG()
        self.calcH(destino)
        self.f = (1 - NodoAjustado.w)*self.g + NodoAjustado.w*self.h