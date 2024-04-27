import cv2
import numpy as np
import matplotlib.pyplot as plt

# Funcion para obtener el renlgon de datos del examen --> devuelve la iamgen ya recortada
def obtener_renglon_de_datos(examen):

    img = cv2.imread(examen, cv2.IMREAD_GRAYSCALE)
    umbral, umbralizada = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
    img_neg = umbralizada==0  #True -> blanco, False --> negro
    
    img_row_zeros = img_neg.any(axis=1) # True donde está el renglón
    x = np.diff(img_row_zeros) 
    renglones_indxs = np.argwhere(x) # me devuelve donde empieza y termina el renglon, me interesa la pos 2 y 3

    renglon_de_datos=[renglones_indxs[2], renglones_indxs[3]]
    r_datos_idxs = np.reshape(renglon_de_datos, (-1,2)) # Los convierto en un array para que tenga dos columnas con los vectores
    
    datos_del_examen=[]
    # Genero imagen para pasar como argumento a la otra que analiza el texto: renglones = []
    for ir, idxs in enumerate(r_datos_idxs):
        recorte_renglon = img[idxs[0]:idxs[1], :] 
        
        datos_del_examen.append(
            recorte_renglon
        )
    
    return datos_del_examen[0]

def obtener_datos_de_campos(imagen):
    """ 
    Funcion que devuelve una lista con las imagenes de los campos completados
    """
    campos = imagen[0]
    
    _, umbral = cv2.threshold(campos, 220, 255, cv2.THRESH_BINARY)
    contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    columnas = []

    for c in contornos:
        x, y, w, h = cv2.boundingRect(c) 
        # CChequeo el ancho
        if w > 77:
          # chequeo que la posiscion de x no sea 569 porque coincide con el ancho del campo de codigo
          if x == 569:
            continue
          
          ##### 
          columna_roi = umbral[y:y+h, x:x+w] 

          # Chequeo que sea mayormente blanco
          avg_intensity = np.mean(columna_roi)

          if avg_intensity > 200:
            columnas.append((x, y, w, h))

    # Genero imagenes para pasar como argumento a la otra que analiza el texto: renglones = []
    indv_datos_del_examen=[]
    campos_a_retornar=imagen[0].copy()
    for x, y, w, h in columnas:
      indv_datos_del_examen.append(campos_a_retornar[y+3:y+h-3, x+3:x+w-3]) ## me queda el campo vacio en negro
    return indv_datos_del_examen

def contar_componentes(campos):
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
        if i > 1: # descartar el primero porque corresponde el fondo
          val_espacio = stats[i][0]-(stats[i-1][0]) # calulo la diferencia entre la cordenada x de mi componente siguiente y la anterior
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
      
  


lista_de_examenes=['PDI\multiple_choice_1.png','PDI\multiple_choice_2.png', 'PDI\multiple_choice_3.png', 'PDI\multiple_choice_4.png', 'PDI\multiple_choice_5.png']
ex_id = 0 
for examen in lista_de_examenes:
   print(f"Examen: {ex_id}-{examen}")
   renglon = obtener_renglon_de_datos(examen)
   #plt.figure(), plt.imshow(renglon, cmap='gray'),  plt.show(block=True)
   datos_de_los_campos = obtener_datos_de_campos([renglon])
   componentes = contar_componentes(datos_de_los_campos)
   print(componentes)
   validar_caracteres(componentes)
   ex_id = ex_id + 1
