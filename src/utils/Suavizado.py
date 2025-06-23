import numpy as np 
import scipy.signal as signal 
import matplotlib.pyplot as plt
#import os
#import sys
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .Cargar_Audios import cargar_audios_por_tipo
from .espectro import graficar_espectro_frecuencia

def suavizado(señal, L, fs=44100):
    """
    Suaviza una señal utilizando el método de suavizado de Hilbert.
    Parámetros:
    - señal (array): la señal a suavizar.
    - L (int): longitud del filtro de suavizado.
    - fs (int): frecuencia de muestreo de la señal (opcional, por defecto 44100 Hz).
    Devuelve:
    - suavizada (array): la señal suavizada.
    """

    señal_analitica = signal.hilbert(señal)
    modulo = np.abs(señal_analitica)

    suavizada = np.convolve(modulo, np.ones(L)/L, mode='valid')
    
    return suavizada

if __name__ == "__main__":
        
    data = cargar_audios_por_tipo({
    'respuestas al impulso': ['src\\SintesisIR1.wav', 'src\\IR1.wav']
    })
    suavizado_ri = suavizado(data['respuestas al impulso'][0][0],  L=10, fs=data['respuestas al impulso'][0][1])
    
    graficar_espectro_frecuencia(data['respuestas al impulso'][0][0], fs=data['respuestas al impulso'][0][1], titulo='Respuesta al Impulso Original')
    graficar_espectro_frecuencia(suavizado_ri, fs=data['respuestas al impulso'][0][1], titulo='Suavizado de Respuesta al Impulso')
