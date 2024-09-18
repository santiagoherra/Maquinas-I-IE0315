#Este es el archivo el cual se dara para poder crear las funciones necesarias para poder resolver el circuito magnetico.

#librerias a utilizar
import tkinter as tk
import math

def reluctancia(largo, u_o, superficie):
    re = largo/(u_o * superficie)
    return re

def dispersion_areaefectiva(area, porcentaje_deformacion):
    return area * (1 + porcentaje_deformacion / 100)

def dispersion_flujo_real(coe_dispersion, flujo_entrehierro):
    return  (1 + coe_dispersion)/(flujo_entrehierro)
    
#Aqui es la funcion de la solucion principal del circuito
def solucion_circuitomagentico(valores_magnitudes_electricas, valores_dimensiones):
    bobina1 = False

    #asignar valores a variables de magnitudes electricas
    N_1, N_2, I_1, I_2, flujo_E = valores_magnitudes_electricas

    #asignar valores a variables de magnitudes electricas
    L3, LE, Sc, SL, A, L1, L2 = valores_dimensiones

    #Se seleccionado cual bobina es la que se le dio el valor de corriente osea i1 o i2
    if I_1:
        fmm_bobina1 = N_1 * I_1
        bobina1 = True
    else:
        fmm_bobina2 = N_2 * I_2

    #calculo de la reluctancia del aire
    reluctancia_entrehierro = reluctancia(valores_dimensiones[0], 4*math.pi*10**-7, valores_dimensiones[2])

    #calculo de la fmm del entrehierro
    fmm_entrehierro = reluctancia_entrehierro * flujo_E

    #obtener el campo del flujo E
    B_flujoe = flujo_E / Sc

    #Obtengo el valor de H del flujo del entre hierro con la funcion B-H
    H = funcion_B_H(B_flujoe)

    #Obtengo la fmm de la reluctancia de la barra
    fmm_reluctancia_barra = H * LE

    #Obtengo la fmm de la barra total
    fmm_barra_central_total = fmm_reluctancia_barra + fmm_entrehierro

    






