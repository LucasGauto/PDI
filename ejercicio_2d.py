import cv2
import numpy as np
import matplotlib.pyplot as plt
from ej2_b import obtener_renglon_de_datos, obtener_datos_de_campos, main

def obtener_campo_nombre(examen):
    '''Función que evuelve los crop de los campos name'''
    renglon = obtener_renglon_de_datos(examen)
    # Como sé que el ultimo campo es el nombre, me quedo con ese
    name = obtener_datos_de_campos(renglon)[3]
    #plt.figure(), plt.imshow(renglon, cmap='gray'),  plt.show(block=True)
    return name

def generar_imagen_salida(resultados):
    '''Función para generar la imágen de salida'''
    # Crear una imagen en blanco para la salida
    height = len(resultados) * 60
    width = 600
    #output_image = np.ones((height, width, 3), np.uint8) * 255
    output_image = np.ones((height, width), np.uint8) * 255

    # Iterar sobre los resultados y generar los crops de los campos Name
    y = 20
    for examen, respuestas_correctas in resultados:
        # Obtener el campo Name del examen
        campo_name = obtener_campo_nombre(examen)
        h, w = campo_name.shape[:2]
        # Dibujar el crop del campo Name en la imagen de salida
        output_image[y:y+h, :w] = campo_name
        # Escribir el nombre del examen y el número de respuestas correctas
        if respuestas_correctas >= 20:
            text = f"Examen {examen}: APROBADO"
        else:
            text = f"Examen {examen}: DESAPROBADO"
        cv2.putText(output_image, text, (w + 10, y + h // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        y += h + 10

    # Guardar la imagen de salida
    cv2.imwrite('output_image.png', output_image)
    plt.imshow(output_image)
    plt.axis('off')
    plt.show()

# Obtener los resultados de los exámenes
resultados_examenes = main(['multiple_choice_1.png','multiple_choice_2.png', 'multiple_choice_3.png', 'multiple_choice_4.png', 'multiple_choice_5.png'])

# Generar la imagen de salida
generar_imagen_salida(resultados_examenes)