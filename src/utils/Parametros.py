import numpy as np
from utils.Int_Schroeder import integral_schroeder, ventana
from utils.Convertir_Log import convertir_log
from utils.RuidoRosa_Grafica import graficar_funcion
from utils.Suavizado import suavizado
from utils.Cuadrados_min import cuadrados_minimos
from utils.Cargar_Audios import cargar_audios_por_tipo
from utils.Filtros import filtro

def T_Reverberacion(señal, inicio, final):

    """
    Calcula el tiempo de reverberación (T_xx) de una señal de respuesta al impulso (RI) utilizando el 
    método de cuadrados mínimos.
    Parámetros:
    - señal (numpy array): la señal de respuesta al impulso.
    - inicio (float): nivel del inicio de la ventana en dB.
    - final (float): nivel del final de la ventana en dB.
    Devuelve:
    - T_xx (float): tiempo de reverberación calculado. Según los valores de incio y final calcula:
    T30 (-5 y -35), T20 (-5 y -25), T10(-5 y -15) o EDT (-1 y -11).
    """

    ventana_señal, start = ventana(señal, inicio, final)
    f, m, b = cuadrados_minimos(ventana_señal)
    T_xx = (-60-b)/m

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
    
    data = cargar_audios_por_tipo({"sintesis": ["SintesisRtaImpulso(2).wav"], "RI": ["IR1.wav"]})
    # filtro1k = filtro('octavas', data["sintesis"][0][0], data["sintesis"][0][1]) # Sintética
    filtro1k = filtro('octavas', data["RI"][0][0], data["RI"][0][1]) # Real
    suave = suavizado(filtro1k[5], 10)
    int_sch = integral_schroeder(suave, 6)

    T30 = T_Reverberacion(int_sch, -5, -35)
    T20 = T_Reverberacion(int_sch, -5, -25)
    T10 = T_Reverberacion(int_sch, -5, -15)
    EDT = T_Reverberacion(int_sch, -1, -11)
    C_80 = C80(suave, data["RI"][0][1])
    D_50 = D50(suave, data["RI"][0][1])

    print("Parámetros para la banda de octava de 1 kHz:")
    print(f"D50: {D_50:.4f}%")
    print(f"C80: {C_80:.4f} dB")
    print("Tiempos de Reverberación:")
    print(f"T30: {T30:.4f} s")
    print(f"T20: {T20:.4f} s")  
    print(f"T10: {T10:.4f} s")
    print(f"EDT: {EDT:.4f} s")