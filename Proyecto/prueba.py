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

