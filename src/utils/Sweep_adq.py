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

"""
Según lo que estuvimos investigando, para calcular la latencia entre dos señales primero hay que determinar
el "lag" en las mismas, este "lag" representa la cantidad de muestras que están desfazadas una de la otra y
se puede determinar a partir de la realizar una correlación cruzada entre la señal original y la señal 
grabada, básicamente se trata de comparar las señales entre sí para obtener un valor de correlación que 
indica que tanto se parecen las señales cuando una de ellas es desplazada en "k" muestras respecto de la 
otra. Cuando este valor se hace máximo significa que las dos señales están "superpuestas" y el valor de k 
indica cuanto se tuvo que desplazar la señal grabada para que esto suceda. Si a este valor de "k" le 
restamos la cantidad de muestras de la señal original obtendríamos el "lag" y a partir de estas y sabiendo 
la frecuencia de muestreo podríamos obtener la latencia en segundos. Lamentablemente los valores que 
obtenemos son muy dispersos y no son los que se podría esperar, por lo que hay algo que evidentemente no 
estamos haciendo bien o no estamos viendo.
""" 

def latencia(recording, original, fs=44100):
    """
    Calcula la latencia entre una grabación y un barrido.
    
    Parámetros:
    recording : array
        Señal grabada.
    original : array
        Señal original.
    fs : int
        Frecuencia de muestreo.
    
    Retorna:
    float
        Latencia estimada en segundos.
    """
    # Asegurarse de que las señales sean 1D
    if recording.ndim > 1:
        recording = recording.flatten()
    if original.ndim > 1:
        original = original.flatten()

    # Correlación cruzada para estimar desplazamiento
    corr = correlate(recording, original, mode='full')
    lag = np.argmax(corr) - len(original) - 1 
    latencia_estimada = lag / fs
    print(f"Latencia estimada: {latencia_estimada:.4f} segundos")

    return latencia_estimada

if __name__ == "__main__":
    # Ejemplo de uso
    barrido, filtro = sweep_filtro(10, 20, 20000)
    grabacion = adq_rep(barrido)
    latencia_estimada = latencia(grabacion, barrido)
    
    # Graficar las señales
    t = np.arange(0, len(barrido)) / 44100 
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t, barrido)
    plt.title('Barrido')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    

    plt.subplot(2, 1, 2)
    plt.plot(t, filtro, color='red')
    plt.title('Filtro Inverso')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    

    plt.tight_layout()
    plt.show()
