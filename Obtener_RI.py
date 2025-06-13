import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve
import numpy as np
from scipy.io import wavfile
import soundfile as sf

def respuesta_impulso(path_archivo_filtro, path_archivo_grabacion):
    
    # Leer los audios
    fs_k, k = wavfile.read(path_archivo_filtro)
    fs_y, y = wavfile.read(path_archivo_grabacion)

    # Asegurar que ambos audios tengan la misma frecuencia de muestreo
    if fs_k != fs_y:
        raise ValueError("Las frecuencias de muestreo no coinciden.")

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

