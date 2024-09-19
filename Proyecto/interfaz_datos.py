import tkinter as tk
from tkinter import messagebox, ttk

# Función para validar cada campo de entrada
def validar_entrada(entry, campo_nombre, condicion=None):
    try:
        valor = float(entry.get().strip())  # Eliminar espacios en blanco
        if condicion and not condicion(valor):
            raise ValueError
        return valor
    except ValueError:
        messagebox.showerror("Error", f"Valor no válido o fuera de rango en el campo: {campo_nombre}")
        return None

# Función para convertir unidades (longitud o área)
def convertir_a_unidades(valor, unidad, tipo):
    if tipo == 'longitud':
        if unidad == "cm":
            return valor / 100
        elif unidad == "mm":
            return valor / 1000
    elif tipo == 'area':
        if unidad == "cm²":
            return valor / 10000
        elif unidad == "mm²":
            return valor / 1000000
    return valor

# Función para entradas opcionales
def validar_opcional(entry, campo_nombre):
    return validar_entrada(entry, campo_nombre) if entry.get() else None

# Función para recoger datos y validar los campos de entrada
def recoger_datos(entry_N1, entry_N2, entry_I1, entry_I2, entry_factor_apilado, 
                  entry_SL, entry_Sc, entry_A, entry_L1, entry_L2, entry_L3, entry_LE,
                  entry_flujo_entre, entry_coef_dispersion, entry_porcentaje_deformacion,
                  unidad_SL, unidad_Sc, unidad_A, unidad_L1, unidad_L2, unidad_L3, unidad_LE):
    
    N1 = validar_entrada(entry_N1, "N1 [vueltas]")
    N2 = validar_entrada(entry_N2, "N2 [vueltas]")
    I1 = validar_opcional(entry_I1, "I1 [A]")
    I2 = validar_opcional(entry_I2, "I2 [A]")
    factor_apilado = validar_entrada(entry_factor_apilado, "Factor Apilado", lambda x: 0 < x < 1)
    
    SL = convertir_a_unidades(validar_entrada(entry_SL, "Área SL"), unidad_SL.get(), 'area')
    Sc = convertir_a_unidades(validar_entrada(entry_Sc, "Área Sc"), unidad_Sc.get(), 'area')
    
    A = convertir_a_unidades(validar_entrada(entry_A, "Ancho A"), unidad_A.get(), 'longitud')
    L1 = convertir_a_unidades(validar_entrada(entry_L1, "Longitud L1"), unidad_L1.get(), 'longitud')
    L2 = convertir_a_unidades(validar_entrada(entry_L2, "Longitud L2"), unidad_L2.get(), 'longitud')
    L3 = convertir_a_unidades(validar_entrada(entry_L3, "Altura L3"), unidad_L3.get(), 'longitud')
    LE = convertir_a_unidades(validar_entrada(entry_LE, "Longitud LE"), unidad_LE.get(), 'longitud')
    
    flujo_entre = validar_entrada(entry_flujo_entre, "Flujo ΦE [Wb]")
    coeficiente_dispersion = validar_opcional(entry_coef_dispersion, "Coef. Dispersión")
    porcentaje_deformacion = validar_opcional(entry_porcentaje_deformacion, "Deformación Área [%]")

    if None in [N1, N2, factor_apilado, SL, Sc, A, L1, L2, L3, LE, flujo_entre]:
        messagebox.showerror("Error", "Por favor corrija los errores antes de continuar.")
        return

    # Guardar los valores obtenidos en listas
    valores_magnitudes_electricas = [N1, N2, I1, I2]
    valores_dimensiones = [L1, L2, L3, LE, Sc, SL, A]
    otros_valores = [flujo_entre, coeficiente_dispersion, porcentaje_deformacion, factor_apilado]
    
    # Imprimir para verificar
    print("Magnitudes Eléctricas:", valores_magnitudes_electricas)
    print("Dimensiones:", valores_dimensiones)
    print("Otros Valores:", otros_valores)

    messagebox.showinfo("Datos recogidos", f"Datos recogidos correctamente")


# Función para obtener la curva H-B a través de la interfaz gráfica
def obtener_curva_hb_gui(parent_ventana):
    ventana_hb = tk.Toplevel(parent_ventana)  # Usar ventana padre
    ventana_hb.title("Curva H-B")
    
    def seleccionar_opcion():
        opcion = hb_opcion.get()
        if opcion == "tabla":
            label_tabla.pack(side="top", fill="x")
            entry_tabla.pack(side="top", fill="x")
            label_ecuacion.pack_forget()
            entry_ecuacion.pack_forget()
        elif opcion == "ecuacion":
            label_ecuacion.pack(side="top", fill="x")
            entry_ecuacion.pack(side="top", fill="x")
            label_tabla.pack_forget()
            entry_tabla.pack_forget()

    hb_opcion = tk.StringVar(value="tabla")
    tk.Radiobutton(ventana_hb, text="Tabla de datos", variable=hb_opcion, value="tabla", command=seleccionar_opcion).pack()
    tk.Radiobutton(ventana_hb, text="Ecuación", variable=hb_opcion, value="ecuacion", command=seleccionar_opcion).pack()

    label_tabla = tk.Label(ventana_hb, text="Ingrese los puntos H-B (Ejemplo: H1,B1; H2,B2...)")
    entry_tabla = tk.Entry(ventana_hb)

    label_ecuacion = tk.Label(ventana_hb, text="Ingrese la ecuación para H-B (Ejemplo: B = m * H + c)")
    entry_ecuacion = tk.Entry(ventana_hb)

    tk.Button(ventana_hb, text="Aceptar", command=lambda: print("Opción seleccionada:", hb_opcion.get())).pack()
