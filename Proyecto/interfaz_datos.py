import tkinter as tk
from tkinter import messagebox, ttk

# Función para validar cada campo de entrada
def validar_entrada(entry, campo_nombre, condicion=None):
    try:
        valor = float(entry.get())
        if condicion and not condicion(valor):
            raise ValueError
        return valor
    except ValueError:
        messagebox.showerror("Error", f"Valor no válido o fuera de rango en el campo: {campo_nombre}")
        return None

# Función para convertir la longitud a metros
def convertir_a_metros(valor, unidad):
    if unidad == "cm":
        return valor / 100  # Convertir cm a metros
    elif unidad == "mm":
        return valor / 1000  # Convertir mm a metros
    return valor  # Ya está en metros

# Función para convertir el área a metros cuadrados
def convertir_a_metros_cuadrados(valor, unidad):
    if unidad == "cm²":
        return valor / 10000  # Convertir cm² a metros² (1 cm² = 0.0001 m²)
    elif unidad == "mm²":
        return valor / 1000000  # Convertir mm² a metros² (1 mm² = 0.000001 m²)
    return valor  # Ya está en metros cuadrados

def recoger_datos():
    # Recoger datos con validación y conversión de unidades
    N1 = validar_entrada(entry_N1, "N1 [vueltas]")
    N2 = validar_entrada(entry_N2, "N2 [vueltas]")
    I1 = validar_entrada(entry_I1, "I1 [A]") if entry_I1.get() else None
    I2 = validar_entrada(entry_I2, "I2 [A]") if entry_I2.get() else None
    
    # Validación específica del factor de apilado (debe estar entre 0 y 1)
    factor_apilado = validar_entrada(entry_factor_apilado, "Factor Apilado", lambda x: 0 <= x <= 1)
    
    # Convertir áreas a metros cuadrados
    SL = convertir_a_metros_cuadrados(validar_entrada(entry_SL, "Área SL"), unidad_SL.get())
    Sc = convertir_a_metros_cuadrados(validar_entrada(entry_Sc, "Área Sc"), unidad_Sc.get())
    
    # Convertir longitudes a metros
    A = convertir_a_metros(validar_entrada(entry_A, "Ancho A"), unidad_A.get())
    L1 = convertir_a_metros(validar_entrada(entry_L1, "Longitud L1"), unidad_L1.get())
    L2 = convertir_a_metros(validar_entrada(entry_L2, "Longitud L2"), unidad_L2.get())
    L3 = convertir_a_metros(validar_entrada(entry_L3, "Altura L3"), unidad_L3.get())
    LE = convertir_a_metros(validar_entrada(entry_LE, "Longitud LE"), unidad_LE.get())
    
    flujo_entre = validar_entrada(entry_flujo_entre, "Flujo ΦE [Wb]")
    coeficiente_dispersion = validar_entrada(entry_coef_dispersion, "Coef. Dispersión") if entry_coef_dispersion.get() else None
    porcentaje_deformacion = validar_entrada(entry_porcentaje_deformacion, "Deformación Área [%]") if entry_porcentaje_deformacion.get() else None

    # Si alguna validación falla, no continuar
    if None in [N1, N2, factor_apilado, SL, Sc, A, L1, L2, L3, LE, flujo_entre]:
        messagebox.showerror("Error", "Por favor corrija los errores antes de continuar.")
        return

    # Si todo está bien, se imprimen los datos
    datos = {
        'N1': N1, 'N2': N2, 'I1': I1, 'I2': I2, 
        'factor_apilado': factor_apilado, 'SL': SL, 'Sc': Sc,
        'A': A, 'L1': L1, 'L2': L2, 'L3': L3, 'LE': LE,
        'flujo_entre': flujo_entre,
        'coeficiente_dispersion': coeficiente_dispersion,
        'porcentaje_deformacion': porcentaje_deformacion
    }
    
    print("Datos ingresados:", datos)
    messagebox.showinfo("Datos recogidos", f"Datos recogidos correctamente: {datos}")

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

