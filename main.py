# Esta es el archivo principal del programa donde se ejecutará la interfaz gráfica con tkinter 
# y se unirán las funciones previas que se realizaron.

# Librerías y archivos
import tkinter as tk
from tkinter import ttk
from Proyecto.interfaz_datos import recoger_datos, obtener_curva_hb_gui
# Crear la ventana principal de Tkinter
ventana = tk.Tk()
ventana.title("Formulario de Datos - Circuito Magnético")

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

# Botón para enviar los datos, pasando las entradas y unidades a la función recoger_datos
tk.Button(ventana, text="Enviar", command=lambda: recoger_datos(
    entry_N1, entry_N2, entry_I1, entry_I2, entry_factor_apilado, entry_SL,
    entry_Sc, entry_A, entry_L1, entry_L2, entry_L3, entry_LE,
    entry_flujo_entre, entry_coef_dispersion, entry_porcentaje_deformacion,
    unidad_SL, unidad_Sc, unidad_A, unidad_L1, unidad_L2, unidad_L3, unidad_LE
)).grid(row=15, column=0, columnspan=3, pady=10)

# Botón para abrir la ventana de Curva H-B
tk.Button(ventana, text="Ingresar Curva H-B", command=lambda: obtener_curva_hb_gui(ventana)).grid(row=16, column=0, columnspan=3, pady=10)



# Ejecutar la aplicación
ventana.mainloop()
