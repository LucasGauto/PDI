import cv2
import numpy as np
import matplotlib.pyplot as plt
from acciones.funciones import *


def main(multiple_choice):
  '''Función para retornar el nombre del exámen y el número de respuestas correctas'''
  lista_de_examenes = multiple_choice
  resultados = []  # Lista para almacenar los resultados de los exámenes
  ex_id = 0

  for examen in lista_de_examenes:
     print(f"Examen: {ex_id}-{examen}")
     renglon = obtener_renglon_de_datos(examen)
     #plt.figure(), plt.imshow(renglon, cmap='gray'),  plt.show(block=True)
     datos_de_los_campos = obtener_datos_de_campos(renglon)
     #plt.figure(), plt.imshow(datos_de_los_campos[0], cmap='gray'),  plt.show(block=True)
     componentes = contar_componentes(datos_de_los_campos)
     #print(componentes)
     validar_caracteres(componentes)

     # Calcular el número de respuestas correctas
     correccion_exam = corregir(examen)
     respuestas_correctas = sum(1 for estado in correccion_exam.values() if estado == 'OK')
     resultados.append((examen, respuestas_correctas))
     
     ex_id += 1

  return resultados

m_choice=['multiple_choice_1.png','multiple_choice_2.png', 'multiple_choice_3.png', 'multiple_choice_4.png', 'multiple_choice_5.png']
resultados = main(m_choice)

generar_imagen_salida(resultados)