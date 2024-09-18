#Este es el archivo el cual se dara para poder crear las funciones necesarias para poder resolver el circuito magnetico.

#librerias a utilizar
import tkinter as tk

def fmm_ni(n,i):
    fmm = n * i
    return fmm

def reluctancia(largo, u_o, superficie):
    re = largo/(u_o * superficie)
    return re

def dispersion()

