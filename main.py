import sys
import os
import logging
import datetime
import psutil
import yaml

# Nos aseguramos que la ruta src sea reconocida
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from extract.extract_nasa import extraer_datos_api
from transform.transform_datos import transformar_nasa

# Cargamos la configuración desde YAML
with open("config/config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

# Configuramos los Logs
os.makedirs(config["paths"]["logs"], exist_ok=True)
log_path = os.path.join(config["paths"]["logs"], "pipeline.log")

logging.basicConfig(
    level=getattr(logging, config["execution"]["log_level"]),
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

def ejecutar_pipeline_completo():
    try:
        nombre_equipo = os.getlogin()
    except:
        nombre_equipo = "Desconocido"
        
    ruta_ejecucion = os.path.abspath(__file__)
    ram_uso = psutil.virtual_memory().percent
    
    try:
        temp_uso = f"{psutil.sensors_temperatures()['coretemp'][0].current}°C"
    except Exception:
        temp_uso = "N/A"
        
    # Registrar apertura en logs.txt
    with open(os.path.join(config["paths"]["logs"], 'logs.txt'), 'a', encoding='utf-8') as log_file:
        log_file.write(f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')};Abriendo Orquestador ETL;{nombre_equipo};{ruta_ejecucion};RAM:{ram_uso}%;Temp:{temp_uso}\n")

    logging.info("=======================================================")
    logging.info(f"   INICIANDO PIPELINE: {config['project_name']} ")
    logging.info("=======================================================")
    
    # URL de la API
    url_api = config["api"]["url"]
    
    # Las cuatro ciudades con sus coordenadas
    ciudades = {
        "cali": {"lat": 3.4372, "lon": -76.5220},
        "bogota": {"lat": 4.7110, "lon": -74.0721},
        "barranquilla": {"lat": 10.9685, "lon": -74.7813},
        "medellin": {"lat": 6.2442, "lon": -75.5812}
    }
    
    # [CAPA BRONZE - NASA]
    logging.info("[1/2] Bronze: extracción NASA por ciudad...")
    rutas_nasa = {}
    
    for ciudad, coord in ciudades.items():
        parametros = {
            "parameters": "ALLSKY_SFC_SW_DWN,T2M,PRECTOTCORR",
            "community": "RE",
            "longitude": coord["lon"],
            "latitude": coord["lat"],
            "start": "20210101",
            "end": "20241231",
            "format": "CSV"
        }
        
        ruta = f"data/bronze/nasa_{ciudad}_raw.csv"
        
        if extraer_datos_api(url_api, parametros, ruta) is None:
            logging.error(f" Error extrayendo {ciudad}.")
            return
            
        rutas_nasa[ciudad] = ruta

    # [CAPA SILVER - NASA]
    logging.info("[2/2] Silver: limpieza y separación de datos NASA...")
    carpeta_silver_nasa = "data/silver"
    
    rutas_silver_nasa = transformar_nasa(rutas_nasa, carpeta_silver_nasa)
    if rutas_silver_nasa is None:
        logging.error(" Error limpiando los datos de la NASA en Silver.")
        return

    logging.info("_______________________________________________________")
    logging.info("       ¡EXTRACCIÓN Y LIMPIEZA CON ÉXITO!       ")
    logging.info("_______________________________________________________")
    
    # Registrar cierre
    ram_uso_fin = psutil.virtual_memory().percent
    with open(os.path.join(config["paths"]["logs"], 'logs.txt'), 'a', encoding='utf-8') as log_file:
        log_file.write(f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')};Cerrando Orquestador ETL;{nombre_equipo};{ruta_ejecucion};RAM:{ram_uso_fin}%;Temp:{temp_uso}\n")

if __name__ == "__main__":
    ejecutar_pipeline_completo()