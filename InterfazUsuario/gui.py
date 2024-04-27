import tkinter as tk
from tkinter import filedialog
import os
from acciones.funciones import adecuar, corregir

# Funciones de ejemplo para procesar los archivos seleccionados
def procesar_archivo_1(nombre_archivo):
    # Aquí iría el código de la primera función de procesamiento
    return {"Archivo 1": nombre_archivo.upper()}

def procesar_archivo_2(nombre_archivo):
    # Aquí iría el código de la segunda función de procesamiento
    return {"Archivo 2": nombre_archivo.lower()}

# Función para manejar la selección de archivos
def seleccionar_archivos():
    archivos = filedialog.askopenfilenames(
        initialdir="/",  # Directorio inicial
        title="Seleccionar archivos",  # Título del diálogo
        filetypes=(("Archivos PNG", "*.png"), ("Todos los archivos", "*.*"))  # Tipos de archivo permitidos
    )
    return archivos

# Función para corregir los archivos seleccionados
def corregir_archivos():
    archivos_seleccionados = seleccionar_archivos()

    resultado = {}
    for archivo in archivos_seleccionados:
        nombre_archivo = os.path.basename(archivo)
        resultado.update(corregir(adecuar(nombre_archivo)))
        #resultado.update(procesar_archivo_2(nombre_archivo))

    mostrar_resultado(resultado)

# Función para mostrar el resultado en una nueva ventana
def mostrar_resultado(resultado):
    resultado_window = tk.Toplevel(root)
    resultado_window.title("Resultado")

    for key, value in resultado.items():
        tk.Label(resultado_window, text=f"{key}: {value}").pack()

# Crear la ventana principal
root = tk.Tk()
root.title("Aplicación de Corrección")

# Botón para corregir los archivos
boton_corregir = tk.Button(root, text="Corregir", command=corregir_archivos)
boton_corregir.pack()

# Ejecutar el bucle principal de la aplicación
root.mainloop()
