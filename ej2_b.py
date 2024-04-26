import cv2
import numpy as np
import matplotlib.pyplot as plt

def plot_image(img, grayscale=True):
    plt.axis('off')
    if grayscale:
        plt.imshow(img, cmap='gray')
    else:
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()

img = cv2.imread(f'multiple_choice_1.png')
y = 140
img = img[:y]
#print(img.shape) 
#plot_image(img)

img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(img_grey.shape)

umbralizada = cv2.threshold(img_grey, 120, 255, cv2.THRESH_BINARY_INV)[1]

contornos = cv2.findContours(umbralizada, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

canvas = np.zeros_like(img)
cv2.drawContours(canvas, contornos, -1, (0,255,0), 2)
area = cv2.contourArea(contornos)

plt.axis('off')
plt.imshow(canvas)
plot_image(canvas)
#plot_image(umbralizada)
