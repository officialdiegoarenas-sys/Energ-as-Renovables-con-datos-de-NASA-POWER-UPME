import os
import logging
import pandas as pd

def transformar_nasa(lista_rutas, carpeta_silver):
    #Limpiamos los CSV crudos de la NASA para cada ciudad de forma individual y los guardamos en la capa de  Silver
    try:
        logging.info("Iniciando transformación de datos NASA (Capa Silver)...")
        os.makedirs(carpeta_silver, exist_ok=True)
        archivos_generados = {}
        
        for ciudad, ruta_bronze in lista_rutas.items():
            # Leemos las líneas para saltar los metadatos de la NASA
            with open(ruta_bronze, "r", encoding="utf-8") as f:
                lineas = f.readlines()
                
            fila_inicio = 0
            for i, linea in enumerate(lineas):
                if "-END HEADER-" in linea:
                    fila_inicio = i + 1
                    break
                    
            # Cargamos el dataframe saltando el encabezado
            df = pd.read_csv(ruta_bronze, skiprows=fila_inicio)
            
            # Agregamos la columna ciudad en mayúsculas
            df["ciudad"] = ciudad.upper()
            
            # NASA usa -999 para faltantes: se converten  a nulos reales
            df = df.replace(-999, pd.NA)
            
            #Eliminando duplicados si existen
            df = df.drop_duplicates()
            
            # Renombramos las  columnas a nombres claros
            df = df.rename(columns={
                "ALLSKY_SFC_SW_DWN": "radiacion_solar",
                "T2M": "temperatura",
                "PRECTOTCORR": "precipitacion"
            })
            
            # Crearmos la  columna de la fecha unificada
            df["fecha"] = pd.to_datetime(
                df["YEAR"].astype(str) + "-" + df["MO"].astype(str) + "-" + df["DY"].astype(str),
                errors="coerce"
            )
            
            # Rellenamos los  nulos con el promedio de cada variable
            for col in ["radiacion_solar", "temperatura", "precipitacion"]:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
                    df[col] = df[col].fillna(df[col].mean())
                    
            # Guardamos un archivo independiente por ciudad en Silver
            ruta_salida = os.path.join(carpeta_silver, f"nasa_{ciudad}_clean.csv")
            df.to_csv(ruta_salida, index=False, encoding="utf-8")
            
            archivos_generados[ciudad] = ruta_salida
            logging.info(f" NASA {ciudad.upper()} limpio guardado en Silver ({df.shape[0]} filas).")
            
        return archivos_generados
        
    except Exception as e:
        logging.error(f" Error transformando datos NASA: {e}")
        return None

def transformar_cobertura_upme():

    # Limpiamos y estandarizamos los datos crudos de cobertura eléctrica (UPME) desde Bronze hacia Silver
    try:
        logging.info("Iniciando transformación de datos de Cobertura UPME (Capa Silver)...")
        ruta_bronze = "data/bronze/cobertura_ciudades_raw.csv"
        
        if not os.path.exists(ruta_bronze):
            logging.error(f" No se encontró el archivo crudo en: {ruta_bronze}")
            return None
            
        df = pd.read_csv(ruta_bronze)
        
        # Estandarizamos los textos a mayúsculas y quitamos los  espacios en blanco laterales
        df['ciudad'] = df['ciudad'].str.upper().str.strip()
        df['departamento'] = df['departamento'].str.upper().str.strip()
        
        # Verificamos y rellenamos los valores nulos o vacíos

        # Si no hay registro de viviendas sin servicio, asumimos 0

        df['viviendas_sin_servicio'] = df['viviendas_sin_servicio'].fillna(0)

        # Si falta el porcentaje ICEE, rellenamos con el promedio para no dañar los cálculos

        df['icee'] = df['icee'].fillna(df['icee'].mean())
        
        # Eliminamos las filas que estan duplicadas

        df = df.drop_duplicates()
        
        # Aca se guardan en la capa Silver
        os.makedirs("data/silver", exist_ok=True)
        ruta_salida = "data/silver/cobertura_ciudades_clean.csv"
        df.to_csv(ruta_salida, index=False, encoding="utf-8")
        
        logging.info(f" Datos de Cobertura UPME limpios guardados en Silver ({df.shape[0]} filas).")
        return ruta_salida
        
    except Exception as e:
        logging.error(f" Error transformando datos de Cobertura UPME: {e}")
        return None