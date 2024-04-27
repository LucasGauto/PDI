import cv2
import numpy as np
import matplotlib.pyplot as plt
from acciones import funciones

######## Ejercicio 2 ################
#a)
examen = funciones.adecuar('multiple_choice_1.png')
print(funciones.corregir(examen))