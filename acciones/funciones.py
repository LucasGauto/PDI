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


# Funcion para obtener el renlgon de datos del examen --> devuelve la iamgen ya recortada
def obtener_renglon_de_datos(examen):
    """
    Devuelve la imagen del renglón de los campos a analizar
    """
    img = cv2.imread(examen, cv2.IMREAD_GRAYSCALE)
    umbral, umbralizada = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
    img_neg = umbralizada==0  #True -> blanco, False --> negro

    img_row_zeros = img_neg.any(axis=1)
    x = np.diff(img_row_zeros)
    renglones_indxs = np.argwhere(x)  # me devuelve donde empieza y termina el renglon, me interesa la pos 2 y 3
    renglon_de_datos = [renglones_indxs[2], renglones_indxs[3]]
    # Genero imagen para pasar como argumento a la otra que analiza el texto
    recorte_renglon = img[renglon_de_datos[0][0]:renglon_de_datos[1][0], :]
    return recorte_renglon

def obtener_datos_de_campos(imagen):
    """ 
    Funcion que devuelve una lista con las imagenes de los campos completados
    """
    campos = imagen
    
    _, umbral = cv2.threshold(campos, 220, 255, cv2.THRESH_BINARY)
    contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    campos = []

    for c in contornos:
        x, y, w, h = cv2.boundingRect(c) 
        
        if w > 77:
          # chequeo que la posiscion de x no sea 569 porque coincide con el ancho del campo de codigo
          if x == 569:
            continue

          campos.append((x, y, w, h))

    # Genero imagenes para pasar como argumento a la otra que analiza los caracteres:
    indv_datos_del_examen=[]
    campos_a_retornar=imagen.copy()
    for x, y, w, h in campos:
      indv_datos_del_examen.append(campos_a_retornar[y+3:y+h-3, x+3:x+w-3]) # Agrego los recortes de los campos, el +3, -3 para descartar los borde
    
    return indv_datos_del_examen

def contar_componentes(campos):
    """
    Función que cuenta los caracteres de mi imagen
    """
    componentes={}
    con = 0
    
    for imagen in campos:
      ret, thresh = cv2.threshold(imagen, 127, 255, 0)

      #cv2 Componets detecta los blancos como porciones de componentes --> hay que invertir los bits 
      img = cv2.bitwise_not(thresh)     
      output = cv2.connectedComponentsWithStats(img)
      caracteres = output[0]-1
        
      stats = output[2]
      sort_index = np.argsort(stats[:, 0])
      stats = stats[sort_index]
      
      # Descartar las componentes de ancho pequeño
      for i in range(len(stats)):
        if i >= 1:
          anchura = stats[i][2]
          if anchura <= 2:
             caracteres = caracteres -1

      espacios =  []
      for i in range(len(stats)):
        if i > 1: # para calcular la diferencia con el anterior
          val_espacio = stats[i][0]-(stats[i-1][0]) # calculo la diferencia entre la cordenada x de mi componente siguiente y la anterior
          if val_espacio > 9 and  i > 2: # > 2 Es para descartar el vector de mi primer componente. Porque las masyusculas tienden a ser mas anchas y no corresponden a espacios
            espacios.append(val_espacio)  
       
      clave = f"campo_{con}"
      componentes[clave] = (caracteres, len(espacios))
      con = con + 1

    return componentes

def validar_caracteres(componentes):

  for val, keys in componentes.items():
    n_caracteres = keys[0]
    espacios = keys[1]

    if val == "campo_1":
       if n_caracteres == 1:
          print("CODE:OK")
       else:
          print("CODE: MAL")  
       
    if val == "campo_2" or val == "campo_0": 
       if n_caracteres == 8:
          if val == "campo_0": 
            print("DATE:OK")
          else:
            print("ID:OK")
       else:
          if val == "campo_0": 
            print("DATE:MAL")
          else: 
            print("ID: MAL")  

    if val == "campo_3":
       if n_caracteres > 1 and  n_caracteres <= 25 and espacios == 1:
          print("NAME:OK")
       else:
          print("NAME: MAL")       
      
def obtener_campo_nombre(examen):
    '''Función que evuelve los crop de los campos name'''
    renglon = obtener_renglon_de_datos(examen)
    # Como sé que el ultimo campo es el nombre, me quedo con ese
    campos_datos = obtener_datos_de_campos(renglon)
    name = campos_datos[3]
    #plt.figure(), plt.imshow(renglon, cmap='gray'),  plt.show(block=True)
    return name

def generar_imagen_salida(resultados):
    
    '''Función para generar la imágen de salida'''
    # Crear una imagen en blanco para la salida
    height = len(resultados) * 60
    width = 400
    output_image = np.ones((height, width, 3), np.uint8) * 255

    # Iterar sobre los resultados y generar los crops de los campos Name
    y = 20
    for examen, respuestas_correctas in resultados:
        # Obtener el campo Name del examen
        campo_name = obtener_campo_nombre(examen)
        #plt.figure(), plt.imshow(campo_name, cmap='gray'),  plt.show(block=True)
        h, w = campo_name.shape[:3]

        # Dibujar el crop del campo Name en la imagen de salida
        output_image[y:y+h, :w, 1] = campo_name
        # Escribir el nombre del examen y el número de respuestas correctas
        if respuestas_correctas >= 20:
            text = f"Examen: APROBADO"
        else:
            text = f"Examen: DESAPROBADO"

        cv2.putText(output_image, text, (w + 5, y + h // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        y += h + 10

    # Guardar la imagen de salida
    cv2.imwrite('output_image.png', output_image)
    plt.imshow(output_image)
    plt.axis('off')
    plt.show()


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

    img = cv2.imread(examen, cv2.IMREAD_GRAYSCALE)

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
        lista.append(img[inicio:fin,:])

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