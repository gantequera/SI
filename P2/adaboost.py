import clasificador_debil as cd

def entrenar(X, Y, T, A):
    clasificadores_debiles = []
    alphas = []

    ###########################
    #### Bloque de ejemplo ####

    # Datos
    imagenes_X = [[3,234,50], [1,89,100], [245,130,134]]
    etiquetas_Y = [1, -1, 1]
    D = [0,0,0]

    # Obtenemos un clasificador debil
    c_d = cd.generar_clasificador_debil(28*28)

    # Aplicamos el clasificador a una imagen
    res = cd.aplicar_clasificador_debil(c_d, imagenes_X[0])

    # Calculamos el error 
    error = cd.obtener_error(c_d, imagenes_X, etiquetas_Y, D)

    ##########################

    print("COMPLETAR ENTRENAMIENTO")
    
    return (clasificadores_debiles, alphas)