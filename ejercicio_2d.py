import cv2
import numpy as np
import matplotlib.pyplot as plt
from ej2_b import obtener_renglon_de_datos, obtener_datos_de_campos

# Funcion que devuelve los crop de los campos name
def obtener_campo_nombre(examen):
    renglon = obtener_renglon_de_datos(examen)
    # Como sé que el ultimo campo en el nombre, me quedo con ese
    campos = obtener_datos_de_campos(renglon)
    name = campos[3]
    #plt.figure(), plt.imshow(renglon, cmap='gray'),  plt.show(block=True)
    return name



