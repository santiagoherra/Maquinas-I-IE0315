import tkinter as tk
from tkinter import messagebox, ttk
import re
import numpy as np
from scipy.optimize import curve_fit

# Función para convertir unidades (longitud o área)
def convertir_a_unidades(valor, unidad, tipo):
    conversiones = {
        'longitud': {'cm': 100, 'mm': 1000},
        'area': {'cm²': 10000, 'mm²': 1000000}
    }
    if unidad in conversiones[tipo]:
        return valor / conversiones[tipo][unidad]
    return valor

# Función para recoger datos y validar los campos de entrada
def recoger_datos(entry_N1, entry_N2, entry_I1, entry_I2, entry_factor_apilado, 
                  entry_SL, entry_Sc, entry_A, entry_L1, entry_L2, entry_L3, entry_LE,
                  entry_flujo_entre, entry_coef_dispersion, entry_porcentaje_deformacion,
                  unidad_SL, unidad_Sc, unidad_A, unidad_L1, unidad_L2, unidad_L3, unidad_LE):
    
    # Validaciones: no permitir negativos excepto en corrientes
    N1 = validar_entrada(entry_N1, "N1 [vueltas]", permitir_negativo=False)
    print(f"Validación de N1: {N1}")
    N2 = validar_entrada(entry_N2, "N2 [vueltas]", permitir_negativo=False)
    print(f"Validación de N2: {N2}")
    
    I1 = validar_entrada(entry_I1, "I1 [A]", permitir_negativo=True) if entry_I1.get() else None
    print(f"Validación de I1: {I1}")
    I2 = validar_entrada(entry_I2, "I2 [A]", permitir_negativo=True) if entry_I2.get() else None
    print(f"Validación de I2: {I2}")
    
    factor_apilado = validar_entrada(entry_factor_apilado, "Factor Apilado", permitir_negativo=False, condicion=lambda x: 0 < x < 1)
    print(f"Validación de factor_apilado: {factor_apilado}")
    
    # Validación de áreas y longitudes (no se permiten negativos)
    SL = convertir_a_unidades(validar_entrada(entry_SL, "Área SL", permitir_negativo=False), unidad_SL.get(), 'area')
    print(f"Validación de SL: {SL}")
    Sc = convertir_a_unidades(validar_entrada(entry_Sc, "Área Sc", permitir_negativo=False), unidad_Sc.get(), 'area')
    print(f"Validación de Sc: {Sc}")
    
    A = convertir_a_unidades(validar_entrada(entry_A, "Ancho A", permitir_negativo=False), unidad_A.get(), 'longitud')
    print(f"Validación de A: {A}")
    L1 = convertir_a_unidades(validar_entrada(entry_L1, "Longitud L1", permitir_negativo=False), unidad_L1.get(), 'longitud')
    print(f"Validación de L1: {L1}")
    L2 = convertir_a_unidades(validar_entrada(entry_L2, "Longitud L2", permitir_negativo=False), unidad_L2.get(), 'longitud')
    print(f"Validación de L2: {L2}")
    L3 = convertir_a_unidades(validar_entrada(entry_L3, "Altura L3", permitir_negativo=False), unidad_L3.get(), 'longitud')
    print(f"Validación de L3: {L3}")
    LE = convertir_a_unidades(validar_entrada(entry_LE, "Longitud LE", permitir_negativo=False), unidad_LE.get(), 'longitud')
    print(f"Validación de LE: {LE}")
    
    flujo_entre = validar_entrada(entry_flujo_entre, "Flujo ΦE [Wb]", permitir_negativo=False)
    print(f"Validación de flujo_entre: {flujo_entre}")
    
    coeficiente_dispersion = validar_entrada(entry_coef_dispersion, "Coef. Dispersión", permitir_negativo=False) if entry_coef_dispersion.get() else None
    print(f"Validación de coeficiente_dispersion: {coeficiente_dispersion}")
    porcentaje_deformacion = validar_entrada(entry_porcentaje_deformacion, "Deformación Área [%]", permitir_negativo=False) if entry_porcentaje_deformacion.get() else None
    print(f"Validación de porcentaje_deformacion: {porcentaje_deformacion}")

    # Verificar si algún campo contiene un valor no válido
    if None in [N1, N2, factor_apilado, SL, Sc, A, L1, L2, L3, LE, flujo_entre]:
        print("Error: Uno o más valores no son válidos.")
        messagebox.showerror("Error", "Por favor corrija los errores antes de continuar.")
        return None  # Retornar None explícitamente en caso de error

    # Guardar los valores obtenidos en listas
    valores_magnitudes_electricas = [N1, N2, I1, I2, flujo_entre, coeficiente_dispersion, porcentaje_deformacion, factor_apilado]
    valores_dimensiones = [L1, L2, L3, LE, Sc, SL, A]
    
    # Imprimir para verificar
    print("Magnitudes Eléctricas:", valores_magnitudes_electricas)
    print("Dimensiones:", valores_dimensiones)

    messagebox.showinfo("Datos recogidos", "Datos recogidos correctamente")
    
    # Devolver los valores como una tupla
    return valores_magnitudes_electricas, valores_dimensiones

# Función para procesar los datos de la tabla y convertirlos en listas de H y B
def procesar_datos_tabla(texto_tabla):
    pares_hb = texto_tabla.split(";")
    H_values = []
    B_values = []

    for par in pares_hb:
        if par.strip():
            H, B = map(float, par.split(","))
            H_values.append(H)
            B_values.append(B)

    print("Valores H:", H_values)
    print("Valores B:", B_values)

    return H_values, B_values

# Generar ecuación B(H) ajustada a los datos
def generar_ecuacion_bh(H_values, B_values):
    # Verificar que hay suficientes datos
    if len(H_values) < 2 or len(B_values) < 2:
        messagebox.showerror("Error", "Se requieren al menos dos pares de valores H y B para ajustar la curva.")
        return None, None

    try:
        # Estimar los valores iniciales (p0)
        p0 = [max(B_values), max(H_values) / 2]

        # Ajuste no lineal con la función B(H) = a * H / (b + H)
        popt, _ = curve_fit(funcion_bh, H_values, B_values, p0=p0)
        a, b = popt
        
        # Crear la cadena de la ecuación
        ecuacion_str = f"{a:.4f} * H / ({b:.4f} + H)"
        
        # Mostrar la función B(H)
        print(f"La función B(H) ajustada es: {ecuacion_str}")
        messagebox.showinfo("Ecuación B(H)", f"La ecuación B(H) es: {ecuacion_str}")
        
        # Devolver los valores de a y b
        return a, b
    
    except (RuntimeError, ValueError) as e:
        messagebox.showerror("Error", f"No se pudo ajustar la curva: {str(e)}. Por favor, verifica los datos ingresados.")
        return None, None

# Función para validar el formato de la tabla
def validar_formato_tabla(texto):
    texto = texto.strip()
    if texto.endswith(";"):
        texto = texto[:-1].strip()

    patron = r'^\d+(\.\d+)?\s*,\s*\d+(\.\d+)?\s*(;\s*\d+(\.\d+)?\s*,\s*\d+(\.\d+)?\s*)*$'
    if not re.fullmatch(patron, texto):
        messagebox.showerror("Error de formato", "El formato debe ser: H1,B1; H2,B2; con números separados por comas y punto y coma.")
        return False

    return True

# Validar el formato de la ecuación ingresada
def validar_formato_ecuacion(texto):
    # Asegurar que "h" se convierta en "H" antes de validar
    texto = texto.replace('h', 'H').upper()  # Convertir "h" a "H" y todo a mayúsculas
    permitido = set("H0123456789+-*/.= ")
    
    # Verificar caracteres permitidos
    for char in texto:
        if char not in permitido:
            messagebox.showerror("Error de formato", "Solo se permiten números, la letra 'H', y operadores matemáticos.")
            return None, None

    # Extraer los valores de a y b si el formato es válido
    # Supongamos que el formato esperado es: "B = a * H / (b + H)"
    patron = r"B\s*=\s*([\d.]+)\s*\*\s*H\s*/\s*\(([\d.]+)\s*\+\s*H\)"
    coincidencia = re.match(patron, texto)
    
    if coincidencia:
        a = float(coincidencia.group(1))
        b = float(coincidencia.group(2))
        print(f"Ecuación ingresada: a = {a}, b = {b}")
        return a, b
    else:
        messagebox.showerror("Error de formato", "El formato debe ser: B = a * H / (b + H)")
        return None, None

# Función para obtener la curva H-B a través de la interfaz gráfica
def obtener_curva_hb_gui(parent_ventana):
    ventana_hb = tk.Toplevel(parent_ventana)
    ventana_hb.title("Curva H-B")
    ventana_hb.geometry("700x300")
    
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

    label_tabla = tk.Label(ventana_hb, text="Ingrese los puntos H-B (Ejemplo: H1,B1; H2,B2...) el primero mayor al 25"
                                            "% de la recta y el otro mayor al 90% de la recta. Si no es de eta manera"
                                            "el valor de a y b estaran mal")
    entry_tabla = tk.Entry(ventana_hb)

    label_ecuacion = tk.Label(ventana_hb, text="Ingrese la ecuación para H-B (Ejemplo: B = m * H + c)")
    entry_ecuacion = tk.Entry(ventana_hb)

    tk.Button(ventana_hb, text="Aceptar", command=lambda: (
        texto_tabla := entry_tabla.get().strip() if hb_opcion.get() == "tabla" else None,
        texto_ecuacion := entry_ecuacion.get().strip() if hb_opcion.get() == "ecuacion" else None,
        validar_formato_tabla(texto_tabla) if texto_tabla else None,
        generar_ecuacion_bh(*procesar_datos_tabla(texto_tabla)) if texto_tabla else None,
        texto_ecuacion := texto_ecuacion.replace('h', 'H') if texto_ecuacion else None,  # Convertir 'h' en 'H'
        validar_formato_ecuacion(texto_ecuacion) if texto_ecuacion else None,
        print(f"Ecuación ingresada: {texto_ecuacion}") if texto_ecuacion else None
    )).pack()
