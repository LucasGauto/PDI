"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

#ejercicio 1

img = cv2.imread('imagen_con_detalles_escondidos.tif',cv2.IMREAD_GRAYSCALE)
plt.imshow(img, cmap='gray') 
plt.show()


img_heq = cv2.equalizeHist(img)

plt.imshow(img_heq)
plt.show()

np.histogram(img.flatten(), 256, [0, 256])

plt.hist(img.flatten(), 256, [0, 256])
plt.imshow(img_heq,cmap='gray')
plt.hist(img_heq.flatten(), 256, [0, 256])
plt.show()
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

######## Ejercicio 2

img = cv2.imread('multiple_choice_1.png', cv2.IMREAD_GRAYSCALE)
plt.imshow(img, cmap='gray', vmin=100, vmax=101)
plt.show(block = False)

y = 140
img[img < 150] = 0 #umbralado negro
img[img > 150] = 255 #Umbralado blanco
imgRecortada = img[y:]
plt.imshow(imgRecortada, cmap='gray') #imagen recortada
plt.show()

imgRecortada.shape

#255 * 816 = fila de solo blancos

'''
Como la imagen tiene 916 pixeles en sus columnas
podemos decir que una fila toda blanca tendra una suma
de 255*816. Por lo tanto, si la suma de la fila da un valor
menor a ese numero, podemos decir que ya hay algun valr igual
a 0
'''
#Recortar filas
def sumar_filas(matriz):
    suma_filas = []
    for fila in matriz:
        suma = sum(fila)
        suma_filas.append(suma)
    return suma_filas

sumaFilas = sumar_filas(imgRecortada) #arraay

contador = 1
for i in sumaFilas:
    if i != 255*816:
        print(i, contador)
        break
    contador += 1

plt.imshow(imgRecortada[contador-1:])

#Recortar columnas


imgTraspuesta = imgRecortada.T #trasponemo

sumaColumnas = sumar_filas(imgTraspuesta)

imgRecortada.shape
contador = 1
for i in sumaColumnas:
    if i != 255*916:
        print(i, contador)
        break
    contador += 1

plt.imshow(imgRecortada[:contador])