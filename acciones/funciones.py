import cv2
import numpy as np
import matplotlib.pyplot as plt

def ecualizacionLocal(window_size = 25):
    '''
    Toma la ruta de una imagen y devuelve la misma imagen pero ecualizada localmente.
    '''
    #Primero realizamos una carga y visualización de la imagen
    imagen = cv2.imread('Imagen_con_detalles_escondidos.tif', cv2.IMREAD_GRAYSCALE)
    
    #Funcion para ecualizar localmente
    def local_histogram_equalization(img, window_size):
        '''
        Calcula la ecualizacion local de histograma
        '''
        h, w = img.shape #Toma el alto y ancho de la imagen
        img_equalized = np.zeros((h, w), dtype=np.uint8) #Se crea una imagen base en blanco
        
        #Se toma la mitad de la imagen para calcular el desplazamiento
        #de la ventana desde el centro, donde el centro es i,j
        half_size = window_size // 2

        for i in range(h):
            for j in range(w):
                i_min = max(0, i - half_size) #Para que no tome una fila menor a 0
                i_max = min(h, i + half_size + 1) #Lo mismo pero mayor a 255
                j_min = max(0, j - half_size) #Lo mismo para las columnas
                j_max = min(w, j + half_size + 1) #etc

                # Obtener la subimagen dentro de la ventana
                window = img[i_min:i_max, j_min:j_max]

                # Ecualizar el histograma localmente
                window_equalized = cv2.equalizeHist(window)

                # Asignar el valor ecualizado al píxel central de la ventana en la imagen resultante
                img_equalized[i, j] = window_equalized[i - i_min, j - j_min]

        return img_equalized

    #window_size = 25

    imagen_ecualizada_localmente = local_histogram_equalization(imagen, window_size)

    #plt.imshow(imagen_ecualizada_localmente, cmap = 'gray')
    #plt.show(block=False)
    return imagen_ecualizada_localmente

def adecuar(NombreImagen:str):
    '''
    Toma la imagen leida y extrae solamente la parte del examen
    '''
    img = cv2.imread(NombreImagen, cv2.IMREAD_GRAYSCALE)
    #---------- UMBRALADO ------------
    '''
    Las siguientes líneas llevan los píxeles menores de 150 a 0 y,
    los mayores, a 255, quedando una imagen solo con blancos y negros.
    '''
    img[img < 150] = 0 #umbralado negro
    img[img > 150] = 255 #Umbralado blanco

    #----- RECORTAR EL ENCABEZADO -----
    y = 140
    imgRecortada = img[y:]

    #------ SELECCIONAR SOLO LAS RESPUESTAS -------

    '''
    Razonamiento:

    Como la imagen tiene 916 pixeles en sus columnas
    podemos decir que una fila toda blanca tendra una suma
    de 255*816. Por lo tanto, si la suma de la fila da un valor
    menor a ese numero, podemos decir que ya hay algun valr igual
    a 0
    '''
    #Recortar filas
    def sumar_filas(matriz):
        '''
        Recibe un array de mas de una dimensión, recorre la dimensión
        inferior y realiza la suma de sus elementos.
        '''
        suma_filas = []
        for fila in matriz:
            suma = sum(fila)
            suma_filas.append(suma)
        return suma_filas

    sumaFilas = sumar_filas(imgRecortada) #lista de longitud = filas matriz con la suma de cada fila

    cant_filas, cant_columnas = imgRecortada.shape

    contador = 1
    for i in sumaFilas:
        if i != 255*cant_columnas:
            #print(f'La fila n° {contador} es la primera con un valor distinto de blanco')
            break
        contador += 1


    examenRecorte1 = imgRecortada[contador-1:]
    examenRecorte2 = examenRecorte1[:766] #766 es el alto del examen

    #Recortar columnas

    imgTraspuesta = examenRecorte2.T #trasponemo'

    sumaColumnas = sumar_filas(imgTraspuesta)

    cant_filas,cant_columnas = examenRecorte2.shape

    contador = 1
    for i in sumaColumnas:
        if i != 255*cant_filas:
            #print(f'La columna n° {contador} es la primera con un valor distinto de blanco')
            break
        contador += 1

    imagenRecorte3 = examenRecorte2[:,contador-1:]
    ancho_examen = 197

    examen = imagenRecorte3[:,:ancho_examen] #Imagen sobre la que trabajar

    return examen

def corregir(examen):

    respuestasCorrectas = {
        1: 'A',
        2: 'A',
        3: 'B',
        4: 'A',
        5: 'D',
        6: 'B',
        7: 'B',
        8: 'C',
        9: 'B',
        10: 'A',
        11: 'D',
        12: 'A',
        13: 'C',
        14: 'C',
        15: 'D',
        16: 'B',
        17: 'A',
        18: 'C',
        19: 'C',
        20: 'D',
        21: 'B',
        22: 'A',
        23: 'C',
        24: 'C',
        25: 'C'
    }

    separacion_entre_letras = 6
    ancho_de_las_letras = 23

    lista = []
    cantidad_preguntas = 25
    longitud_renglon = 20
    espacio_entre_renglones = 11

    for i in range(cantidad_preguntas):
        inicio = longitud_renglon * i + espacio_entre_renglones * i
        fin = inicio + 20
        lista.append(examen[inicio:fin,:])

    '''
    Las preguntas ya estan separadas.
    Ahora hay que ver como comprobar cual fue la que se seleccionó.
    Para ello se nos ocurrió hacerlo por posición y sumando los valores.
    Es evidente que una letra marcada tendrá una suma de sus valores muy baja
    porque la mayoria de sus valores son = 0.
    Se nos ocurrió tomar la fila de en medio de cada respuesta, separar por posicion
    y realizar la suma de sus filas. Aquella que posea una suma más baja será la 
    seleccionada.
    '''

    respuestasAlumno = {}

    contador = 1
    for respuesta in lista:
        #Seteo las posiciones para cada letra
        A = sum(respuesta[10:11,61:81][0])
        B = sum(respuesta[10:11,90:111][0])
        C = sum(respuesta[10:11,119:140][0])
        D = sum(respuesta[10:11,148:168][0])
        E = sum(respuesta[10:11,177:197][0])

        opciones = [A,B,C,D,E]

        menorValor = min(opciones)

        if menorValor == opciones[0]:
            respuestasAlumno[contador] = 'A'
            contador+=1
        elif menorValor == opciones[1]:
            respuestasAlumno[contador] = 'B'
            contador+=1
        elif menorValor == opciones[2]:
            respuestasAlumno[contador] = 'C'
            contador+=1
        elif menorValor == opciones[3]:
            respuestasAlumno[contador] = 'D'
            contador+=1
        else:
            respuestasAlumno[contador] = 'E'
            contador+=1

    #COMPARACION CON LAS RESPUESTAS CORRECTAS
    correccion = {}

    for i in range(1,25+1):
        if respuestasAlumno[i] == respuestasCorrectas[i]:
            correccion[f'Pregunta {i}'] = 'OK'
        else:
            correccion[f'Pregunta {i}'] = 'MAL'

    return correccion