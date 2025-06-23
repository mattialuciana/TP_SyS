import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

def graficar_espectro_frecuencia(signal, fs, titulo='Espectro de Frecuencia', xlim=None):
    """
    Grafica el espectro de magnitud de una señal.

    Parámetros:
    - signal (array): señal en el dominio del tiempo.
    - fs (int): frecuencia de muestreo en Hz.
    - titulo (str): título del gráfico.
    - xlim (tupla): límites del eje x (frecuencia), opcional.
    Devuelve:
    - None: muestra el gráfico del espectro de frecuencia.
    """

    N = len(signal)
    fft_result = fft(signal)
    freqs = fftfreq(N, 1/fs)

    # Solo tomamos la mitad positiva del espectro
    magnitudes = np.abs(fft_result)[:N//2]
    freqs = freqs[:N//2]

    plt.figure(figsize=(10, 5))
    plt.plot(freqs, 20*np.log10(magnitudes + 1e-12))  # en dB
    plt.title(titulo)
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Magnitud [dB]')
    if xlim:
        plt.xlim(xlim)
    plt.tight_layout()
    plt.show()
