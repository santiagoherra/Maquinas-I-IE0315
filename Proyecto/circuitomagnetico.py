#Este es el archivo el cual se dara para poder crear las funciones necesarias para poder resolver el circuito magnetico.

#librerias a utilizar
import tkinter as tk
import math

a = [100, 50, 20, None, 0.02, 0.97, None]
b = [0.3, 0.002, 0.02, 0.01, 0.298, 1.1, 1.1, None ]

def funcion_B_H(H):
    return (0.01364 * H) / (1 + 0.0089 * H)

def funcion_H_B(B):
    return  B / (0.01364 - 0.0089 * B)

def reluctancia(largo, u_o, superficie, f_apilado):
    re = largo/(u_o * superficie * f_apilado)
    return re

def solucion(valores_magnitudes_electricas, valores_dimensiones):
    # Inicializar banderas para verificar qué bobina está activa y qué flujo se ha calculado
    bobina1_bandera = False
    flujo1_bandera = False

    # Asignar valores a las variables de magnitudes eléctricas (entradas del usuario)
    N_1, N_2, I_1, I_2, flujo_E, f_apilado, coe_dispersion = valores_magnitudes_electricas

    # Asignar valores a las variables de dimensiones del circuito magnético
    L3, LE, Sc, SL, A, L1, L2, defor_area = valores_dimensiones

    # Corregir el flujo entre las bobinas si se proporcionó un coeficiente de dispersión
    if coe_dispersion is not None:
        flujo_E = flujo_E / coe_dispersion  # Se ajusta el flujo para incluir la dispersión

    # Corregir el área efectiva si se dio un porcentaje de deformación del área
    if defor_area is not None:
        Sc = Sc * (1 + defor_area / 100)  # Ajuste del área en base a la deformación

    # Determinar si se proporcionó la corriente I_1 o I_2
    if I_1:
        # Si se dio I_1, calcular la FMM (fuerza magnetomotriz) de la bobina 1
        fmm_bobina1 = N_1 * I_1  # FMM = N (número de vueltas) * I (corriente)
        bobina1_bandera = True  # Marcar que la bobina 1 está activa
    else:
        # Si no se dio I_1, se debe haber dado I_2, entonces calcular la FMM de la bobina 2
        fmm_bobina2 = N_2 * I_2

    # Calcular la densidad de flujo magnético (B) en el segmento L3
    B_flujoL3 = flujo_E / (Sc * f_apilado)  # B = flujo / (área * factor de apilado)

    # Obtener el campo magnético (H) para el segmento L3 usando la función B-H
    H_flujoL3 = funcion_H_B(B_flujoL3)

    # Calcular la densidad de flujo magnético en el entrehierro
    B_entrehierro = flujo_E / Sc  # B = flujo / área del entrehierro

    # Calcular el campo magnético (H) en el entrehierro usando la permeabilidad del aire (µ0)
    H_entrehierro = B_entrehierro / (4 * math.pi * 10**-7)

    # Calcular la FMM total de la barra central y el entrehierro
    fmm_barra_central_total = H_flujoL3 * A + H_entrehierro * LE  # FMM = H * largo

    # Si la bobina 1 estaba activa
    if bobina1_bandera:
        # Calcular el campo magnético en la malla 1 (restando FMM total de la FMM de la bobina 1)
        H_flujo_1 = (fmm_bobina1 - fmm_barra_central_total) / L1

        # Obtener la densidad de flujo magnético B para la malla 1 usando la función B-H
        B_flujo1 = funcion_B_H(H_flujo_1)

        # Calcular el flujo en la malla 1
        flujo1 = B_flujo1 * SL * f_apilado  # Flujo = B * área * factor de apilado

        # El flujo en la malla 2 es el flujo total menos el flujo de la malla 1
        flujo2 = flujo_E - flujo1

        # Marcar que se ha calculado el flujo 1
        flujo1_bandera = True
    else:
        # Si la bobina 2 estaba activa, calcular el campo magnético en la malla 2
        H_flujo_2 = (fmm_bobina2 - fmm_barra_central_total) / L1

        # Obtener la densidad de flujo magnético B para la malla 2
        B_flujo2 = funcion_B_H(H_flujo_2)

        # Calcular el flujo en la malla 2
        flujo2 = B_flujo2 * SL * f_apilado

        # El flujo en la malla 1 es el flujo total menos el flujo de la malla 2
        flujo1 = flujo_E - flujo2

    # Si el flujo 1 ha sido calculado
    if flujo1_bandera:
        # Obtener la densidad de flujo B para la malla 2
        B_flujo2 = flujo2 / (SL * f_apilado)

        # Calcular el campo magnético H para la malla 2 usando la función B-H
        H_flujo_2 = funcion_H_B(B_flujo2)

        # Calcular la corriente I_2 usando la FMM de la malla 2
        I_2 = (H_flujo_2 * L2 + fmm_barra_central_total) / N_2
    else:
        # Si el flujo 2 ha sido calculado, hacer el cálculo inverso para I_1
        B_flujo1 = flujo1 / (SL * f_apilado)

        # Calcular el campo magnético H para la malla 1
        H_flujo_1 = funcion_H_B(B_flujo1)

        # Calcular la corriente I_1 usando la FMM de la malla 1
        I_1 = (H_flujo_1 * L2 + fmm_barra_central_total) / N_1

    print(f"I1: {I_1}, I2: {I_2}, Flujo1: {flujo1}, Flujo2: {flujo2}")


