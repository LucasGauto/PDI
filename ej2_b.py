import cv2
import numpy as np
import matplotlib.pyplot as plt

# Funcion para obtener el renlgon de datos del examen --> devuelve la iamgen ya recortada





#def plot_image(img, grayscale=True):
#    plt.axis('off')
#    if grayscale:
#        plt.imshow(img, cmap='gray')
#    else:
#        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#    plt.show()

img = cv2.imread('PDI\multiple_choice_4.png', cv2.IMREAD_GRAYSCALE)
umbral, umbralizada = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
img_neg = umbralizada==0  #True -> blanco, False --> negro
y = 140
img_neg = img_neg[:y]
plt.figure(), plt.imshow(img_neg, cmap='gray'), plt.show()

img_row_zeros = img_neg.any(axis=1) # True donde está el renglón
x = np.diff(img_row_zeros) 
renglones_indxs = np.argwhere(x) # me devuelve donde empieza y termina el renglon, me interesa la pos 2 y 3

renglon_de_datos=[renglones_indxs[2], renglones_indxs[3]]
r_datos_idxs = np.reshape(renglon_de_datos, (-1,2))
len(renglones_indxs)


ii = np.arange(0,len(renglon_de_datos),2)    # 0 2 4 ... X --> X es el último nro par antes de len(renglones_indxs)
# renglon_de_datos[ii]+=1 no hace falta porque se trata de un reblgon



img_row_zeros_idxs = np.argwhere(img_neg.any(axis=1))
plt.figure(), plt.plot(img_row_zeros), plt.show()

# Visualizo
xri = np.zeros(img.shape[0])
xri[renglon_de_datos] = (img.shape[1]-1)
yri = np.arange(img.shape[0])            
plt.figure(), plt.imshow(img, cmap='gray'), plt.plot(xri, yri, 'r'), plt.title("Renglones - Inicio y Fin"), plt.show(block=False)

datos_del_examen=[]
# Genero imagen para pasar como argumento a la otra que analiza el texto: renglones = []
for ir, idxs in enumerate(r_datos_idxs):
    recorte_renglon = img[idxs[0]:idxs[1], :] 
    #recorte_renglon_neg = recorte_renglon==0 # ya la agrego acondicionada
    datos_del_examen.append(
        recorte_renglon
    )

plt.figure(), plt.imshow(datos_del_examen[0], cmap='gray'),  plt.show(block=False)

# Creo otra funcion que devuelve una lista con las imagenes de los campos completados


### def devuelve_campos_txt()
campos = datos_del_examen[0]
_, thresh = cv2.threshold(campos, 220, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

white_columns = []

for c in contours:
    x, y, w, h = cv2.boundingRect(c)    #
    print(w, h, x)
    # Check if contour is relatively wide and tall (indicating a column)
    if w > 77:
      if x == 569:
        continue
      # chequeo que
      # Extract column ROI
      column_roi = thresh[y:y+h, x:x+w] 
      # Check if the column is mostly white (average pixel intensity)
      avg_intensity = np.mean(column_roi)
      if avg_intensity > 200:
        white_columns.append((x, y, w, h))

indv_datos_del_examen=[]
# Genero imagen para pasar como argumento a la otra que analiza el texto: renglones = []

campos_a_retornar=datos_del_examen[0].copy()
for x, y, w, h in white_columns:
  cv2.rectangle(campos_a_retornar, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Draw green rectangles around columns
  indv_datos_del_examen.append(campos_a_retornar[y:y+h, x:x+w])

plt.figure(), plt.imshow(campos_a_retornar, cmap='gray'),  plt.show(block=False)



#######
cont=0
for im in indv_datos_del_examen:
   cont+=1
   plt.figure(), plt.imshow(im, cmap='gray'),  plt.show(block=False), plt.title(f'{cont}')
   
1
campos = []
renglon = datos_del_examen[0]

ren_col_zeros = renglon.any(axis=0)
ren_col_zeros_idxs = np.argwhere(renglon.any(axis=1))


# Visualizo
xc = np.arange(renglon.shape[1])
yc = ren_col_zeros*(renglon.shape[0]-1)
plt.figure(), plt.imshow(renglon, cmap='gray'), plt.plot(xc, yc, c='b'), plt.show()        


### TODO
# renombrar datos del examen --> renglon_datos del examen
# funcion para analizar el texto por caracteres
####
####
#2) Con las subimagenes de los campos detectados, una posible forma de obtener
#los caracteres dentro de los mismos, es obteniendo las componentes conectadas
#dentro: cv2.connectedComponentsWithStats(celda_img, 8, cv2.CV_32S).
#Tenga especial cuidado que no hayan quedado pixels de las líneas divisorias de
#la tabla dentro de la celda. Una posible forma de evitar este problema, es eliminar
#las componentes conectadas de área muy chica, definiendo un umbral: ix_area =
#stats[:,-1]>th_area y luego stats = stats[ix_area,:].



## 1 fecha
## 2 id
## 3 codigo
## 4 nombre





# Segmentar los renglones 
# encuentro los unidimensionalmente son igual a 0 indica rectangulo padre






#print(img.shape) 
#plot_image(img)



print(img_grey.shape)

umbral, umbralizada = cv2.threshold(img_grey, 120, 255, cv2.THRESH_BINARY)

contornos, jerarquia = cv2.findContours(umbralizada, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

cv2.drawContours(img, contornos, contourIdx=-1, color=(0, 0, 255), thickness=2)  # https://docs.opencv.org/3.4/d6/d6e/group__imgproc__draw.html#ga746c0625f1781f1ffc9056259103edbc
#plot_image(img)

#canvas = np.zeros_like(img)
#cv2.drawContours(canvas, contornos, -1, (0,255,0), 2)
#area = cv2.contourArea(contornos)

#plt.axis('off')
#plt.imshow(canvas)
#plot_image(canvas)
#plot_image(umbralizada)
