import numpy as np

# Función para manejar la entrada de datos con validación
def pedir_parametro(prompt, tipo=float, condicion=None, mensaje_error="Entrada no válida."):
    while True:
        try:
            valor = tipo(input(prompt))
            if condicion and not condicion(valor):
                raise ValueError
            return valor
        except ValueError:
            print(mensaje_error)

# Función para obtener los parámetros del usuario
def obtener_parametros():
    print("Ingrese los parámetros del circuito magnético:")
    
    # Pedir los valores de las bobinas
    N1 = pedir_parametro("Número de vueltas N1: ", int, lambda x: x > 0, "Debe ser un número entero positivo.")
    N2 = pedir_parametro("Número de vueltas N2: ", int, lambda x: x > 0, "Debe ser un número entero positivo.")
    
    # Preguntar si se va a ingresar I1 o I2
    corriente_opcion = input("¿Desea ingresar I1 o I2? (Escriba 'I1' o 'I2'): ").strip().upper()
    
    if corriente_opcion == "I1":
        I1 = pedir_parametro("Corriente I1 (Amperios, con signo): ")
        I2 = None
    elif corriente_opcion == "I2":
        I2 = pedir_parametro("Corriente I2 (Amperios, con signo): ")
        I1 = None
    else:
        print("Opción no válida. Asumiendo I1.")
        I1 = pedir_parametro("Corriente I1 (Amperios, con signo): ")
        I2 = None
    
    # Otros parámetros
    factor_apilado = pedir_parametro("Factor de apilado (valor entre 0 y 1): ", float, lambda x: 0 <= x <= 1, "Debe ser un número entre 0 y 1.")
    SL = pedir_parametro("Área de sección transversal SL (m²): ")
    Sc = pedir_parametro("Área de sección transversal Sc (m²): ")
    
    # Dimensiones
    A = pedir_parametro("Ancho A del circuito (m): ")
    L1 = pedir_parametro("Longitud L1 de la sección izquierda (m): ")
    L2 = pedir_parametro("Longitud L2 de la sección derecha (m): ")
    L3 = pedir_parametro("Altura L3 donde se encuentra el entrehierro (m): ")
    LE = pedir_parametro("Longitud LE del entrehierro (m): ")

    # Flujo en el entrehierro
    flujo_entre = pedir_parametro("Flujo magnético deseado en el entrehierro ΦE (Wb, con signo): ")

    return {
        'N1': N1, 'N2': N2, 'I1': I1, 'I2': I2, 
        'factor_apilado': factor_apilado, 'SL': SL, 'Sc': Sc,
        'A': A, 'L1': L1, 'L2': L2, 'L3': L3, 'LE': LE,
        'flujo_entre': flujo_entre
    }

# Función para procesar la curva H-B del material
def obtener_curva_hb():
    opcion_hb = input("¿Desea ingresar la curva H-B como tabla o ecuación? (Escriba 'tabla' o 'ecuacion'): ").strip().lower()
    if opcion_hb == "tabla":
        puntos_hb = []
        print("Ingrese los puntos de la curva H-B. Escriba 'done' para finalizar.")
        while True:
            h = input("Ingrese H (A/m) o 'done' para finalizar: ").strip()
            if h.lower() == 'done':
                break
            b = input("Ingrese B (T): ").strip()
            try:
                h_val = float(h)
                b_val = float(b)
                puntos_hb.append((h_val, b_val))
            except ValueError:
                print("Valores no válidos, intente nuevamente.")
        # Ajustar una curva a los puntos (simplificado)
        h_vals, b_vals = zip(*puntos_hb)
        coef = np.polyfit(h_vals, b_vals, deg=3)  # Polinomio de grado 3
        print(f"Curva H-B ajustada: {coef}")
        return lambda H: np.polyval(coef, H)
    
    elif opcion_hb == "ecuacion":
        print("Ingrese la ecuación de la curva H-B en función de H:")
        # Simular que obtenemos una ecuación válida, esto se debe mejorar.
        return lambda H: float(input(f"Ingrese B para H={H}: "))

    else:
        print("Opción no válida. Asumiendo ecuación.")
        return lambda H: float(input(f"Ingrese B para H={H}: "))

# Función principal para cálculos
def realizar_calculos(parametros, hb_curve):
    N1 = parametros['N1']
    N2 = parametros['N2']
    I1 = parametros['I1']
    I2 = parametros['I2']
    flujo_entre = parametros['flujo_entre']
    
    # Realizar los cálculos (esto es un placeholder, deben agregarse las ecuaciones físicas)
    if I1 is not None:
        I2_calculada = flujo_entre / N2  # Esto es solo un ejemplo
        print(f"Cálculo de I2: {I2_calculada} A")
    elif I2 is not None:
        I1_calculada = flujo_entre / N1  # Esto es solo un ejemplo
        print(f"Cálculo de I1: {I1_calculada} A")

    # Placeholder para los flujos Φ1 y Φ2
    flujo_1 = flujo_entre / 2  # Solo un ejemplo
    flujo_2 = flujo_entre / 2  # Solo un ejemplo

    print(f"Flujo Φ1: {flujo_1} Wb")
    print(f"Flujo Φ2: {flujo_2} Wb")

# Programa principal
if __name__ == "__main__":
    parametros = obtener_parametros()
    hb_curve = obtener_curva_hb()
    realizar_calculos(parametros, hb_curve)
