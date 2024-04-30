import cv2
import numpy as np
import matplotlib.pyplot as plt
from acciones import funciones

######## Ejercicio 1 ##############
imagen = funciones.ecualizacionLocal(ruta = 'Imagen_con_detalles_escondidos.tif',window_size=25)
plt.imshow(imagen)
plt.show()

######## Ejercicio 2 ################
#a)
examen = funciones.adecuar('multiple_choice_1.png')
print(funciones.corregir(examen))

#b)
#Correccion de encabezados
m_choice=['multiple_choice_1.png','multiple_choice_2.png', 'multiple_choice_3.png', 'multiple_choice_4.png', 'multiple_choice_5.png']
resultados_examenes = funciones.main(m_choice)
print(resultados_examenes)

#c)
#Correccion de cada examen
for imagen in m_choice:
    respuesta = funciones.corregir(funciones.adecuar(imagen))
    print(imagen)
    #print(respuesta)
    for punto in respuesta:
        print(punto, respuesta[punto])
    print('\n')
    
#d)
funciones.generar_imagen_salida(resultados_examenes)