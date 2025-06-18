import numpy as np 
import scipy.signal as signal
from utils.Cargar_Audios import cargar_audios_por_tipo

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

"""
data = cargar_audios_por_tipo({
    'respuestas al impulso': ['SintesisRtaImpulso.wav', 'RI_sweep.wav']
})

suavizado_ri = suavizado(data['respuestas al impulso'][0][0],  L=100, fs=data['respuestas al impulso'][0][1])
sf.write("SintesisRtaImpulso_suavizado.wav", suavizado_ri, data['respuestas al impulso'][0][1])
"""