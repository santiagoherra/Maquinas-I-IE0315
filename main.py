#Esta es el archivo principal del programa donde se ejecutara la interaz grafica con tkinter y
#se uniran las funciones previas que se realizaron.


#librerias y archivos.
import tkinter as tk
import interfaz_datos

# Crear la ventana principal de Tkinter
ventana = tk.Tk()
ventana.title("Formulario de Datos - Circuito Magnético")

# Etiquetas y entradas para cada parámetro con unidades desplegables
labels = [
    "N1 [vueltas]", "N2 [vueltas]", "I1 [A]", "I2 [A]", "Factor Apilado",
    "SL [Área]", "Sc [Área]", "Ancho A [Longitud]", "L1 [Longitud]", "L2 [Longitud]", 
    "L3 [Longitud]", "LE [Longitud]", "Flujo ΦE [Wb]", "Coef. Dispersión", "Deformación Área [%]"
]
entries = {}
unidades = {}

# Añadir los campos de texto y los desplegables para unidades
for i, label in enumerate(labels):
    tk.Label(ventana, text=label).grid(row=i, column=0, padx=5, pady=5)
    entries[label] = tk.Entry(ventana)
    entries[label].grid(row=i, column=1, padx=5, pady=5)
    
    # Agregar un combobox para las unidades en las áreas y longitudes
    if "Área" in label:
        unidades[label] = ttk.Combobox(ventana, values=["m²", "cm²", "mm²"])
        unidades[label].grid(row=i, column=2)
        unidades[label].set("m²")  # Valor por defecto: metros cuadrados
    elif "Longitud" in label:
        unidades[label] = ttk.Combobox(ventana, values=["m", "cm", "mm"])
        unidades[label].grid(row=i, column=2)
        unidades[label].set("m")  # Valor por defecto: metros

# Asignar las entradas a variables
entry_N1 = entries["N1 [vueltas]"]
entry_N2 = entries["N2 [vueltas]"]
entry_I1 = entries["I1 [A]"]
entry_I2 = entries["I2 [A]"]
entry_factor_apilado = entries["Factor Apilado"]
entry_SL = entries["SL [Área]"]
entry_Sc = entries["Sc [Área]"]
entry_A = entries["Ancho A [Longitud]"]
entry_L1 = entries["L1 [Longitud]"]
entry_L2 = entries["L2 [Longitud]"]
entry_L3 = entries["L3 [Longitud]"]
entry_LE = entries["LE [Longitud]"]
entry_flujo_entre = entries["Flujo ΦE [Wb]"]
entry_coef_dispersion = entries["Coef. Dispersión"]
entry_porcentaje_deformacion = entries["Deformación Área [%]"]

# Unidades seleccionadas
unidad_SL = unidades["SL [Área]"]
unidad_Sc = unidades["Sc [Área]"]
unidad_A = unidades["Ancho A [Longitud]"]
unidad_L1 = unidades["L1 [Longitud]"]
unidad_L2 = unidades["L2 [Longitud]"]
unidad_L3 = unidades["L3 [Longitud]"]
unidad_LE = unidades["LE [Longitud]"]

# Botón para enviar los datos
tk.Button(ventana, text="Enviar", command=recoger_datos).grid(row=len(labels), column=0, columnspan=3, pady=10)

# Ejecutar la aplicación
ventana.mainloop()