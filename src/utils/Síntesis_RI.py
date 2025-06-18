import numpy as np
import soundfile as sf
from utils.RuidoRosa_Grafica import graficar_funcion
from utils.Convertir_Log import convertir_log

def sintesis_impulso(T_60, bandas, duracion, fs=44100, amplitud=1):
    """
    Sintetiza una respuesta al impulso (RI) a partir de tiempos de reverberación (T_60) para diferentes bandas de frecuencia.
    
    Parámetros:
    - T_60 (lista): lista de tiempos de reverberación para cada frecuencia. 
    - bandas (str): tipo de bandas de frecuencia ('octavas' o 'tercios').
    - duracion (float): duración de la señal en segundos.
    - fs (int): frecuencia de muestreo en Hz (por defecto 44100).
    - amplitud (float): amplitud de la señal (por defecto 1).
    
    Devuelve:
    - RI_tot (numpy array): señal de respuesta al impulso sintetizada.
    - fs (int): frecuencia de muestreo utilizada.

    """
    if bandas == "octavas":
        frecuencias = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000] 
        
    elif bandas == "tercios":
        frecuencias = [25,31.5,40,50,63,80,100,125,160,200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000,6300,8000,10000,12500,16000,20000] 
        
    T_60 = np.array(T_60)  
    RI = []
    t = np.arange(0, duracion, 1/fs)
    for i in range(len(T_60)):
        tau = -np.log(10**(-3)) / T_60[i]
        y = amplitud * np.exp(-tau * t) * np.cos(2 * np.pi * frecuencias[i] * t)
        RI.append(y)
    
    ruido = np.random.normal(0, 0.005, int(0.05 * fs))
    RI_sintetizada = np.sum(RI, axis=0)  
    
    RI_tot = np.concatenate([ruido, RI_sintetizada + np.random.normal(0, 0.005, len(t))])  
    # RI_tot = RI_tot / np.max(np.abs(RI_tot))  # Normalizar la señal
    sf.write("SintesisRtaImpulso(nonorm).wav", RI_tot, fs)

    return RI_tot, fs

"""
sintesis, fs = sintesis_impulso([1.877, 1.727, 1.588, 2.176, 2.986, 2.813, 2.161, 1.561, 0.810, 0.454], 'octavas', 6)
log = convertir_log(sintesis)
graficar_funcion(len(log)/fs, fs, log, titulo_1='Síntesis de Respuesta al Impulso (Log)')
"""