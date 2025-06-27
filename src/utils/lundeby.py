import numpy as np
from .Cargar_Audios import cargar_audios_por_tipo
from .Cuadrados_min import cuadrados_minimos_gen
from .Suavizado import suavizado

def lundeby(ri, fs, bloque_tiempo=0.03, intervalos=3, max_iter=7):
    """
    Implementación del método de Lundeby para calcular el tiempo óptimo de la integral de Schroeder. Itera
    hasta 7 veces y tiene una tolerancia de convergencia de 0.01 segundos.

    Parameters:
    - ri: np.ndarray, respuesta impulsiva (1D)
    - fs: float, frecuencia de muestreo (Hz)
    - bloque_tiempo: float, duración del bloque de tiempo para el análisis (segundos). Por defecto 0.03 
    segundos (30 ms).
    - intervalos: int, número de intervalos cada 10dB para el análisis. Por defecto 3.
    - max_iter: int, número máximo de iteraciones para encontrar el tiempo de cruce. Por defecto 7.

    Returns:
    - t_cruce: float, tiempo en segundos donde la energía cae al nivel de ruido
    """

    # Se eleva la señal al cuadrado para facilitar
    energia = ri ** 2
    
    # División de la señal en bloques
    bloque_tam = int(bloque_tiempo * fs)
    num_bloques = len(energia) // bloque_tam
    energia_recortada = energia[:num_bloques * bloque_tam]
    bloques = energia_recortada.reshape(num_bloques, bloque_tam)

    # Calcula la media cuadrática de cada bloque y convierte a dB
    rms_bloques = np.sqrt(np.mean(bloques, axis=1))
    bloque_db = 10 * np.log10(rms_bloques + 1e-20)
    times = np.arange(num_bloques) * bloque_tiempo

    # Estimación inicial del piso de ruido con el último 10% de la RI
    ruido = np.mean(rms_bloques[-int(num_bloques * 0.1):])
    ruido_dB = 10 * np.log10(ruido + 1e-20)

    # Se define un umbral, 10dB por encima del ruido
    umbral = ruido_dB + 10

    # Regresión lineal por cuadrados mínimos inicial
    peak_idx = np.argmax(bloque_db)
    try:
        end_idx = np.where(bloque_db[peak_idx:] < umbral)[0][0] + peak_idx
    except IndexError:
        raise ValueError("No se encuentra tramo válido para regresión inicial.")

    x = times[peak_idx:end_idx]
    y = bloque_db[peak_idx:end_idx]
    _, m, b = cuadrados_minimos_gen(x, y)
    
    # Primera estimación del tiempo de cruce
    t_cruce = (ruido_dB - b) / m
    previo = t_cruce

    # Comienza a iterar 
    for i in range(0, max_iter):

        # Definir nuevo intervalo basado en la pendiente
        interval_dB = 10 / intervalos
        intervalo_muestras = int(-interval_dB / m * fs)
        if intervalo_muestras < 1:
            intervalo_muestras = 1
        bloque_tiempo = intervalo_muestras / fs

        # Nuevos bloques para nuevo suavizado
        bloque = int(bloque_tiempo * fs)
        num_bloques = len(energia) // bloque
        energy_recortada = energia[:num_bloques * bloque]
        bloques = energy_recortada.reshape(num_bloques, bloque)
        rms_bloques = np.sqrt(np.mean(bloques, axis=1))
        bloque_db = 10 * np.log10(rms_bloques + 1e-20)
        times = np.arange(num_bloques) * bloque_tiempo

        # Recalcular ruido
        idx_cruce_aprox = int(t_cruce / bloque_tiempo)
        tail = int(num_bloques * 0.1)

        # Para asegurar que el ruido no corresponda a menos del 10% de la RI
        if idx_cruce_aprox < num_bloques - tail:
            ruido_dB = np.mean(bloque_db[idx_cruce_aprox:])
        else:
            ruido_dB = np.mean(bloque_db[-tail:])

        # Nuevo tramo para regresión lineal. Rango dinámico de 15 dB        
        ini = (ruido_dB + 10 - b) / m
        fin = (ruido_dB - 5 - b) / m
        ini_idx = int(ini / bloque_tiempo)
        fin_idx = int(fin / bloque_tiempo)
        if ini_idx >= len(times) or fin_idx <= ini_idx:
            break
        x = times[ini_idx:fin_idx]
        y = bloque_db[ini_idx:fin_idx]
        _, m, b = cuadrados_minimos_gen(x, y)
        t_cruce = (ruido_dB - b) / m

        # Imprimir información de la iteración para alguna prueba
        # print(f"Iteración {i+1}: t_cruce = {t_cruce:.6f}, previo = {previo:.6f}, Δ = {abs(t_cruce - previo):.6f}") 

        # Busca la convergencia con una tolerancia de 0.01 segundos de diferencia con el cálculo anterior
        if abs(t_cruce - previo) < 10 ** -2:  
            # print(f"Iteración {i+1}: convergencia alcanzada.") # Está bueno para cuando se ejecuta este 
            # modulo pero estorba en el main
            break
        previo = t_cruce
    
    return t_cruce

if __name__ == "__main__":

    data = cargar_audios_por_tipo({"RI": ["src\\SintesisIR1.wav"]})
    suave = suavizado(data["RI"][0][0], 30)
    lim = lundeby(suave, data["RI"][0][1])
    print(f"Tiempo de cruce: {lim:.4f} segundos")