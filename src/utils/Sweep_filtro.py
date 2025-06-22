import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import winsound

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

if __name__ == "__main__":
    
    barrido, filtro = sweep_filtro(10, 20, 20000)
    winsound.PlaySound("sine_sweep.wav", winsound.SND_FILENAME)
    winsound.PlaySound("filtro.wav", winsound.SND_FILENAME)
    
    # Graficar 
    t = np.arange(0, len(barrido)) / 44100 
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t, barrido)
    plt.title('Barrido')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    
    plt.subplot(2, 1, 2)
    plt.plot(t, filtro)
    plt.title('Filtro Inverso')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    
    plt.tight_layout()
    plt.show()
