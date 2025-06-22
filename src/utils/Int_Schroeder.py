import numpy as np
import scipy.signal as signal

def integral_schroeder(señal, t, fs=44100):
    """
    Calcula la función integral de Schroeder usando la forma equivalente:
        E(t) = integral total - integral acumulada hasta t

    Parámetros:
        señal: array de la respuesta impulsional p(t)
        fs: frecuencia de muestreo (Hz)

    Retorna:
        E: array con el decaimiento de energía acumulada (función de Schroeder)
        t: array de tiempo correspondiente
    """
  
    impulso_corto = señal[0:round(t*fs)]
    integral_sch = np.cumsum(impulso_corto[::-1]**2)/np.sum(señal**2)

    E = integral_sch[::-1]  # Invertir para que E(t) decrezca
    
    return 10 * np.log10(E)
    

def ventana(señal, inicio, final):
    
    """
    Ventanea la señal en el rango de inicio y final especificado. 
    Parámetros:
    - señal (array): la señal a ventanear.
    - inicio (float): valor inicial del rango.
    - final (float): valor final del rango.
    Devuelve:
    - data (array): la señal ventaneada.
    - Inicio (int): índice del primer elemento en el rango.
     
    """  

    
    # Buscar el índice del primer elemento
    for i in range(len(señal)):
        if señal[i] <= inicio:
            Inicio = i
            break

    # Buscar el índice del primer elemento mayor o igual a final_value desde el final del array
    for i in range(len(señal)):
        if señal[i] <= final:
            Final = i
            break

    

    return señal[Inicio:Final+1], Inicio