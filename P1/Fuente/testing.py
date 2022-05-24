from main import *

orden = [("Mundos/mapa.txt", Casilla(3, 1)),
             ("Mundos/mapa2.txt", Casilla(5, 1)),
             ("Mundos/mapa3.txt", Casilla(1, 1)),
             ("Mundos/mapaChico.txt", Casilla(6, 6)),
             ("Mundos/mapaCruz.txt", Casilla(3, 1)),
             ("Mundos/mapaCubo.txt", Casilla(4, 12)),
             ("Mundos/mapaCuboDoble.txt", Casilla(1, 12)),
             ("Mundos/mapaGrande.txt", Casilla(14, 2)),
             ("Mundos/mapaLaberinto.txt", Casilla(13, 13)),
             ("Mundos/mapaPlano.txt", Casilla(3, 1))]

def testiempo(destino, file, ajustado):    
    mapi=Mapa(file)
    origen=mapi.getOrigen()    
    camino=inic(mapi)   
    
    casi=Casilla(destino.getFila(), destino.getCol())
    if bueno(mapi, casi):                                             
        mapi.setCelda(int(origen.getFila()), int(origen.getCol()), 0) #se marca como libre la celda origen
        destino=casi                        
        camino=inic(mapi)
        # llamar al A*
        nExplorados = [0]
        mExplorados = exploIni(mapi, origen)
        start_t = time.time()
        if ajustado:
            aEstrellaAjustado(mapi, origen, destino, camino, mExplorados, nExplorados)
        else:
            aEstrella(mapi, origen, destino, camino, mExplorados, nExplorados)      
        end_t = time.time() - start_t
    return end_t*1000

def testnodos(destino, file):    
    mapi=Mapa(file)
    origen=mapi.getOrigen()    
    camino=inic(mapi)   
    
    casi=Casilla(destino.getFila(), destino.getCol())
    if bueno(mapi, casi):                                             
        mapi.setCelda(int(origen.getFila()), int(origen.getCol()), 0) #se marca como libre la celda origen
        destino=casi                        
        camino=inic(mapi)
        # llamar al A*
        nExplorados = [0]
        mExplorados = exploIni(mapi, origen)
        aEstrellaAjustado(mapi, origen, destino, camino, mExplorados, nExplorados)
    return nExplorados

def analisis(fi, aj):
    fi.write('   ')
    for x, y in orden:
        wname = ''
        for l in x:
            if l == '.':
                break
            wname += l
            if l == '/':
                wname = ''
        fi.write(wname)
        for i in range(19-len(wname)):
            fi.write(' ')
    fi.write('\n')
    for heu in ['ce', 'di', 'ma', 'eu', 'mi']: # Para cada heurística
        Nodo.heuristicaSelec = heu
        fi.write(heu + ' ')
        for file, casilla in orden: # Para cada mapa y su casilla destino
            media = 0
            for i in range(10): # se ejecuta 10 veces
                media += testiempo(casilla, file, aj)
            fi.write(str(media / 10) + " ") # se almacena el tiempo medio de ejecución
        fi.write('\n')

def nodos(fi):
    for x, y in orden:
        wname = ''
        for l in x:
            if l == '.':
                break
            wname += l
            if l == '/':
                wname = ''
        fi.write(wname)
        fi.write(' ')
    fi.write('\n')
    for heu in ['ce', 'di', 'ma', 'eu', 'mi']: # Para cada heurística
        Nodo.heuristicaSelec = heu
        fi.write(heu + ' ')
        for file, casilla in orden: # Para cada mapa y su casilla destino
            fi.write(str(testnodos(casilla, file)[0]) + " ") # se almacena el tiempo medio de ejecución
        fi.write('\n')

def anw(fi):
    nord = [orden[0], orden[3], orden[5]]
    for x, y in nord:
        wname = ''
        for l in x:
            if l == '.':
                break
            wname += l
            if l == '/':
                wname = ''
        fi.write(wname)
        fi.write(' ')
    fi.write('\n')
    Nodo.heuristicaSelec = 'mi'
    for w in [0.2, 0.5, 0.8]:
        NodoAjustado.w = w
        fi.write(str(w) + 't' + ' ')
        for file, casilla in nord: # Para cada mapa y su casilla destino
            media = 0
            for i in range(10): # se ejecuta 10 veces
                media += testiempo(casilla, file, True)
            fi.write(str(media / 10) + " ") # se almacena el tiempo medio de ejecución
        fi.write('\n')
        fi.write(str(w) + 'n' + ' ')
        for file, casilla in nord: # Para cada mapa y su casilla destino
            fi.write(str(testnodos(casilla, file)[0]) + " ") # se almacena el tiempo medio de ejecución
        fi.write('\n')

def test1():
    fi = open("Fuente/analisis-ajustado.txt", "w")
    analisis(fi, True)
    fi.close()
    fi = open("Fuente/analisis.txt", "w")
    analisis(fi, False)
    fi.close()
    print("Fin test1")

def test2():
    fi = open("Fuente/nodos.txt", "w")
    nodos(fi)
    fi.close()
    print("Fin test2")

def test3():
    fi = open("Fuente/analisis-w.txt", "w")
    anw(fi)
    fi.close()
    print("Fin test3")

test1()
test2()
test3()