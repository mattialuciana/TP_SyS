import numpy as np
import matplotlib.pyplot as plt
#import os
#import sys
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from .Int_Schroeder import integral_schroeder, ventana
from .Convertir_Log import convertir_log
from .RuidoRosa_Grafica import graficar_funcion
from .Suavizado import suavizado
from .Cuadrados_min import cuadrados_minimos
from .Cargar_Audios import cargar_audios_por_tipo
from .Filtros import filtro

def T_Reverberacion(señal, inicio, final):

    """
    Calcula el tiempo de reverberación (T_xx) de una señal de respuesta al impulso (RI) utilizando el 
    método de cuadrados mínimos.
    Parámetros:
    - señal (numpy array): la integral de Schroeder de la respuesta al impulso.
    - inicio (float): nivel del inicio de la ventana en dB.
    - final (float): nivel del final de la ventana en dB.
    Devuelve:
    - T_xx (float): tiempo de reverberación calculado. Según los valores de incio y final calcula:
    T30 (-5 y -35), T20 (-5 y -25), T10(-5 y -15) o EDT (-1 y -11).
    """

    ventana_señal, start = ventana(señal, inicio, final)
    f, m, b = cuadrados_minimos(ventana_señal)
    T_xx = (-60)/m

    return T_xx

def C80(señal, fs=44100):
    """
    Calcula el C80 de una señal de respuesta al impulso (RI). Se asume que el impulso comienza en el punto
    de máxima amplitud.
    Parámetros:
    - señal (numpy array): la señal de respuesta al impulso.
    - fs (int): frecuencia de muestreo de la señal (opcional, por defecto 44100 Hz).
    Devuelve:
    - C80 (float): el valor de C80 en dB.
    """
    
    T = int(0.08 * fs) 
    p2 = señal**2
    principio = np.sum(p2[np.argmax(señal) :np.argmax(señal) + T])
    final = np.sum(p2[np.argmax(señal) + T:])
    C80 = 10 * np.log10(principio / final)
        
    return C80

def D50(señal, fs=44100):
    """
    Calcula el D50 de una señal de respuesta al impulso (RI). Se asume que el impulso comienza en el punto
    de máxima amplitud.
    Parámetros:
    - señal (numpy array): la señal de respuesta al impulso.
    - fs (int): frecuencia de muestreo de la señal (opcional, por defecto 44100 Hz).
    Devuelve:
    - D50 (float): el porcentaje de D50.
    """
    
    T = int(0.05 * fs) 
    p2 = señal**2
    principio = np.sum(p2[np.argmax(señal) :np.argmax(señal) + T])
    final = np.sum(p2)
    D50 = principio / final
        
    return 100*D50

if __name__ == "__main__":
    
    data = cargar_audios_por_tipo({"sintesis": ["src\\SintesisIR1.wav"], "RI": ["src\\IR1.wav"]})
    # filtro1k = filtro('octavas', data["sintesis"][0][0], data["sintesis"][0][1]) # Sintética
    filtro1k = filtro('octavas', data["RI"][0][0], data["RI"][0][1]) # Real
    suave = suavizado(filtro1k[5], 10)
    log = convertir_log(suave)
    int_sch = integral_schroeder(suave, 6)

    T30 = T_Reverberacion(int_sch, -5, -35)
    T20 = T_Reverberacion(int_sch, -5, -25)
    T10 = T_Reverberacion(int_sch, -5, -15)
    EDT = T_Reverberacion(int_sch, -1, -11)
    # C_80 = C80(suave, data["sintesis"][0][1]) # Sintética
    # D_50 = D50(suave, data["sintesis"][0][1]) # Sintética
    C_80 = C80(suave, data["RI"][0][1]) # Real
    D_50 = D50(suave, data["RI"][0][1]) # Real

    ventana_señal, start = ventana(int_sch, -5, -35)
    f, m, b = cuadrados_minimos(ventana_señal)

    print("Parámetros para la banda de octava de 1 kHz:")
    print(f"D50: {D_50:.4f}%")
    print(f"C80: {C_80:.4f} dB")
    print("Tiempos de Reverberación:")
    print(f"T30: {T30:.4f} s")
    print(f"T20: {T20:.4f} s")  
    print(f"T10: {T10:.4f} s")
    print(f"EDT: {EDT:.4f} s")

    plt.figure(figsize=(10,6))
    t = np.arange(0, len(int_sch)/data["RI"][0][1], 1/data["RI"][0][1])
    t2 = np.arange(0, len(log)/data["RI"][0][1], 1/data["RI"][0][1])
    t3 = t[start:start + len(ventana_señal)] 
    plt.plot(t, int_sch, label='Integral de Schroeder', color='brown')
    plt.plot(t2, log, label='Respuesta al impulso suavizada en escala logaritmica', color='blue')
    plt.plot(t3, f, label='Ajuste lineal para T30', color='green')
    plt.title('Integral de Schroeder y Respuesta al impulso suavizada')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud (dB)')
    plt.legend()
    plt.tight_layout()
    plt.show()
    