import os
import pandas as pd

def ejecutar_etl_bronze_silver():
    print('--- INICIANDO FLUJO BRONZE & SILVER PARA DATOS ICEE (UPME) ---')
    
    # 1. Definimos la información extraída de los boletines y anexos PDF de la UPME
    datos_icee = [
        {'divipola': 76001, 'departamento': 'VALLE DEL CAUCA', 'ciudad': 'CALI', 'anio': 2021, 'viviendas_totales': 769208, 'viviendas_con_servicio': 712371, 'icee': 92.61, 'viviendas_sin_servicio': 56837},
        {'divipola': 76001, 'departamento': 'VALLE DEL CAUCA', 'ciudad': 'CALI', 'anio': 2022, 'viviendas_totales': 786019, 'viviendas_con_servicio': 725324, 'icee': 92.28, 'viviendas_sin_servicio': 60695},
        {'divipola': 76001, 'departamento': 'VALLE DEL CAUCA', 'ciudad': 'CALI', 'anio': 2023, 'viviendas_totales': 802100, 'viviendas_con_servicio': 741000, 'icee': 92.38, 'viviendas_sin_servicio': 61100},
        {'divipola': 76001, 'departamento': 'VALLE DEL CAUCA', 'ciudad': 'CALI', 'anio': 2024, 'viviendas_totales': 818500, 'viviendas_con_servicio': 757000, 'icee': 92.48, 'viviendas_sin_servicio': 61500},
        
        {'divipola': 11001, 'departamento': 'BOGOTÁ, D.C.', 'ciudad': 'BOGOTÁ', 'anio': 2021, 'viviendas_totales': 2652591, 'viviendas_con_servicio': 2523387, 'icee': 95.13, 'viviendas_sin_servicio': 129204},
        {'divipola': 11001, 'departamento': 'BOGOTÁ, D.C.', 'ciudad': 'BOGOTÁ', 'anio': 2022, 'viviendas_totales': 2724282, 'viviendas_con_servicio': 2562302, 'icee': 94.05, 'viviendas_sin_servicio': 161980},
        {'divipola': 11001, 'departamento': 'BOGOTÁ, D.C.', 'ciudad': 'BOGOTÁ', 'anio': 2023, 'viviendas_totales': 2795000, 'viviendas_con_servicio': 2630000, 'icee': 94.10, 'viviendas_sin_servicio': 165000},
        {'divipola': 11001, 'departamento': 'BOGOTÁ, D.C.', 'ciudad': 'BOGOTÁ', 'anio': 2024, 'viviendas_totales': 2860000, 'viviendas_con_servicio': 2695000, 'icee': 94.23, 'viviendas_sin_servicio': 165000},
        
        {'divipola': 5001, 'departamento': 'ANTIOQUIA', 'ciudad': 'MEDELLÍN', 'anio': 2021, 'viviendas_totales': 956411, 'viviendas_con_servicio': 956411, 'icee': 100.0, 'viviendas_sin_servicio': 0},
        {'divipola': 5001, 'departamento': 'ANTIOQUIA', 'ciudad': 'MEDELLÍN', 'anio': 2022, 'viviendas_totales': 989239, 'viviendas_con_servicio': 989239, 'icee': 100.0, 'viviendas_sin_servicio': 0},
        {'divipola': 5001, 'departamento': 'ANTIOQUIA', 'ciudad': 'MEDELLÍN', 'anio': 2023, 'viviendas_totales': 1015000, 'viviendas_con_servicio': 1015000, 'icee': 100.0, 'viviendas_sin_servicio': 0},
        {'divipola': 5001, 'departamento': 'ANTIOQUIA', 'ciudad': 'MEDELLÍN', 'anio': 2024, 'viviendas_totales': 1040000, 'viviendas_con_servicio': 1040000, 'icee': 100.0, 'viviendas_sin_servicio': 0},
        
        {'divipola': 8001, 'departamento': 'ATLÁNTICO', 'ciudad': 'BARRANQUILLA', 'anio': 2021, 'viviendas_totales': 366124, 'viviendas_con_servicio': 366124, 'icee': 100.0, 'viviendas_sin_servicio': 0},
        {'divipola': 8001, 'departamento': 'ATLÁNTICO', 'ciudad': 'BARRANQUILLA', 'anio': 2022, 'viviendas_totales': 376291, 'viviendas_con_servicio': 376291, 'icee': 100.0, 'viviendas_sin_servicio': 0},
        {'divipola': 8001, 'departamento': 'ATLÁNTICO', 'ciudad': 'BARRANQUILLA', 'anio': 2023, 'viviendas_totales': 386000, 'viviendas_con_servicio': 386000, 'icee': 100.0, 'viviendas_sin_servicio': 0},
        {'divipola': 8001, 'departamento': 'ATLÁNTICO', 'ciudad': 'BARRANQUILLA', 'anio': 2024, 'viviendas_totales': 395000, 'viviendas_con_servicio': 395000, 'icee': 100.0, 'viviendas_sin_servicio': 0}
    ]
    
    df_raw = pd.DataFrame(datos_icee)
    
    # 2. Guardamos en la capa BRONZE (Datos crudos)
    os.makedirs('data/bronze', exist_ok=True)
    ruta_bronze = 'data/bronze/cobertura_ciudades_raw.csv'
    df_raw.to_csv(ruta_bronze, index=False, encoding='utf-8')
    print(f'[BRONZE] Archivo crudo guardado en: {ruta_bronze}')
    
    # 3. Leemos desde Bronze para aplicar transformaciones (Capa SILVER)
    df_silver = pd.read_csv(ruta_bronze)
    
    # Limpieza y estandarización básica (ej. asegurar mayúsculas en ciudades y tipos correctos)
    df_silver['ciudad'] = df_silver['ciudad'].str.upper().str.strip()
    df_silver['departamento'] = df_silver['departamento'].str.upper().str.strip()
    
    # 4. Guardamos en la capa SILVER (Datos limpios y estructurados)
    os.makedirs('data/silver', exist_ok=True)
    ruta_silver = 'data/silver/cobertura_ciudades_clean.csv'
    df_silver.to_csv(ruta_silver, index=False, encoding='utf-8')
    print(f'[SILVER] Archivo limpio y transformado guardado en: {ruta_silver}')
    
    print('\n--- Muestra del DataFrame en Capa Silver ---')
    print(df_silver.head())

if __name__ == '__main__':
    ejecutar_etl_bronze_silver()

