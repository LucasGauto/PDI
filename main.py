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

# Cargar la imagen
img = cv2.imread('imagen_con_detalles_escondidos.tif', cv2.IMREAD_GRAYSCALE)

# Ecualizar la imagen
img_heq = cv2.equalizeHist(img)
plt.imshow(img_heq, cmap='gray')
# Crear los histogramas
hist_original, bins_original = np.histogram(img.flatten(), 256, [0, 256])
hist_ecualizada, bins_ecualizada = np.histogram(img_heq.flatten(), 256, [0, 256])

# Mostrar los histogramas
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.plot(hist_original, color='b')
plt.title('Histograma de imagen original')
plt.xlabel('Intensidad de píxel')
plt.ylabel('Frecuencia')

plt.subplot(1, 2, 2)
plt.plot(hist_ecualizada, color='r')
plt.title('Histograma de imagen ecualizada')
plt.xlabel('Intensidad de píxel')
plt.ylabel('Frecuencia')

plt.tight_layout()
plt.show()

img.shape


w = np.ones((5, 5), np.float32) / (5*5)
w
img_fil = cv2.filter2D(img, -1, w, borderType=cv2.BORDER_DEFAULT)

plt.imshow(img_fil, cmap='gray')
plt.show()




import cv2
import numpy as np

def local_histogram_equalization(img, window_size):
    h, w = img.shape
    img_equalized = np.zeros((h, w), dtype=np.uint8)
    half_size = window_size // 2

    for i in range(h):
        for j in range(w):
            i_min = max(0, i - half_size)
            i_max = min(h, i + half_size + 1)
            j_min = max(0, j - half_size)
            j_max = min(w, j + half_size + 1)

            # Obtener la subimagen dentro de la ventana
            window = img[i_min:i_max, j_min:j_max]

            # Ecualizar el histograma localmente
            window_equalized = cv2.equalizeHist(window)

            # Asignar el valor ecualizado al píxel central de la ventana en la imagen resultante
            img_equalized[i, j] = window_equalized[i - i_min, j - j_min]

    return img_equalized

# Cargar la imagen
img = cv2.imread('imagen_con_detalles_escondidos.tif', cv2.IMREAD_GRAYSCALE)

# Tamaño de la ventana de procesamiento (puede ajustarse según sea necesario)
window_size = 25

# Aplicar la ecualización local del histograma
img_local_equalized = local_histogram_equalization(img, window_size)

# Mostrar la imagen original y la imagen procesada
cv2.imshow('Imagen Original', img)
cv2.imshow('Imagen con Ecualización Local del Histograma', img_local_equalized)
cv2.waitKey(0)
cv2.destroyAllWindows()



###################

import cv2
import numpy as np

def local_histogram_equalization_with_border(img, window_size):
    h, w = img.shape
    img_equalized = np.zeros((h, w), dtype=np.uint8)
    half_size = window_size // 2

    # Agregar un borde a la imagen para evitar problemas en los bordes
    img_with_border = cv2.copyMakeBorder(img, half_size, half_size, half_size, half_size, cv2.BORDER_REPLICATE)

    for i in range(h):
        for j in range(w):
            # Definir la región de interés (ROI) en la imagen con borde
            roi = img_with_border[i:i + window_size, j:j + window_size]

            # Ecualizar el histograma localmente
            roi_equalized = cv2.equalizeHist(roi)

            # Asignar el valor ecualizado al píxel central de la ventana en la imagen resultante
            img_equalized[i, j] = roi_equalized[half_size, half_size]

    return img_equalized

# Cargar la imagen
img = cv2.imread('imagen_con_detalles_escondidos.tif', cv2.IMREAD_GRAYSCALE)

# Tamaño de la ventana de procesamiento (puede ajustarse según sea necesario)
window_size = 20

# Aplicar la ecualización local del histograma con borde
img_local_equalized_with_border = local_histogram_equalization_with_border(img, window_size)

# Mostrar la imagen original y la imagen procesada
plt.imshow(img)
plt.imshow(img_local_equalized_with_border, cmap='gray')
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()


######## Ejercicio 2
w

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