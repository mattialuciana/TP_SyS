from utils.Parametros import C80, D50, T_Reverberacion
from utils.Cargar_Audios import cargar_audios_por_tipo
from utils.Cuadrados_min import cuadrados_minimos
from utils.Filtros import filtro
from utils.Convertir_Log import convertir_log
from utils.Suavizado import suavizado
from utils.Int_Schroeder import integral_schroeder, ventana
from utils.Sweep_filtro import sweep_filtro
from utils.Adq_rep_latencia import adq_rep
from utils.Obtener_RI import respuesta_impulso
from utils.lundeby import lundeby
import sounddevice as sd

def Main(titulo=None, banda="octavas", fs=44100):
    
    """
    Función que permite calcular parametros acústicos de la norma ISO 3382 a partir de una respuesta al 
    impulso grabada o generada.

    Parametros:
    titulo : str, opcional
        Path relativo de la respuesta al impulso grabada. Si no se ingresa, se genera un sine sweep, su 
        filtro inverso y se calcula la respuesta al impulso apartir de su reproducción y grabación
        
    banda : str, opcional
        Tipo de banda de frecuencias a utilizar ('octavas' o 'tercios'). Por defecto 'octavas'

    fs : int, opcional
        Frecuencia de muestreo. Por defecto 44100

    Devuelve:
    frec_c, EDT, T10, T20, T30, D_50, C_80 : listas
        Contienen la información de cada parámetro por banda de frecuencia.
    """

    if titulo == None:
        barrido, filtro_inv = sweep_filtro(10, 20, 20000)
        recording = adq_rep(barrido, fs) 
        sd.wait()
        recording = recording.flatten()
        RI = respuesta_impulso(filtro_inv, recording)
    
    else:
        a = cargar_audios_por_tipo({"RI": [titulo]})
        RI = a["RI"][0][0]
    
    # Bandas de frecuencias sobre las que se calculan los parámetros acústicos

    if banda == "octavas":
        frec_c = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
    elif banda == "tercios":
        frec_c = [25,31.5,40,50,63,80,100,125,160,200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000,6300,8000,10000,12500,16000,20000]
    
    lista_filtros = []

    # Filtro según banda definido por la norma IEC61260

    for i in range(len(frec_c)):
        fi = filtro(banda, RI, fs)[i]
        lista_filtros.append(fi)

    EDT = []

    T10 = []

    T20 = []

    T30 = []

    D_50 = []

    C_80 = []
    

    for i in range(len(lista_filtros)): 
        
        PM = suavizado(lista_filtros[i],30) # Transformada de Hilbert y Filtro de promedio movil2
        
        lim = lundeby(PM, fs) # Método de Lundeby para determinar el tiempo optimo de la integral de Schroeder

        integral_de_schroeder = integral_schroeder(PM, lim) # Integral de Schroeder
   
        T_10 = T_Reverberacion(integral_de_schroeder,-5,-15) #Calculo del T60 a partir del T10
        T10.append(T_10)
        
        T_20 = T_Reverberacion(integral_de_schroeder,-5,-25) #Calculo del T60 a partir del T20
        T20.append(T_20)
        
        T_30 = T_Reverberacion(integral_de_schroeder,-5,-35) #Calculo del T60 a partir del T30
        T30.append(T_30)
        
        EDTi = T_Reverberacion(integral_de_schroeder,-1,-11) #Calculo EDT
        EDT.append(EDTi)
        
        C80i = C80(PM,fs)  #Calculo C80
        C_80.append(C80i)
        
        D50i = D50(PM,fs) #Calculo D50
        D_50.append(D50i)
        
    return frec_c, EDT, T10, T20, T30, D_50, C_80



if __name__ == "__main__":
    
    IR2 = Main("src\\SintesisIR1.wav")

    f_centrales= IR2[0]
    EDT = IR2[1]
    T10 = IR2[2]
    T20 = IR2[3]
    T30 = IR2[4]
    D_50 = IR2[5]
    C_80 = IR2[6]

    print("Las frecuencias centrales son:", f_centrales)
    print("EDT:", [f"{float(val):.4f}s" for val in EDT])
    print("T10:", [f"{float(val):.4f}s" for val in T10])
    print("T20:", [f"{float(val):.4f}s" for val in T20])
    print("T30:", [f"{float(val):.4f}s" for val in T30])
    print("D_50:", [f"{float(val):.4f}%" for val in D_50])
    print("C_80:", [f"{float(val):.4f} dB" for val in C_80]) 