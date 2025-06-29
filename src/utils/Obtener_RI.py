import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve
import numpy as np
from scipy.io import wavfile
import soundfile as sf

def respuesta_impulso(filtro, grabacion):
    
    """
    Calcula la respuesta al impulso (RI) de un sistema a partir de un filtro y una grabación.
    Parámetros:
    - filtro (numpy array): el filtro utilizado para la convolución. Debe ser el filtro inverso para 
    el sine sweep original.
    - grabacion (numpy array): la grabación del sine sweep reproducido en el espacio a estudiar.
    Devuelve:
    - h_real (numpy array): la respuesta al impulso normalizada del sistema.
    """

    # Leer los audios
    k = filtro
    y = grabacion

    fs_k = 44100

    # Longitud para convolución lineal
    N = len(k) + len(y) - 1
    N_fft = 1 << int(np.ceil(np.log2(N)))  # próxima potencia de 2

    # FFT de ambos con padding a la misma longitud
    fft_k = np.fft.fft(k, n=N_fft)
    fft_y = np.fft.fft(y, n=N_fft)

    # Multiplicación en frecuencia
    fft_h = fft_k * fft_y

    # Inversa y normalización
    h = np.fft.ifft(fft_h)
    h_real = np.real(h)
    h_real /= np.max(np.abs(h_real))

    # Guardar WAV
    sf.write('respuesta_impulso.wav', h_real, fs_k)

    return h_real