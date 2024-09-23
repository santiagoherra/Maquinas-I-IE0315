#Este es el archivo el cual se dara para poder crear las funciones necesarias para poder resolver el circuito magnetico.

#librerias a utilizar
import re
import tkinter as tk 
from tkinter import messagebox, PhotoImage, ttk
import math
from scipy.optimize import curve_fit

class CircuitoMagnetico:

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("Formulario de Datos - Circuito Magnético")
        
        # Inicializar los atributos para almacenar los valores de los inputs
        self.valores_magnitudes_electricas = None
        self.valores_dimensiones = None
        self.funcion_a = None
        self.funcion_b = None

        #variables finales del circuito para mostrar resultado.
        self.resultado_I1 = None
        self.resultado_I2 = None
        self.resultado_flujo1 = None
        self.resultado_flujo2 = None
        
        # Crear las entradas gráficas
        self.crear_entradas()

    def funcion_B_H(self, H):
        return (self.funcion_a * H) / (1 + self.funcion_b * H)

    def funcion_H_B(self, B):
        return B / (self.funcion_a - self.funcion_b * B)

    def generar_ecuacion_bh(self, H_values, B_values):
        if len(H_values) < 2 or len(B_values) < 2:
            messagebox.showerror("Error", "Se requieren al menos dos pares de valores H y B para ajustar la curva.")
            return None, None

        try:
            # Estimar los valores iniciales
            p0 = [max(B_values), max(H_values) / 2]
            popt, _ = curve_fit(self.funcion_bh, H_values, B_values, p0=p0)
            self.funcion_a, self.funcion_b = popt

            ecuacion_str = f"{self.funcion_a:.4f} * H / ({self.funcion_b:.4f} + H)"
            messagebox.showinfo("Ecuación B(H)", f"La ecuación B(H) es: {ecuacion_str}")
            return self.funcion_a, self.funcion_b

        except (RuntimeError, ValueError) as e:
            messagebox.showerror("Error", f"No se pudo ajustar la curva: {str(e)}.")
            return None, None

    def funcion_bh(self, H, a, b):
        return a * H / (b + H)

    def validar_formato_tabla(self, texto):
        texto = texto.strip()
        if texto.endswith(";"):
            texto = texto[:-1].strip()

        patron = r'^\d+(\.\d+)?\s*,\s*\d+(\.\d+)?\s*(;\s*\d+(\.\d+)?\s*,\s*\d+(\.\d+)?\s*)*$'
        if not re.fullmatch(patron, texto):
            messagebox.showerror("Error de formato", "El formato debe ser: H1,B1; H2,B2; con números separados por comas y punto y coma.")
            return False

        return True

    def validar_formato_ecuacion(self, texto):
        texto = texto.replace('h', 'H').upper()
        permitido = set("H0123456789+-*/.= ")
        
        for char in texto:
            if char not in permitido:
                messagebox.showerror("Error de formato", "Solo se permiten números, la letra 'H', y operadores matemáticos.")
                return None, None

        patron = r"B\s*=\s*([\d.]+)\s*\*\s*H\s*/\s*\(([\d.]+)\s*\+\s*H\)"
        coincidencia = re.match(patron, texto)
        
        if coincidencia:
            self.funcion_a = float(coincidencia.group(1))
            self.funcion_b = float(coincidencia.group(2))
            return self.funcion_a, self.funcion_b
        else:
            messagebox.showerror("Error de formato", "El formato debe ser: B = a * H / (b + H)")
            return None, None

    def obtener_curva_hb_gui(self):
        ventana_hb = tk.Toplevel(self.ventana)
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

        label_tabla = tk.Label(ventana_hb, text="Ingrese los puntos H-B (Ejemplo: H1,B1; H2,B2...)")
        entry_tabla = tk.Entry(ventana_hb)

        label_ecuacion = tk.Label(ventana_hb, text="Ingrese la ecuación para H-B (Ejemplo: B = a * H / (b + H))")
        entry_ecuacion = tk.Entry(ventana_hb)

        def procesar_datos():
            texto_tabla = entry_tabla.get().strip() if hb_opcion.get() == "tabla" else None
            texto_ecuacion = entry_ecuacion.get().strip() if hb_opcion.get() == "ecuacion" else None
            
            if texto_tabla and self.validar_formato_tabla(texto_tabla):
                H_values, B_values = self.procesar_datos_tabla(texto_tabla)
                if H_values and B_values:
                    self.generar_ecuacion_bh(H_values, B_values)
            
            if texto_ecuacion:
                self.validar_formato_ecuacion(texto_ecuacion)

        tk.Button(ventana_hb, text="Aceptar", command=procesar_datos).pack()

    def procesar_datos_tabla(self, texto_tabla):
        pares_hb = texto_tabla.split(";")
        H_values = []
        B_values = []

        for par in pares_hb:
            if par.strip():
                try:
                    H, B = map(float, par.split(","))
                    H_values.append(H)
                    B_values.append(B)
                except ValueError:
                    messagebox.showerror("Error", f"Formato inválido en el par: {par}")
                    return None, None

        return H_values, B_values

    # Crear las entradas gráficas y otros métodos ya existentes
    def crear_entradas(self):
        # El resto de la función de crear_entradas, aquí puedes agregar un botón para la curva H-B
        self.entry_N1, _ = self.crear_entrada("N1 [vueltas]", 0)
        # ... (el resto de tus entradas)
        tk.Button(self.ventana, text="Ajustar Curva H-B", command=self.obtener_curva_hb_gui).grid(row=16, column=0, columnspan=3, pady=10)

    def crear_entrada(self, label, fila, tipo_unidad=None):
        tk.Label(self.ventana, text=label).grid(row=fila, column=0, padx=5, pady=5)
        entry = tk.Entry(self.ventana)
        entry.grid(row=fila, column=1, padx=5, pady=5)
        if tipo_unidad:
            combobox = ttk.Combobox(self.ventana, values=tipo_unidad)
            combobox.grid(row=fila, column=2)
            combobox.set(tipo_unidad[0])  
            return entry, combobox
        return entry, None

    def solucion(self):
        # Inicializar banderas para verificar qué bobina está activa y qué flujo se ha calculado
        bobina1_bandera = False
        flujo1_bandera = False

        # Asignar valores a las variables de magnitudes eléctricas (entradas del usuario)
        N_1, N_2, I_1, I_2, flujo_E, f_apilado, coe_dispersion = self.valores_magnitudes_electricas

        # Asignar valores a las variables de dimensiones del circuito magnético
        L3, LE, Sc, SL, A, L1, L2, defor_area = self.valores_dimensiones

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
        H_flujoL3 = self.funcion_H_B(B_flujoL3)

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
            B_flujo1 = self.funcion_B_H(H_flujo_1)

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
            B_flujo2 = self.funcion_B_H(H_flujo_2)

            # Calcular el flujo en la malla 2
            flujo2 = B_flujo2 * SL * f_apilado

            # El flujo en la malla 1 es el flujo total menos el flujo de la malla 2
            flujo1 = flujo_E - flujo2

        # Si el flujo 1 ha sido calculado
        if flujo1_bandera:
            # Obtener la densidad de flujo B para la malla 2
            B_flujo2 = flujo2 / (SL * f_apilado)

            # Calcular el campo magnético H para la malla 2 usando la función B-H
            H_flujo_2 = self.funcion_H_B(B_flujo2)

            # Calcular la corriente I_2 usando la FMM de la malla 2
            I_2 = (H_flujo_2 * L2 + fmm_barra_central_total) / N_2
        else:
            # Si el flujo 2 ha sido calculado, hacer el cálculo inverso para I_1
            B_flujo1 = flujo1 / (SL * f_apilado)

            # Calcular el campo magnético H para la malla 1
            H_flujo_1 = self.funcion_H_B(B_flujo1)

            # Calcular la corriente I_1 usando la FMM de la malla 1
            I_1 = (H_flujo_1 * L2 + fmm_barra_central_total) / N_1

        #ASIGNANDO VARIABLES PARA EL RESULTADO FINAL.
        self.resultado_I1 = I_1
        self.resultado_I2 = I_2
        self.resultado_flujo1 = flujo1
        self.resultado_flujo2 = flujo2


    #METODOS PARA OBTENER LOS DATOS Y VALIDAR LOS DATOS

    def crear_entradas(self):
        # Función para crear una entrada con un combobox para la unidad
        def crear_entrada(label, fila, tipo_unidad=None):
            tk.Label(self.ventana, text=label).grid(row=fila, column=0, padx=5, pady=5)
            entry = tk.Entry(self.ventana)
            entry.grid(row=fila, column=1, padx=5, pady=5)
            if tipo_unidad:
                combobox = ttk.Combobox(self.ventana, values=tipo_unidad)
                combobox.grid(row=fila, column=2)
                combobox.set(tipo_unidad[0])  # Seleccionar por defecto la primera unidad
                return entry, combobox
            return entry, None

        # Crear las entradas y comboboxes
        self.entry_N1, _ = crear_entrada("N1 [vueltas]", 0)
        self.entry_N2, _ = crear_entrada("N2 [vueltas]", 1)
        self.entry_I1, _ = crear_entrada("I1 [A]", 2)
        self.entry_I2, _ = crear_entrada("I2 [A]", 3)
        self.entry_factor_apilado, _ = crear_entrada("Factor Apilado", 4)
        self.entry_SL, self.unidad_SL = crear_entrada("SL [Área]", 5, ["m²", "cm²", "mm²"])
        self.entry_Sc, self.unidad_Sc = crear_entrada("Sc [Área]", 6, ["m²", "cm²", "mm²"])
        self.entry_A, self.unidad_A = crear_entrada("Ancho A [Longitud]", 7, ["m", "cm", "mm"])
        self.entry_L1, self.unidad_L1 = crear_entrada("L1 [Longitud]", 8, ["m", "cm", "mm"])
        self.entry_L2, self.unidad_L2 = crear_entrada("L2 [Longitud]", 9, ["m", "cm", "mm"])
        self.entry_L3, self.unidad_L3 = crear_entrada("L3 [Longitud]", 10, ["m", "cm", "mm"])
        self.entry_LE, self.unidad_LE = crear_entrada("LE [Longitud]", 11, ["m", "cm", "mm"])
        self.entry_flujo_entre, _ = crear_entrada("Flujo ΦE [Wb]", 12)
        self.entry_coef_dispersion, _ = crear_entrada("Coef. Dispersión", 13)
        self.entry_porcentaje_deformacion, _ = crear_entrada("Deformación Área [%]", 14)

        #IMPLEMENTACION DE LA FIGURA
        self.imagen_circuito = PhotoImage(file="Proyecto/figura_circuito.png")
        label_imagen_circuito = tk.Label(self.ventana, image=self.imagen_circuito)
        label_imagen_circuito.grid(row=0, column=4, rowspan=15, padx=20, pady=20, sticky='n')

        # Botones para procesar datos
        tk.Button(self.ventana, text="Enviar", command=self.procesar_datos).grid(row=15, column=0, columnspan=3, pady=10)

    def validar_entrada(self, entry, campo_nombre, permitir_negativo=False, condicion=None):
        try:
            valor = float(entry.get().strip())  # Eliminar espacios en blanco
            if not permitir_negativo and valor < 0:
                raise ValueError
            if condicion and not condicion(valor):
                raise ValueError
            return valor
        except ValueError:
            mensaje_error = f"Valor no válido o fuera de rango en el campo: {campo_nombre}"
            if not permitir_negativo:
                mensaje_error += " (no se permiten valores negativos)"
            messagebox.showerror("Error", mensaje_error)
            return None
        
    def convertir_a_unidades(self, valor, unidad, tipo):
        conversiones = {
            'longitud': {'cm': 100, 'mm': 1000},
            'area': {'cm²': 10000, 'mm²': 1000000}
        }
        if unidad in conversiones[tipo]:
            return valor / conversiones[tipo][unidad]
        return valor


    def recoger_datos(self):
        # Validar los campos y convertir unidades
        N1 = self.validar_entrada(self.entry_N1, "N1 [vueltas]", permitir_negativo=False)
        N2 = self.validar_entrada(self.entry_N2, "N2 [vueltas]", permitir_negativo=False)
        
        I1 = self.validar_entrada(self.entry_I1, "I1 [A]", permitir_negativo=True) if self.entry_I1.get() else None
        I2 = self.validar_entrada(self.entry_I2, "I2 [A]", permitir_negativo=True) if self.entry_I2.get() else None
        
        factor_apilado = self.validar_entrada(self.entry_factor_apilado, "Factor Apilado", permitir_negativo=False, condicion=lambda x: 0 < x < 1)

        SL = self.convertir_a_unidades(self.validar_entrada(self.entry_SL, "Área SL", permitir_negativo=False), self.unidad_SL.get(), 'area')
        Sc = self.convertir_a_unidades(self.validar_entrada(self.entry_Sc, "Área Sc", permitir_negativo=False), self.unidad_Sc.get(), 'area')

        A = self.convertir_a_unidades(self.validar_entrada(self.entry_A, "Ancho A", permitir_negativo=False), self.unidad_A.get(), 'longitud')
        L1 = self.convertir_a_unidades(self.validar_entrada(self.entry_L1, "Longitud L1", permitir_negativo=False), self.unidad_L1.get(), 'longitud')
        L2 = self.convertir_a_unidades(self.validar_entrada(self.entry_L2, "Longitud L2", permitir_negativo=False), self.unidad_L2.get(), 'longitud')
        L3 = self.convertir_a_unidades(self.validar_entrada(self.entry_L3, "Altura L3", permitir_negativo=False), self.unidad_L3.get(), 'longitud')
        LE = self.convertir_a_unidades(self.validar_entrada(self.entry_LE, "Longitud LE", permitir_negativo=False), self.unidad_LE.get(), 'longitud')

        flujo_entre = self.validar_entrada(self.entry_flujo_entre, "Flujo ΦE [Wb]", permitir_negativo=False)
        coeficiente_dispersion = self.validar_entrada(self.entry_coef_dispersion, "Coef. Dispersión", permitir_negativo=False) if self.entry_coef_dispersion.get() else None
        porcentaje_deformacion = self.validar_entrada(self.entry_porcentaje_deformacion, "Deformación Área [%]", permitir_negativo=False) if self.entry_porcentaje_deformacion.get() else None

        # Verificar si algún campo contiene un valor no válido
        if None in [N1, N2, factor_apilado, SL, Sc, A, L1, L2, L3, LE, flujo_entre]:
            messagebox.showerror("Error", "Por favor corrija los errores antes de continuar.")
            return None, None

        # Guardar los valores obtenidos en listas
        self.valores_magnitudes_electricas = [N1, N2, I1, I2, flujo_entre, coeficiente_dispersion, porcentaje_deformacion, factor_apilado]
        self.valores_dimensiones = [L1, L2, L3, LE, Sc, SL, A]
    
    def procesar_datos(self):
        # Recolectar los datos validados y convertidos
        self.valores_magnitudes_electricas, self.valores_dimensiones = self.recoger_datos()

        if self.valores_magnitudes_electricas and self.valores_dimensiones:
            self.solucion()
            messagebox.showinfo(f"RESULTADO:\nCorriente 1 = {self.resultado_I1}\Corriente 2 = {self.resultado_I2}\n"
                                f"Flujo 1 = {self.resultado_flujo1}\nFlujo 2 = {self.resultado_flujo2}")

    

def main():
    root = tk.Tk()
    circuito = CircuitoMagnetico(root)
    root.mainloop()

main()