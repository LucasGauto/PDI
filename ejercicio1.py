import cv2
import numpy as np
import matplotlib.pyplot as plt

'''
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
plt.show(block=False)

cv2.waitKey(0)
cv2.destroyAllWindows()
'''

#plt.style.use('default')
plt.style.use('dark_background')

#Primero realizamos una carga y visualización de la imagen
imagen = cv2.imread('Imagen_con_detalles_escondidos.tif', cv2.IMREAD_GRAYSCALE)
plt.imshow(imagen, cmap='gray')
plt.show()

#Realizamos una prueba de ecualización de histograma de la imagen
imagen_ecualizada= cv2.equalizeHist(imagen)
plt.imshow(imagen_ecualizada, cmap='gray', vmin = 0, vmax=255)
plt.show()

#Histograma de la imagen
fig, ax = plt.subplots(1,2,figsize=(12,6))

ax[0].hist(imagen.flatten(), 256, [0, 256])
ax[0].set_title("Histograma original")
ax[1].hist(imagen_ecualizada.flatten(), 256, [0,256])
ax[1].set_title("Histograma ecualizado")
plt.show()

#Imagenes con sus respectivos histogramas

ax1 = plt.subplot(221)
plt.imshow(imagen, cmap='gray', vmin=0, vmax=255)
plt.title('Imagen Original')

ax2 = plt.subplot(222)
plt.hist(imagen.flatten(), 255, [0,255])
plt.title('Histograma')

plt.subplot(223, sharex = ax1, sharey = ax1)
plt.imshow(imagen_ecualizada, cmap='gray', vmin=0, vmax=255)
plt.title('Imagen Ecualizada')

plt.subplot(224, sharex=ax2, sharey=ax2)
plt.hist(imagen_ecualizada.flatten(), 255, [0,255])
plt.title('Histograma Ecualizado')

plt.show()

#Dimensiones de la imagen
imagen[:20].shape

#Ecualizacion de fragmento de la imagen
fragmento = cv2.equalizeHist(imagen[:30,:30])
plt.imshow(fragmento, cmap='gray')
plt.show()

#Funcion para ecualizar localmente

def local_histogram_equalization(img, window_size):
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

window_size = 25

imagen_ecualizada_localmente = local_histogram_equalization(imagen, window_size)

plt.imshow(imagen_ecualizada_localmente, cmap = 'gray')
plt.show(block=False)