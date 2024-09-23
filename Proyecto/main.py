# Esta es el archivo principal del programa donde se ejecutará la interfaz gráfica con tkinter 
# y se unirán las funciones previas que se realizaron.

# Librerías y archivos
import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage

#Archivos utilizados
from interfaz_datos import recoger_datos, obtener_curva_hb_gui, generar_ecuacion_bh
from circuitomagnetico import solucion


# Crear la ventana principal de Tkinter
ventana = tk.Tk()
ventana.title("Formulario de Datos - Circuito Magnético")

funcion_H_B = None

# Función para crear una entrada con un combobox para la unidad
def crear_entrada(label, fila, tipo_unidad=None):
    tk.Label(ventana, text=label).grid(row=fila, column=0, padx=5, pady=5)
    entry = tk.Entry(ventana)
    entry.grid(row=fila, column=1, padx=5, pady=5)
    if tipo_unidad:
        combobox = ttk.Combobox(ventana, values=tipo_unidad)
        combobox.grid(row=fila, column=2)
        combobox.set(tipo_unidad[0])  # Seleccionar por defecto la primera unidad
        return entry, combobox
    return entry, None

# Crear las entradas y comboboxes
entry_N1, _ = crear_entrada("N1 [vueltas]", 0)
entry_N2, _ = crear_entrada("N2 [vueltas]", 1)
entry_I1, _ = crear_entrada("I1 [A]", 2)
entry_I2, _ = crear_entrada("I2 [A]", 3)
entry_factor_apilado, _ = crear_entrada("Factor Apilado", 4)
entry_SL, unidad_SL = crear_entrada("SL [Área]", 5, ["m²", "cm²", "mm²"])
entry_Sc, unidad_Sc = crear_entrada("Sc [Área]", 6, ["m²", "cm²", "mm²"])
entry_A, unidad_A = crear_entrada("Ancho A [Longitud]", 7, ["m", "cm", "mm"])
entry_L1, unidad_L1 = crear_entrada("L1 [Longitud]", 8, ["m", "cm", "mm"])
entry_L2, unidad_L2 = crear_entrada("L2 [Longitud]", 9, ["m", "cm", "mm"])
entry_L3, unidad_L3 = crear_entrada("L3 [Longitud]", 10, ["m", "cm", "mm"])
entry_LE, unidad_LE = crear_entrada("LE [Longitud]", 11, ["m", "cm", "mm"])
entry_flujo_entre, _ = crear_entrada("Flujo ΦE [Wb]", 12)
entry_coef_dispersion, _ = crear_entrada("Coef. Dispersión", 13)
entry_porcentaje_deformacion, _ = crear_entrada("Deformación Área [%]", 14)

#Agregando la imagen del circuito a la ventana principal para que se visualice el circuito
imagen_circuito = PhotoImage(file="Proyecto/figura_circuito.png")
label_imagen_circuito = tk.Label(ventana, image=imagen_circuito)
label_imagen_circuito.grid(row=0, column=4, rowspan=15, padx=20, pady=20, sticky='n')

# Función para procesar los datos
def procesar_datos():
    global funcion_H_B  # Necesitamos acceder a la variable global
    
    # Verificar si funcion_H_B está definida
    if not funcion_H_B:
        messagebox.showerror("Error", "La función B-H no está definida.")
        return

    # Recolectar los datos
    valores_magnitudes_electricas, valores_dimensiones = recoger_datos(
        entry_N1, entry_N2, entry_I1, entry_I2, entry_factor_apilado, entry_SL,
        entry_Sc, entry_A, entry_L1, entry_L2, entry_L3, entry_LE,
        entry_flujo_entre, entry_coef_dispersion, entry_porcentaje_deformacion,
        unidad_SL, unidad_Sc, unidad_A, unidad_L1, unidad_L2, unidad_L3, unidad_LE
    )
    
    # Asegurarse que no haya errores en los datos antes de continuar
    if valores_magnitudes_electricas and valores_dimensiones and funcion_H_B:
        # Llamar a la función de solución del circuito magnético
        resultado = solucion(valores_magnitudes_electricas, valores_dimensiones)
        
        # Mostrar los resultados en pantalla
        messagebox.showinfo("Resultado", f"Solución del circuito magnético: {resultado}")

# Función para obtener la ecuación B-H y asignarla a la variable global
def obtener_ecuacion_bh():
    global funcion_H_B
    funcion_H_B = obtener_curva_hb_gui(ventana)  # Asegúrate de que esto devuelva la ecuación correctamente

    #if funcion_H_B:
        #messagebox.showinfo("Éxito", "Ecuación B-H generada correctamente.")
    #else:
        #messagebox.showerror("Error", "No se pudo generar la ecuación B-H.")

# Botón para enviar los datos
tk.Button(ventana, text="Enviar", command=procesar_datos).grid(row=15, column=0, columnspan=3, pady=10)

# Botón para abrir la ventana de Curva H-B y obtener la ecuación B-H
tk.Button(ventana, text="Ingresar Curva H-B", command=obtener_ecuacion_bh).grid(row=16, column=0, columnspan=3, pady=10)

# Ejecutar la aplicación
ventana.mainloop()