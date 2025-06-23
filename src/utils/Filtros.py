import numpy as np
import scipy.signal as signal

def filtro(bandas, señal, fs=44100):
    
    """
    Aplica un filtro de banda a una señal de audio.

    Parámetros:
    - bandas (str): tipo de bandas de frecuencia ('octavas' o 'tercios').
    - señal (numpy array): señal de audio a filtrar.
    - fs (int): frecuencia de muestreo en Hz (por defecto 44100).

    Devuelve:
    - lista_filtros (list): lista de señales filtradas.
    """
    
    if bandas == "octavas":
        frecuencias = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000] 
        G = 1.0/2.0
    elif bandas == "tercios":
        frecuencias = [25,31.5,40,50,63,80,100,125,160,200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000,6300,8000,10000,12500,16000,20000] 
        G = 1.0/6.0
    
    lista_filtros = []
    for i in range(len(frecuencias)):
        factor = np.power(2, G)
        centerFrequency_Hz = frecuencias[i]
        
        # Calculo los extremos de la banda a partir de la frecuencia central
        lowerCutoffFrequency_Hz = centerFrequency_Hz / factor
        upperCutoffFrequency_Hz = centerFrequency_Hz * factor
        
        if upperCutoffFrequency_Hz >= (fs/2): # Para no alcanzar ni superar la frecuencia máxima del Teo. del Muestreo
            upperCutoffFrequency_Hz = (fs/2) - 1
        # Extraemos los coeficientes del filtro 
        b,a = signal.iirfilter(4, [2*np.pi*lowerCutoffFrequency_Hz,2*np.pi*upperCutoffFrequency_Hz],
                            rs=60, btype='band', analog=True,
                            ftype='butter') 

        # para aplicar el filtro es más óptimo
        sos = signal.iirfilter(4, [lowerCutoffFrequency_Hz,upperCutoffFrequency_Hz],
                            rs=60, btype='band', analog=False,
                            ftype='butter', fs=fs, output='sos') 
        w, h = signal.freqs(b,a)

        # aplicando filtro al audio
        filt = signal.sosfilt(sos, señal)
        lista_filtros.append(filt)
        
    return lista_filtros

