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
    bobina1_bandera = False
    flujo1_bandera = False

    #asignar valores a variables de magnitudes electricas
    N_1, N_2, I_1, I_2, flujo_E = valores_magnitudes_electricas

    #asignar valores a variables de magnitudes electricas
    L3, LE, Sc, SL, A, L1, L2 = valores_dimensiones

    #Se seleccionado cual bobina es la que se le dio el valor de corriente osea i1 o i2
    if I_1:
        fmm_bobina1 = N_1 * I_1
        bobina1_bandera = True
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

    #Obtengo la fmm de la reluctancia de la malla donde me dieron la corriente 
    #ademas obtengo el H y con eso B del flujo y por ultimo el flujo.

    if bobina1_bandera:
        fmm_reluctancia_malla1 = fmm_barra_central_total - fmm_bobina1
        H_flujo_1 = fmm_reluctancia_malla1 / 2 * L1 + A 
        B_flujo1 = funcion_H_B(H_flujo_1)
        flujo1 = B_flujo1 / SL
        flujo2  = flujo1 + flujo_E
        flujo1_bandera = True

    else:
        fmm_reluctancia_malla2 = fmm_barra_central_total - fmm_bobina2
        H_flujo_2 = fmm_reluctancia_malla2 / 2 * L2 + A
        B_flujo2 = funcion_H_B(H_flujo_1)
        flujo2 = B_flujo2 / SL
        flujo1  = flujo2 + flujo_E

    #Obtengo la corriente que me falta.
    #Primero obtengo la fuerza de la reluctancia en la malla que me hace falta.
    #Despues con ltk despues la corriente que hace falta.

    if not flujo1_bandera:
        B_flujo1 = flujo1 / SL
        H_flujo_1 = funcion_H_B(B_flujo1)
        fmm_reluctancia_malla1 = H_flujo_1 * (2*L1 + A)
        I_1 = fmm_barra_central_total + fmm_reluctancia_malla1 / N_1
    
    else:
        B_flujo2 = flujo2 / SL
        H_flujo_2 = funcion_H_B(B_flujo2)
        fmm_reluctancia_malla2 = H_flujo_2 * (2*L2 + A)
        I_2 = fmm_barra_central_total + fmm_reluctancia_malla1 / N_1

    return I_1, I_2, flujo1, flujo2



    
    
    
    

    
     






