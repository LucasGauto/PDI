from tkinter import *
from tkinter import filedialog
from acciones import funciones
from PIL import Image, ImageTk

"""
- Ventana sola con tamño fijo
- Menu (Inicio, ejercicio1, ejercicio2a, etc)
- Distintas pantallas
- Formulario
- Mostrar datos
"""
def seleccionar_archivo():
    global archivo_seleccionado
    archivo_seleccionado = filedialog.askopenfilename()
    return archivo_seleccionado

ventana = Tk()

ventana.geometry('750x450')
ventana.title('TP')
ventana.resizable(0,0)

#Configurar columnas y filas para expandirse
ventana.columnconfigure(0, weight=1)
ventana.rowconfigure(1, weight=1)
#ventana.rowconfigure(0,weight=1) este era para las filas


#Definir campos de pantallas
#Campos Inicio
inicioFrame1 = Frame(ventana)
encabezadoInicio = Label(inicioFrame1, text='Bienvenido al TP del Grupo 6')
integrantes = Label(inicioFrame1, text = 'Integrantes: Gauto, Arce y Rizzotto')
indicacionesInicio = Label(inicioFrame1, text='A continuación, seleccione el ejercicio que desea ejecutar.')

inicioFrame2 = Frame(ventana)
boton1Prueba = Label(inicioFrame2, text='Esto deberia ser un boton dea')
boton2Prueba = Label(inicioFrame2, text='Esto deberia ser un boton dea')

#Campos Ej1
ej1Frame1 = Frame(ventana)
encabezadoEjercicio1 = Label(ej1Frame1, text='Ejercicio 1')

ej1Frame2 = Frame(ventana)
indicacionesEjercicio1 = Label(ej1Frame2, text='A continuación, seleccione la imagen con figuras ocultas.')
botonSeleccionarArchivo = Button(ej1Frame2, text='Examinar', command=seleccionar_archivo)

ej1Frame3 = Frame(ventana)
#imagen_pil = Image.fromarray(archivo_seleccionado)
#render = ImageTk.PhotoImage(imagen_pil)
#imagen = Label(ej1Frame3, image=render)


#Campos Ej2
ej2Frame1 = Frame()
ej2Frame2 = Frame()
ej2Frame3 = Frame()
encabezadoEjercicio2 = Label(ej2Frame1, text='Ejercicio 2')
indicacionesEjercicio2 = Label(ej2Frame2, text='A continaución, seleccione el exámen que desea corregir.')
botonSeleccionarExamen = Button(ej2Frame2, text='Examinar')
respuesta = Label(ej2Frame3, text='Aqui irian las respuestas... SI TAN SOLO LO HUBIERA PROGRAMADO')


#Pantallas
def inicio():
    inicioFrame1.grid(row=0, column=0, sticky='nsew')
    inicioFrame1.columnconfigure(0, weight=1)
    inicioFrame2.grid(row=1, column=0, sticky='nsew')
    inicioFrame2.columnconfigure(0, weight=1)
    inicioFrame2.columnconfigure(1, weight=1)
    inicioFrame2.rowconfigure(0, weight=1)
    #Crear frame para meter los elementos dentro y cambair color fondo
    encabezadoInicio.config(
        bg='lightblue',
        fg='white',
        font=('Calibri',25)
    )
    encabezadoInicio.grid(row=0,column=0, sticky='ew')
    #encabezadoEjercicio1.grid_remove()
    encabezadoEjercicio2.grid_remove()
    ej1Frame1.grid_remove()
    ej1Frame2.grid_remove()
    ej1Frame3.grid_remove()
    ej2Frame1.grid_remove()
    ej2Frame2.grid_remove()
    ej2Frame3.grid_remove()
    #Integrantes
    integrantes.config(font=('Calibri',15))
    integrantes.grid(row=1, column=0, sticky='ew')

    #Indicaciones
    indicacionesInicio.config(font=('Calibri',14), pady=10)
    indicacionesInicio.grid(row=2, column=0, sticky='ew')

    #Boton para Ejercicio1
    boton1Prueba.config(bg='black',fg='white')
    boton1Prueba.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

    boton2Prueba.config(bg='blue')
    boton2Prueba.grid(row=0, column=1, sticky='nsew', padx=20, pady=20)
    #Boton para Ejercicio2

    return True

def ejercicio1():
    #Frames
    ej1Frame1.grid(row=0, column=0, sticky='nsew')
    ej1Frame1.columnconfigure(0, weight=1)

    ej1Frame2.grid(row=1, column=0, sticky='nsew')
    ej1Frame2.columnconfigure(0, weight=1)

    ej1Frame3.grid(row=2, column=0, sticky='nsew')
    ej1Frame3.columnconfigure(0, weight=1)

    encabezadoEjercicio1.config(
        bg='lightblue',
        fg='white',
        font=('Calibri',25)
    )
    encabezadoEjercicio1.grid(row=0,column=0, sticky='ew')

    indicacionesEjercicio1.config(
        font=('Calibri', 15)
    )
    indicacionesEjercicio1.grid(row=0, column=0, sticky='ew')
    botonSeleccionarArchivo.grid(row=1, column=0)
    
    #imagen.grid(row=0, column=0)
    
    inicioFrame1.grid_remove()
    inicioFrame2.grid_remove()
    #encabezadoEjercicio2.grid_remove()
    ej2Frame1.grid_remove()
    ej2Frame2.grid_remove()
    ej2Frame3.grid_remove()
    return True

def ejercicio2():
    #Frames
    ej2Frame1.grid(row=0, column=0, sticky='nsew')
    ej2Frame1.columnconfigure(0, weight=1)
    ej2Frame2.grid(row=1, column=0, sticky='nsew')
    ej2Frame2.columnconfigure(0, weight=1)
    ej2Frame3.grid(row=2, column=0, sticky='nsew')
    ej2Frame3.columnconfigure(0, weight=1)

    encabezadoEjercicio2.config(
        bg='lightblue',
        fg='white',
        font=('Calibri',25)
    )
    encabezadoEjercicio2.grid(row=0,column=0, sticky='ew')

    indicacionesEjercicio2.config(
        font=('Calibri',15)
    )
    indicacionesEjercicio2.grid(row=0, column=0, sticky='ew')

    botonSeleccionarExamen.grid(row=1, column=0)

    respuesta.grid(row=0, column=0, sticky='nsew')

    #Eliminar los otros
    inicioFrame1.grid_remove()
    inicioFrame2.grid_remove()
    ej1Frame1.grid_remove()
    ej1Frame2.grid_remove()
    ej1Frame3.grid_remove()
    
    return True

#Corre el inicio por default
inicio()

#Menu
menu = Menu(ventana)
menu.add_command(label='Inicio', command=inicio)
menu.add_command(label='Ejercicio 1', command=ejercicio1)
menu.add_command(label='Ejercicio 2', command=ejercicio2)
menu.add_command(label='Salir', command=ventana.quit)
ventana.config(menu=menu)


ventana.mainloop()