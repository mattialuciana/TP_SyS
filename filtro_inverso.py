import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import pandas as pd
import sounddevice as sd
from scipy.signal import correlate
from Cargar_Audios import cargar_audios_por_tipo

def filtro(señal, f1, f2, fs=44100):
    """
    Genera un sweep logaritmico entre dos frecuencias f1 y f2.
    
    Parametros
    ----------
    duracion : float
        Duración del sweep en segundos.
    f1 : float
        Frecuencia inicial en Hz.
    f2 : float
        Frecuencia final en Hz.
    fs : int
        Frecuencia de muestreo en Hz. Por defecto el valor es 44100 Hz.
    
    returns: NumPy array
        Datos de la señal generada.
    
    """
    # Generar el sweep
    R = np.log(f2/f1)
    K = ((len(señal)/fs) * 2*np.pi*f1)/R
    L = (len(señal)/fs)/R
    t = np.arange(0, (len(señal)/fs), 1/fs)

    # Generar el filtro inverso
    w = (K/L) * np.exp(t/L)
    m = f1 / w
    
    filtro = señal[::-1] * m

    # Guardar los audios
    sf.write('filtro_inv_aula.wav', filtro, fs)
    print("Archivo guardado con éxito.")

    return filtro

data = cargar_audios_por_tipo({
    'grabacion': ['sweep_aula.wav']
})

filtro_inverso = filtro(data['grabacion'][0][0], 20, 22000, data['grabacion'][0][1])