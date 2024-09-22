from sympy import symbols, Eq, solve
from circuitomagnetico import solucion_circuitomagentico
import math

a = [100, 50, 20, None, 0.02, 0.97, None]
b = [0.3, 0.002, 0.02, 0.01, 0.298, 1.1, 1.1, None ]


def valores():
# Definimos las variables a y b como incógnitas
    a, b = symbols('a b')

    # Valores proporcionados de la tabla
    H1, B1 = 160, 0.9  # Al 20 Av/m
    H2, B2 = 2000, 1.45  # Al 3000 Av/m

    # Definir las ecuaciones usando la fórmula de Froelich
    equation1 = Eq(B1, (a * H1) / (1 + b * H1))
    equation2 = Eq(B2, (a * H2) / (1 + b * H2))

    # Resolver el sistema de ecuaciones
    soluciones = solve((equation1, equation2), (a, b))

    # Imprimir las soluciones
    print(f"Solución para a: {soluciones[a]}")
    print(f"Solución para b: {soluciones[b]}")

def funcion_B_H(H):
    return (0.01364 * H) / (1 + 0.0089 * H)

def funcion_H_B(B):
    return  B / (0.01364 - 0.0089 * B)

def reluctancia(largo, u_o, superficie, f_apilado):
    re = largo/(u_o * superficie * f_apilado)
    return re

def solucion(valores_magnitudes_electricas, valores_dimensiones):
    bobina1_bandera = False
    flujo1_bandera = False

    #asignar valores a variables de magnitudes electricas
    N_1, N_2, I_1, I_2, flujo_E, f_apilado, coe_dispersion = valores_magnitudes_electricas

    #asignar valores a variables de magnitudes electricas
    L3, LE, Sc, SL, A, L1, L2, defor_area= valores_dimensiones

    #corregir el flujo E si si dieron el coeficiente de dispersion
    if coe_dispersion != None:
        flujo_E = flujo_E/coe_dispersion

    #Si la persona dio el porcentaje de deformacion del area. Se usa elif porque solo se tiene que 
    #aplicar uno creo.
    if defor_area != None:
        A = A * (1 + defor_area / 100)

    if I_1:
        fmm_bobina1 = N_1 * I_1
        bobina1_bandera = True
    else:
        fmm_bobina2 = N_2 * I_2


    B_flujoL3 = flujo_E/(Sc * f_apilado)

    H_flujoL3 = funcion_H_B(B_flujoL3)

    B_entrehierro = flujo_E/Sc

    H_entrehierro = B_entrehierro/(4*math.pi*10**-7)

    fmm_barra_central_total = H_flujoL3 * A + H_entrehierro * LE

    if bobina1_bandera:

        H_flujo_1 = (fmm_bobina1 - fmm_barra_central_total) / L1

        B_flujo1 = funcion_B_H(H_flujo_1)

        flujo1 = B_flujo1 * SL * f_apilado

        flujo2 = flujo_E - flujo1

        flujo1_bandera = True

    else:
        H_flujo_2 = (fmm_bobina2 - fmm_barra_central_total) / L1

        B_flujo2 = funcion_B_H(H_flujo_2)

        flujo2 = B_flujo2 * SL * f_apilado

        flujo1 = flujo_E - flujo2

    if flujo1_bandera:

        B_flujo2 = flujo2 / (SL * f_apilado)

        H_flujo_2 = funcion_H_B(B_flujo2)

        I_2 = (H_flujo_2 * L2 + fmm_barra_central_total)/N_2

    else:
        B_flujo1 = flujo1 / (SL * f_apilado)

        H_flujo_1 = funcion_H_B(B_flujo1)

        I_1 = (H_flujo_1 * L2 + fmm_barra_central_total)/N_1


    print(f"I1: {I_1}, I2: {I_2}, Flujo1: {flujo1}, Flujo2: {flujo2}")


solucion(a,b)