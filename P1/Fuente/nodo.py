from math import sqrt

def heuristicaDiagonal(c1, c2):
    return max(abs(c1.getFila() - c2.getFila()), abs(c1.getCol() - c2.getCol()))

def heuristicaManhattan(c1, c2):
    return abs(c2.getCol() - c1.getCol()) + abs(c2.getFila() - c1.getFila())

def heuristicaEuclidea(c1, c2):
    return sqrt((c2.getCol() - c1.getCol())**2 + (c2.getFila() - c1.getFila())**2)

def heuristica(c1, c2):
    return 

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

    def calcular(self, destino):
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

        #self.h = max(heuristicaEuclidea(self.casilla, destino), heuristicaDiagonal(self.casilla, destino), heuristicaManhattan(self.casilla, destino))
        self.h = heuristicaManhattan(self.casilla, destino)

        self.f = self.g + self.h