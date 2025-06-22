import numpy as np

def cuadrados_minimos(señal, fs=44100):
    """
    Ajusta una línea recta a los datos usando el método de mínimos cuadrados.

    Parámetros:        
    señal : array
        Señal a aproximar

    Devuelve:
    f : 
        Recta
    
    m : float
        Pendiente
    
    b : float
        Ordenada al origen
    """
    
    t = np.arange(0, len(señal)/fs, 1/fs)
    
    A = np.sum(t)
    B = np.sum(señal)
    C = np.sum(t**2)
    D = np.sum(t * señal)

    b = (B - (D*A)/C)/(len(t) - (A**2)/C)
    m = (D - b*A)/C
    f = m*t + b
    
    return f, m, b


