import numpy as np
import pandas as pd
import soundfile as sf
import matplotlib.pyplot as plt
import winsound

def ruidoRosa_voss(t, ncols=16, fs=44100):
    
    """
    Genera ruido rosa utilizando el algoritmo de Voss-McCartney(https://www.dsprelated.com/showabstract/3933.php).
    
    .. Nota:: si 'ruidoRosa.wav' existe, este será sobreescrito
    
    Parametros
    ----------
    t : float
        Valor temporal en segundos, este determina la duración del ruido generado.
    ncols: int
        Determina el número de fuentes a aleatorias a agregar.
    fs: int
        Frecuencia de muestreo en Hz de la señal. Por defecto el valor es 44100 Hz.
    
    returns: NumPy array
        Datos de la señal generada.
    
    Ejemplo
    -------
    Generar un `.wav` desde un numpy array de 10 segundos con ruido rosa a una 
    frecuencia de muestreo de 44100 Hz.
    
        import numpy as np
        import soundfile as sf
        from scipy import signal
        
        ruidoRosa_voss(10)
    """
    
    nrows=t*fs
    
    array = np.full((nrows, ncols), np.nan)
    array[0, :] = np.random.random(ncols)
    array[:, 0] = np.random.random(nrows)
    
    # el numero total de cambios es nrows
    n = nrows
    cols = np.random.geometric(0.5, n)
    cols[cols >= ncols] = 0
    rows = np.random.randint(nrows, size=n)
    array[rows, cols] = np.random.random(n)
    
    df = pd.DataFrame(array)
    filled = df.ffill(axis=0)
    total = filled.sum(axis=1)
    
    ## Centrado de el array en 0
    total = total - total.mean()
    
    ## Normalizado
    valor_max = max(abs(max(total)),abs(min(total)))
    total = total / valor_max
    
    # Agregar generación de archivo de audio .wav
    sf.write("ruidoRosa.wav", total, fs)
    
    return total

def graficar_funcion(duracion, fs, signal_1, titulo_1='Señal'):
    """
    Grafica una señal en funcion del tiempo.
    
        Parametros
    ----------
    duracion: float
        Valor temporal en segundos, determinado por la duracion de la señal.
    fs: int
        Frecuencia de muestreo en Hz de la señal.
    signal_1 : NumPy array
        Datos de la señal generada.
    titulo_1: str
        Titulo del grafico. Por defecto es 'Señal'.
    
    returns: 
        Grafico de la señal respecto del tiempo.
    """
    t = np.arange(0, duracion, 1/fs)
    
    # signal_1 = signal_1 / np.max(np.abs(signal_1)) # Normalización

    plt.figure(figsize=(10, 6))
    plt.plot(t, signal_1, '.')
    plt.title(titulo_1)
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.show()

if __name__ == "__main__":
    # Generar ruido rosa
    prueba = ruidoRosa_voss(10, ncols=16, fs=44100)
    
    # Graficar la señal generada
    graficar_funcion(10, 44100, prueba, 'Ruido Rosa Voss')
    
    # Reproducir el sonido generado (opcional)
    winsound.PlaySound("ruidoRosa.wav", winsound.SND_FILENAME)



