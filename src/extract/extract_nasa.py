import os
import logging
import requests

def extraer_datos_api(url_api, parametros, ruta_destino):
    """
    Extrae datos en CSV de la API de NASA POWER y los guarda en Bronze.
    """
    try:
        logging.info(f"Conectando a NASA POWER: {url_api}")
        response = requests.get(url_api, params=parametros)
        response.raise_for_status()
        
        os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)
        
        with open(ruta_destino, 'wb') as f:
            f.write(response.content)
            
        logging.info(f"✅ Datos descargados en: {ruta_destino}")
        return ruta_destino
        
    except Exception as e:
        logging.error(f"❌ Error al extraer datos de la API: {e}")
        return None