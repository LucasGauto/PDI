from tkinter import *
import os.path #para rutas

class Programa:

    def __init__(self):
        self.title = "Corrector de examenes"
        self.icon = './imagenes/corregido.ico'
        self.icon_alternativo = './InterfazUsuario/imagenes/corregido.ico'
        self.size = "750x450"
        self.resizable = False

    def cargar(self):
        #Ventana raiz
        ventana = Tk()
        self.ventana = ventana
        ventana.geometry(self.size)
        
        if self.resizable == False:
            ventana.resizable(1,1)
        else:
            ventana.resizable(0,0)


        #Comprobar si existe un archivo
        ruta_icono = os.path.abspath(self.icon)

        if not os.path.isfile(ruta_icono):
            ruta_icono = os.path.abspath(self.icon_alternativo)

        #Icono para la ventana
        ventana.iconbitmap(ruta_icono)


        #texto = Label(ventana, text=ruta_icono)
        #texto.pack()

        #Nombre ventana
        ventana.title(self.title)

    def adddEncabezado(self, texto, tamanio):
        texto=Label(self.ventana, text = texto)
        texto.config(
            fg = 'white',
            bg = 'blue',
            font = ('Calibri',tamanio)
        )
        texto.pack(side = TOP, fill=X)

    def adddTexto(self, texto, tamanio):
        texto=Label(self.ventana, text = texto)
        texto.config(
            font=("Calibri", tamanio)
        )
        texto.pack()

    def mostrar(self):
        # Arrancar y mostrar ventana
        self.ventana.mainloop()

#Instanciar programa
programa = Programa()
programa.cargar()
programa.adddEncabezado('Bienvenido a nuestro programa!', 24)
programa.adddTexto('Somos el grupo 6 >:)', 14)
programa.adddTexto('Integrantes: Gauto, Arce y Rizzotto',11)
programa.mostrar()