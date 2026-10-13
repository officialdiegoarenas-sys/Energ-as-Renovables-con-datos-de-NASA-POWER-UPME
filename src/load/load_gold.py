import os
import logging
import pandas as pd

def generar_capa_gold():
    # Integra los datos de NASA y UPME (Silver) para generar el dataset analítico (Gold)
    try:
        logging.info("Iniciando generación de Capa Gold (Integración de datos)...")
        
        ruta_upme = "data/silver/cobertura_ciudades_clean.csv"
        if not os.path.exists(ruta_upme):
            logging.error(f"Falta el archivo de UPME en Silver: {ruta_upme}")
            return None
            
        # Cargarmos los  datos UPME
        df_upme = pd.read_csv(ruta_upme)
        
        # Cargarmos los datos NASA (leemos todos los archivos nasa_clean.csv que haya en silver)
        lista_df_nasa = []
        if os.path.exists("data/silver"):
            archivos_silver = os.listdir("data/silver")
            archivos_nasa = [f for f in archivos_silver if f.startswith("nasa_") and f.endswith("_clean.csv")]
            
            for arch in archivos_nasa:
                df_temp = pd.read_csv(os.path.join("data/silver", arch))
                lista_df_nasa.append(df_temp)
                
        if not lista_df_nasa:
            logging.error("No se encontraron archivos de NASA en la capa Silver.")
            return None
            
        df_nasa_total = pd.concat(lista_df_nasa, ignore_index=True)
        
        # Se esta haciendo una transformación para el Cruce (Agrupamos clima de la NASA por Año)
        # Extraemos el año de la fecha
        df_nasa_total['YEAR'] = pd.to_datetime(df_nasa_total['fecha']).dt.year
        
        # Creamos una columna temporal de cruce sin tildes para evitar errores de JOIN

        df_nasa_total['ciudad_cruce'] = df_nasa_total['ciudad'].str.upper().str.replace('Á', 'A').str.replace('É', 'E').str.replace('Í', 'I').str.replace('Ó', 'O').str.replace('Ú', 'U')
        df_upme['ciudad_cruce'] = df_upme['ciudad'].str.upper().str.replace('Á', 'A').str.replace('É', 'E').str.replace('Í', 'I').str.replace('Ó', 'O').str.replace('Ú', 'U')
        
        # Es el Promedio anual de clima por ciudad
        nasa_anual = df_nasa_total.groupby(['ciudad_cruce', 'YEAR'])[['radiacion_solar', 'temperatura', 'precipitacion']].mean().reset_index()
        nasa_anual = nasa_anual.rename(columns={'YEAR': 'anio'})
        
        # Integración (JOIN): Unimos UPME y NASA
        df_gold = pd.merge(df_upme, nasa_anual, on=['ciudad_cruce', 'anio'], how='left')
        
        # Eliminamos la columna de cruce temporal que ya no necesitamos
        df_gold = df_gold.drop(columns=['ciudad_cruce'])
        
        # Guardamos el archivo final integrado en la Capa Gold
        os.makedirs("data/gold", exist_ok=True)
        ruta_gold = "data/gold/gold_final.csv"
        df_gold.to_csv(ruta_gold, index=False, encoding="utf-8")
        
        logging.info(f"Capa Gold generada exitosamente en: {ruta_gold}")
        print("\n--- ¡CAPA GOLD GENERADA EXITOSAMENTE! ---")
        print(f"Archivo final guardado en: {ruta_gold}\n")
        print(df_gold.head())
        
        # ________________________________________________________________
        # INSTRUCCIÓN DEL PROFE PARA LA ETAPA DE CARGA A BASE DE DATOS
        # ________________________________________________________________
        # aca dejamos el proceso de carga, pero no lo hacemos por el momento.
        
        return ruta_gold
        
    except Exception as e:
        logging.error(f"Error en la generación de la capa Gold: {e}")
        return None

if __name__ == '__main__':
    # Configuración básica de log para verlo en consola
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    generar_capa_gold()