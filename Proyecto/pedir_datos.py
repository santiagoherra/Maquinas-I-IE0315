def pedir_datos():
    def pedir_parametro(prompt, tipo=float, condicion=None, mensaje_error="Entrada no válida."):
        # Manejo de entrada con validación
        while True:
            try:
                valor = tipo(input(prompt))
                if condicion and not condicion(valor):
                    raise ValueError
                return valor
            except ValueError:
                print(mensaje_error)

    print("Ingrese los parámetros del circuito magnético:")
    
    # Pedimos los valores con validaciones robustas
    N1 = pedir_parametro("Número de vueltas N1: ", int, lambda x: x > 0, "Debe ser un número entero positivo.")
    N2 = pedir_parametro("Número de vueltas N2: ", int, lambda x: x > 0, "Debe ser un número entero positivo.")
    
    corriente_opcion = input("¿Desea ingresar I1 o I2? (Escriba 'I1' o 'I2'): ").strip().upper()
    
    if corriente_opcion == "I1":
        I1 = pedir_parametro("Corriente I1 (Amperios, con signo): ")
        I2 = None
    elif corriente_opcion == "I2":
        I2 = pedir_parametro("Corriente I2 (Amperios, con signo): ")
        I1 = None
    else:
        print("Opción no válida. Se asumirá I1.")
        I1 = pedir_parametro("Corriente I1 (Amperios, con signo): ")
        I2 = None
    
    # Otros parámetros con validaciones
    factor_apilado = pedir_parametro("Factor de apilado (valor entre 0 y 1, exclusivo): ", float, lambda x: 0 < x < 1, "Debe estar entre 0 y 1 (excluyendo los extremos).")
    SL = pedir_parametro("Área de sección transversal SL (m²): ", float, lambda x: x > 0, "Debe ser un número positivo.")
    Sc = pedir_parametro("Área de sección transversal Sc (m²): ", float, lambda x: x > 0, "Debe ser un número positivo.")
    
    # Dimensiones con validaciones
    A = pedir_parametro("Ancho A del circuito (m): ", float, lambda x: x > 0, "Debe ser un número positivo.")
    L1 = pedir_parametro("Longitud L1 de la sección izquierda (m): ", float, lambda x: x > 0, "Debe ser un número positivo.")
    L2 = pedir_parametro("Longitud L2 de la sección derecha (m): ", float, lambda x: x > 0, "Debe ser un número positivo.")
    L3 = pedir_parametro("Altura L3 donde se encuentra el entrehierro (m): ", float, lambda x: x > 0, "Debe ser un número positivo.")
    LE = pedir_parametro("Longitud LE del entrehierro (m): ", float, lambda x: x > 0, "Debe ser un número positivo.")

    # Flujo en el entrehierro
    flujo_entre = pedir_parametro("Flujo magnético deseado en el entrehierro ΦE (Wb, con signo): ")

    # Opcional: coeficiente de dispersión magnética
    coeficiente_dispersion = input("¿Conoce el coeficiente de dispersión magnética? (Escriba 'sí' o 'no'): ").strip().lower()
    if coeficiente_dispersion == 'sí':
        coeficiente_dispersion = pedir_parametro("Ingrese el coeficiente de dispersión magnética: ")
    else:
        coeficiente_dispersion = None

    # Opcional: porcentaje de deformación del área efectiva del entrehierro
    porcentaje_deformacion = input("¿Conoce el porcentaje de deformación del área efectiva en el entrehierro? (Escriba 'sí' o 'no'): ").strip().lower()
    if porcentaje_deformacion == 'sí':
        porcentaje_deformacion = pedir_parametro("Ingrese el porcentaje de deformación del área (%): ")
    else:
        porcentaje_deformacion = None

    return {
        'N1': N1, 'N2': N2, 'I1': I1, 'I2': I2, 
        'factor_apilado': factor_apilado, 'SL': SL, 'Sc': Sc,
        'A': A, 'L1': L1, 'L2': L2, 'L3': L3, 'LE': LE,
        'flujo_entre': flujo_entre,
        'coeficiente_dispersion': coeficiente_dispersion,
        'porcentaje_deformacion': porcentaje_deformacion
    }
