import numpy as np

def convertir_log(señal):
    """
    Convierte una señal de audio a escala logarítmica.

    Parámetros:
    - señal (numpy array): señal de audio a convertir.

    Devuelve:
    - señal_log (numpy array): señal convertida a escala logarítmica.
    """
    
    # Evitar log(0) y valores negativos
    señal = np.clip(señal, 1e-10, None)
    
    # Convertir a escala logarítmica
    señal_log = 20 * np.log10(np.abs(señal/np.max(señal)))
        
    return señal_log