import pygame
import tkinter
from tkinter import filedialog, messagebox
from casilla import *
from mapa import *
from nodo import *
from pygame.locals import *
import time

MARGEN=5
MARGEN_INFERIOR=60
TAM=30
NEGRO=(0,0,0)
BLANCO=(255, 255,255)
VERDE=(0, 255,0)
ROJO=(255, 0, 0)
AZUL=(0, 0, 255)
AMARILLO=(255, 255, 0)

# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------

# Devuelve si una casilla del mapa se puede seleccionar como destino
def bueno(mapi, pos):
    res= False
    
    if mapi.getCelda(pos.getFila(),pos.getCol())==0:
       res=True
    
    return res
    
# Devuelve si una posición de la ventana corresponde al mapa
def esMapa(mapi, posicion):
    res=False     
    
    if posicion[0] > MARGEN and posicion[0] < mapi.getAncho()*(TAM+MARGEN)+MARGEN and \
    posicion[1] > MARGEN and posicion[1] < mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res= True       
    
    return res
    
#PDevuelve si se ha pulsado el botón. Posición del botón: 20, mapa.getAlto()*(TAM+MARGEN)+MARGEN+10]
def pulsaBoton(mapi, posicion):
    res=False
    
    if posicion[0] > 20 and posicion[0] < 70 and \
       posicion[1] > mapi.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res= True
    
    return res
    
    
# Construye la matriz para guardar el camino
def inic(mapi):    
    cam=[]
    for i in range(mapi.alto):        
        cam.append([])
        for j in range(mapi.ancho):            
            cam[i].append('.')
    
    return cam

# Inicializa el mapa de nodos explorados
def exploIni(mapi, origen):
    map=[]
    for i in range(mapi.alto):        
        map.append([])
        for j in range(mapi.ancho):   
            if (origen.getFila() == i and origen.getCol() == j): 
                map[i].append(0)
            else:
                map[i].append(-1)
    return map

#################################################################################################

def equalsCasillas(c1, c2): #Dos casillas son iguales si sus filas y columnas son iguales
    if c1.getFila() == c2.getFila() and c1.getCol() == c2.getCol():
        return True
    return False

def obtenerMejor(listaNodos): #Devuelce el nodo con mayor h
    mejor = 0
    for n in listaNodos:
        if mejor == 0:
            mejor = n
        elif mejor.getF() > n.getF():
            mejor = n
    return mejor

def construirCamino(camino, nodo): #devuelve el coste del camino trazado y actualiza la matriz del camino marcando las casilla utilizadas
    g = nodo.getG()
    while type(nodo.getPadre()) == Nodo or type(nodo.getPadre()) == NodoAjustado:
        nodo = nodo.getPadre()
        camino[nodo.getCasilla().getFila()][nodo.getCasilla().getCol()] = "*" #Pertenece al camino

    return g

def listaHijos(nodo, mapa, destino, ajustado): #devuelve una lista de los nodos hijos de otro nodo
    lista = []
    for i in [0, -1, 1]:
        for j in [0, -1, 1]:
            casillaPrueba = Casilla(nodo.getCasilla().getFila() - i, nodo.getCasilla().getCol() - j)
            if bueno(mapa, casillaPrueba) and not (i == j == 0):
                if ajustado:
                    lista.append(NodoAjustado(casillaPrueba, nodo, destino))
                else:
                    lista.append(Nodo(casillaPrueba, nodo, destino))
    return lista

def seEncuentra(nodo, lista): #Comprueba si existe el nodo en la lista
    if len(lista) == 0:
        return False
    for n in lista:
        if equalsCasillas(nodo.getCasilla(), n.getCasilla()) and equalsCasillas(nodo.getPadre().getCasilla(), n.getPadre().getCasilla()):
            return True
    return False

def comparaIncluye(lista, nodo, mExplorados, nExplorados): #comprueba si la casilla está en la lista, de ser así conserva la que menor g tenga. De no estar, la añade como nodo 
    esta = False
    for n in lista:
        if equalsCasillas(n.getCasilla(), nodo.getCasilla()):
            if n.getG() > nodo.getG():
                lista.remove(n)
                lista.append(nodo)
            esta = True
    if not esta:
        lista.append(nodo)
        mExplorados[nodo.getCasilla().getFila()][nodo.getCasilla().getCol()] = nExplorados[0] + 1
        nExplorados[0] += 1

def equalsNodos(n1, n2): #Si las casillas y las casillas de los padres son iguales, los nodos son iguales 
    if not equalsCasillas(n1.getCasilla(), n2.getCasilla()):
        return False
    if type(n1.getPadre()) == Nodo or type(n1.getPadre()) == NodoAjustado:
        if type(n2.getPadre()) == Nodo or type(n2.getPadre()) == NodoAjustado:
            if not equalsCasillas(n1.getPadre().getCasilla(), n2.getPadre().getCasilla()):
                return False
        else:
            if not equalsCasillas(n1.getPadre().getCasilla(), n2.getPadre()):
                return False
    else:
        if type(n2.getPadre()) == Nodo or type(n2.getPadre()) == NodoAjustado:
            if not equalsCasillas(n1.getCasilla(), n2.getPadre().getCasilla()):
                return False
        else:
            if not equalsCasillas(n1.getPadre().getCasilla(), n2.getCasilla()):
                return False
    return True
            
def eliminarDeLista(l1, l2): #Devuelve una lista resultado de la diferencia entre la primera y la segunda (l1 - l2)
    lf = []
    for n in l1:
        esta = False
        for m in l2:
            if (equalsCasillas(n.getCasilla(), m.getCasilla())):
                esta = True
        if esta == False:
            lf.append(n)
    return lf

#Algoritmo A*
def aEstrella(mapi, origen, destino, camino, mExplorados, nExplorados):
    listaInterior = []
    listaFrontera = [Nodo(origen, origen, destino)] #inicializala lista con el nodo origen
    while len(listaFrontera) != 0:
        n = obtenerMejor(listaFrontera) # obtiene el nodo con menor coste esperado
        if equalsCasillas(n.getCasilla(), destino): #ha llegado a la meta
            return construirCamino(camino, n)
        else:
            listaFrontera.remove(n)
            listaInterior.append(n)

            for m in eliminarDeLista(listaHijos(n, mapi, destino, False), listaInterior):
                comparaIncluye(listaFrontera, m, mExplorados, nExplorados)
    return -1

#Algoritmo A* con ajuste de pesos, igual que el A* pero emplea Nodos ajustados
def aEstrellaAjustado(mapi, origen, destino, camino, mExplorados, nExplorados):
    listaInterior = []
    listaFrontera = [NodoAjustado(origen, origen, destino)] #inicializala lista con el nodo origen
    while len(listaFrontera) != 0:
        n = obtenerMejor(listaFrontera) # obtiene el nodo con menor coste esperado
        if equalsCasillas(n.getCasilla(), destino): #ha llegado a la meta
            return construirCamino(camino, n)
        else:
            listaFrontera.remove(n)
            listaInterior.append(n)

            for m in eliminarDeLista(listaHijos(n, mapi, destino, True), listaInterior):
                comparaIncluye(listaFrontera, m, mExplorados, nExplorados)
    return -1

#########################################################################################################

# función principal
def main():
    modoAjustado = False
    root= tkinter.Tk() #para eliminar la ventana de Tkinter
    root.withdraw() #se cierra
    file=tkinter.filedialog.askopenfilename() #abre el explorador de archivos    
    
    pygame.init()
    destino=Casilla(-1,-1)
    
    reloj=pygame.time.Clock()    
    
    if not file:     #si no se elige un fichero coge el mapa por defecto   
        file='Mundos/mapa.txt' 

    wname = ''
    for i in file:
        if i == '.':
            break
        wname += i
        if i == '/':
            wname = ''

    mapi=Mapa(file)
    origen=mapi.getOrigen()    
    camino=inic(mapi)   
    
    anchoVentana=mapi.getAncho()*(TAM+MARGEN)+MARGEN
    altoVentana= MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension)
    pygame.display.set_caption("Practica 1")
    
    boton=pygame.image.load("Fuente/boton.png").convert()
    boton=pygame.transform.scale(boton,[50, 30])
    
    personaje=pygame.image.load("Fuente/pig.png").convert()
    personaje=pygame.transform.scale(personaje,[TAM, TAM])   
    
    coste=-1
    running= True
    primeraVez=True
    
    if modoAjustado:
        timing = open(f"Fuente/timing/datos-{wname}-ajustado.txt", "a")
    else:
        timing = open(f"Fuente/timing/datos-{wname}.txt", "a")
    timing.write(f"\nHeuristica {Nodo.getHeuristica()}" + " {\n")

    while running:        
        #procesamiento de eventos
        for event in pygame.event.get():
            if event.type==pygame.QUIT:               
                running=False               
                
            if event.type==pygame.MOUSEBUTTONDOWN:                
                #obtener posición y calcular coordenadas matriciales
                pos=pygame.mouse.get_pos()                
                colDestino=pos[0]//(TAM+MARGEN)
                filDestino=pos[1]//(TAM+MARGEN)
                casi=Casilla(filDestino, colDestino)
                if pulsaBoton(mapi, pos): #reinicializar                    
                    origen=mapi.getOrigen()
                    destino=Casilla(-1,-1)                    
                    camino=inic(mapi)
                    coste=-1
                    primeraVez=True
                elif esMapa(mapi, pos):
                    if bueno(mapi, casi):
                        if not primeraVez: #la primera vez el origen está en el mapa
                            origen=destino                            
                        else:                          
                            mapi.setCelda(int(origen.getFila()), int(origen.getCol()), 0) #se marca como libre la celda origen
                        destino=casi                        
                        camino=inic(mapi)
                        # llamar al A*
                        nExplorados = [0]
                        mExplorados = exploIni(mapi, origen)
                        start_t = time.time()
                        if modoAjustado:
                            coste=aEstrellaAjustado(mapi, origen, destino, camino, mExplorados, nExplorados)
                        else:
                            coste=aEstrella(mapi, origen, destino, camino, mExplorados, nExplorados)      
                        end_t = time.time() - start_t
                        if coste==-1:
                            tkinter.messagebox.showwarning(title='Error', message='No existe un camino entre origen y destino')                     
                        else:
                            primeraVez=False  # hay un camino y el destino será el origen para el próximo movimiento

                        timing.write(f"Origen: [{origen.getFila()}, {origen.getCol()}]; Destino: [{destino.getFila()}, {destino.getCol()}]; Tiempo: {end_t * 1000}ms\n")
                        timing.write("Camino:\n")
                        for i in range(len(camino)):
                            for j in range(len(camino[i])):
                                timing.write(f"{camino[i][j]} ")
                            timing.write('\n')
                        timing.write("Camino explorado:\n")
                        for i in range(len(mExplorados)):
                            for j in range(len(mExplorados[i])):
                                if mExplorados[i][j] > -1 and mExplorados[i][j] < 10:
                                    timing.write(f" {mExplorados[i][j]} ")
                                else:
                                    timing.write(f"{mExplorados[i][j]} ")
                            timing.write('\n')
                        timing.write(f"Nodos exploraados: {nExplorados[0]}\n\n")

                    else: # se ha hecho click en una celda roja                
                        tkinter.messagebox.showwarning(title='Error', message='Esa casilla no es valida')                
          
        #código de dibujo        
        #limpiar pantalla
        screen.fill(NEGRO)
        #pinta mapa
        for fil in range(mapi.getAlto()):
            for col in range(mapi.getAncho()):
                if mapi.getCelda(fil, col)==2 and not primeraVez: #para que no quede negro el origen inicial
                    pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)                    
                if mapi.getCelda(fil,col)==0:
                    if camino[fil][col]=='.':
                        pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    else:
                        pygame.draw.rect(screen, AMARILLO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    
                elif mapi.getCelda(fil,col)==1:
                    pygame.draw.rect(screen, ROJO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    
        #pinta origen
        screen.blit(personaje, [(TAM+MARGEN)*origen.getCol()+MARGEN, (TAM+MARGEN)*origen.getFila()+MARGEN])    
        #pinta destino
        pygame.draw.rect(screen, VERDE, [(TAM+MARGEN)*destino.getCol()+MARGEN, (TAM+MARGEN)*destino.getFila()+MARGEN, TAM, TAM], 0)
        #pinta boton
        screen.blit(boton, [20, mapi.getAlto()*(TAM+MARGEN)+MARGEN+10])
        #pinta coste
        if coste!=-1:            
            fuente= pygame.font.Font(None, 30)
            texto= fuente.render("Coste "+str(coste), True, AMARILLO)            
            screen.blit(texto, [anchoVentana-120, mapi.getAlto()*(TAM+MARGEN)+MARGEN+15])            
            
        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)

    timing.write('}\n')
    timing.close()
        
    pygame.quit()
    
#---------------------------------------------------------------------
if __name__=="__main__":
    main()
