import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import pandas as pd
import sounddevice as sd
from scipy.signal import correlate

def sweep_filtro(duracion, f1, f2, fs=44100):
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
    K = (duracion * 2*np.pi*f1)/R
    L = duracion/R
    t = np.arange(0, duracion, 1/fs)

    sweep = np.sin(K * (np.exp(t/L) - 1))

    # Generar el filtro inverso
    w = (K/L) * np.exp(t/L)
    m = f1 / w
    
    filtro = sweep[::-1] * m

    # Guardar los audios
    sf.write('sine_sweep.wav', sweep, fs)
    sf.write('filtro.wav', filtro, fs)
    print("Archivo guardado con éxito.")

    return sweep, filtro

def adq_rep(señal, fs=44100, entrada=None, salida=None):
    """
    Función para reproducir y grabar audio al mismo tiempo.
    
    Parametros:
    señal : array
        Señal de audio a reproducir.
    fs : int
        Frecuencia de muestreo.
    entrada : int
        Dispositivo de entrada (opcional). Ingresar nombre completo del dispositivo.
    salida : int
        Dispositivo de salida (opcional). Ingresar nombre completo del dispositivo.
    """
    if entrada is not None or salida is not None:
        sd.default.device = (entrada, salida)
    
    # Reproducir y grabar
    grabacion = sd.playrec(señal, fs, channels=2)
    sd.wait()  # esperar a que termine
    sf.write("respuesta_grabada.wav", grabacion, fs)
    print("Grabación guardada como 'respuesta_grabada.wav'")
    return grabacion

def latencia(recording, barrido, fs=44100):
    """
    Estima la latencia entre la grabación y el barrido.
    
    Parametros:
    recording : array
        Señal grabada.
    barrido : array
        Señal del barrido.
    fs : int
        Frecuencia de muestreo.
    
    returns: float
        Latencia estimada en segundos.
    """
    # Convertir a 1D por si es estéreo
    recording = recording.flatten()

    # Correlación cruzada para estimar desplazamiento
    corr = correlate(recording, barrido, mode='full')
    lag = np.argmax(corr) - len(barrido) - 1 
    latencia_estimada = lag / fs
    print(f"Latencia estimada: {latencia_estimada:.4f} segundos")
    
    return latencia_estimada

if __name__ == "__main__":

    # Generar el barrido y el filtro
    # Duración del barrido en segundos, frecuencia inicial 10 Hz, frecuencia final 20 Hz, frecuencia de muestreo 20000 Hz
    barrido, filter = sweep_filtro(10, 20, 20000)

    fs = 44100
    t = np.arange(0, 10, 1/fs)

    fs = 44100
    t = np.arange(0, 10, 1/fs)
    # Reproducir y grabar
    recording = adq_rep(barrido, fs) 
    sd.wait()

    # Estimar latencia
    latencia_estimada = latencia(recording, barrido, fs)