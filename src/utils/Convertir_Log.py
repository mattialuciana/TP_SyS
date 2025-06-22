import numpy as np

def convertir_log(señal):
    """
    Convierte una señal de audio a escala logarítmica.

    Parámetros:
    - señal (numpy array): señal de audio a convertir.

    Devuelve:
    - señal_log (numpy array): señal convertida a escala logarítmica.
    """
    
    señal = np.abs(señal)
    señal = np.clip(señal, 1e-10, None)
    señal_log = 20 * np.log10(señal / np.max(señal))

    return señal_log