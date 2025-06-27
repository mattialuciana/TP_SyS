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
    
    min_length = min(len(t), len(señal))
    t = t[:min_length]
    
    señal = señal[:min_length]
    A = np.sum(t)
    B = np.sum(señal)
    C = np.sum(t**2)
    D = np.sum(t * señal)

    b = (B - (D*A)/C)/(len(t) - (A**2)/C)
    m = (D - b*A)/C
    f = m*t + b
    
    return f, m, b

def cuadrados_minimos_gen(x, y):
    """
    Ajusta una línea recta a los datos (x, y) usando el método de mínimos cuadrados.
    Devuelve la pendiente (m) y la intersección (b) de la línea ajustada.
    Parámetros:
    x : array
        Valores de la variable independiente.
    y : array
        Valores de la variable dependiente.
    Devuelve:
    f : array   
        Valores de la función ajustada.
    m : float
        Pendiente de la recta ajustada.
    b : float
        Intersección de la recta ajustada con el eje y.
    """

    A = np.sum(x)
    B = np.sum(y)
    C = np.sum(x**2)
    D = np.sum(x * y)

    b = (B - (D*A)/C)/(len(x) - (A**2)/C)
    m = (D - b*A)/C
    f = m*x + b

    return f, m, b
