from utils.Parametros import C80, D50, T_Reverberacion
from utils.Cargar_Audios import cargar_audios_por_tipo
from utils.Cuadrados_min import cuadrados_minimos
from utils.Filtros import filtro
from utils.Convertir_Log import convertir_log
from utils.Suavizado import suavizado
from utils.Int_Schroeder import integral_schroeder, ventana

def Main(titulo=None, T=30, banda="octavas", fs=44100):
    RI = cargar_audios_por_tipo({"RI": [titulo]})
    
    # Bandas de frecuencias sobre las que se calculan los parámetros acústicos

    if banda == "octavas":
        frec_c = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
    elif banda == "tercios":
        frec_c = [25,31.5,40,50,63,80,100,125,160,200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000,6300,8000,10000,12500,16000,20000]
    
    lista_filtros = []

    # Filtro según banda definido por la norma IEC61260

    for i in range(len(frec_c)):
        fi = filtro(banda, RI["RI"][0][0], fs)[i]
        lista_filtros.append(fi)

    EDT = []

    T10 = []

    T20 = []

    T30 = []

    D_50 = []

    C_80 = []


    for i in range(len(lista_filtros)): 
        
        PM = suavizado(lista_filtros[i],30) # Transformada de Hilbert y Filtro de promedio movil2
        
        integral_de_schroeder = integral_schroeder(PM, fs) # Integral de Schroeder

        # integral_ventaneada,I = ventana(integral_de_schroeder,0, -35) # Ventaneo

        # recta, t, a0, a1 = cuadrados_minimos(integral_ventaneada) # Regresión lineal por mínimos cuadrados
        
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
    
    IR2 = Main("src\SintesisRtaImpulso(2).wav")

    f_centrales= IR2[0]
    EDT = IR2[1]
    T10 = IR2[2]
    T20 = IR2[3]
    T30 = IR2[4]
    D_50 = IR2[5]
    C_80 = IR2[6]

    """
    print("Las frecuencias centrales son:", f_centrales)
    print("EDT:", EDT)
    print("T10:", T10)
    print("T20:", T20)
    print("T30:", T30)
    print("D_50:", D_50)
    print("C_80:", C_80)
    """
    print("Las frecuencias centrales son:", f_centrales)
    print("EDT:", [f"{float(val):.4f}s" for val in EDT])
    print("T10:", [f"{float(val):.4f}s" for val in T10])
    print("T20:", [f"{float(val):.4f}s" for val in T20])
    print("T30:", [f"{float(val):.4f}s" for val in T30])
    print("D_50:", [f"{float(val):.4f}%" for val in D_50])
    print("C_80:", [f"{float(val):.4f} dB" for val in C_80])

