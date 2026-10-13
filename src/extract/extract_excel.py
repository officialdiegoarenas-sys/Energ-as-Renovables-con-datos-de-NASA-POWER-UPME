import os
import logging
import pandas as pd

def extraer_datos_excel(ruta_origen, ruta_destino):
    
    #Leemos el archivo de excel original y lo guarda como un archivo CSV en la capa Bronze.
    
    try:
        logging.info(f"Leyendo archivo Excel desde: {ruta_origen}")
        
        # Leer el Excel (asegúrate de tener instalada la librería openpyxl)
        df = pd.read_excel(ruta_origen)
        
        # Crear la carpeta destino si no existe
        os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)
        
        # Guardamos en Bronze como un archivo CSV estandarizado
        df.to_csv(ruta_destino, index=False, encoding="utf-8")
        
        logging.info(f" Excel extraído y guardado en Bronze: {ruta_destino}")
        return ruta_destino
        
    except Exception as e:
        logging.error(f" Error al extraer el Excel: {e}")
        return None