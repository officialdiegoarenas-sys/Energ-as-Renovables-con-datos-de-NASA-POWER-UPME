# Proyecto ETL: Transición a Energías Renovables - NASA POWER & UPME

- Materia: ETL (Extracción, Transformación y Carga)  
- Semestre: Semestre 5  
- Estudiante: Diego Fernando Arenas Lasso 

---------------------------------------------------------------------

# Descripción del Problema y Justificación

El análisis de la transición hacia energías renovables requiere evaluar tanto el (potencial climático natural) como la (realidad de la infraestructura eléctrica). Este proyecto construye un pipeline ETL modular que integra dos fuentes de datos clave para cuatro ciudades estratégicas de Colombia (Cali, Bogotá, Medellín y Barranquilla):

1. API de NASA POWER: Variables meteorológicas (radiación solar, temperatura, precipitación).
2. Datos UPME (Índice de Cobertura de Energía Eléctrica - ICEE): Extraídos de boletines oficiales (PDF convertidos a CSV) para medir el déficit o alcance de la red eléctrica.

El procesamiento se realiza bajo estándares de la arquitectura Medallion (Bronze, Silver, Gold) y gobernanza técnica.

---------------------------------------------------------------------

# Arquitectura del Proyecto (Arquitectura Medallón)

- Capa Bronze (Datos Crudos): Extrae y almacena los archivos originales. Incluye los CSV de la API de la NASA con sus metadatos y la extracción cruda de las tablas de cobertura de la UPME (`cobertura_ciudades_raw.csv`).

- Capa Silver (Datos Limpios): Estructura, estandariza y limpia los datos. Maneja nulos (ej. `-999` en NASA), normaliza nombres de ciudades, unifica formatos de fecha y tipos de datos, generando archivos limpios listos para análisis.

- Capa Gold (Datos Analíticos): Integra (JOIN) ambas fuentes (Clima + Infraestructura) para generar un dataset consolidado (`gold_final.csv`) con indicadores (KPIs) orientados a la toma de decisiones sobre viabilidad de proyectos renovables.

---------------------------------------------------------------------

# Estructura del Repositorio

Parcial_2_ETL/
│
├── config/
│   └── config.yaml             # Configuración centralizada de rutas, API y ejecución
│
├── data/
│   ├── bronze/                 # Datos en bruto extraídos de la API de la NASA y archivos locales
│   │   ├── PDF/
│   │   │   └── Boletin_Calculo_ICEE_2019_2022v3.pdf  # Fuente cruda original UPME (Cobertura eléctrica)
│   │   ├── cobertura_ciudades_raw.csv                # Extracción tabular estructurada desde el PDF
│   │   ├── nasa_barranquilla_raw.csv                 # Descargas directas API NASA
│   │   ├── nasa_bogota_raw.csv
│   │   ├── nasa_cali_raw.csv
│   │   └── nasa_medellin_raw.csv
│   ├── silver/                 # Datos limpios, estandarizados e individuales por ciudad
│   │   ├── cobertura_ciudades_clean.csv              # Datos UPME sin duplicados y formateados
│   │   ├── nasa_barranquilla_clean.csv
│   │   ├── nasa_bogota_clean.csv
│   │   ├── nasa_cali_clean.csv
│   │   └── nasa_medellin_clean.csv
│   └── gold/                   # Modelos analíticos y agregaciones finales
│       └── gold_final.csv                            # JOIN de Clima (NASA) e Infraestructura (UPME)
│
├── logs/                       # Registros de ejecución y auditoría
│   ├── pipeline.log            # Historial del orquestador (niveles INFO/ERROR)
│   └── logs.txt                # Bitácora de hardware, RAM, temperatura y usuario
│
├── notebooks (EDA)/            # Análisis Exploratorio de Datos interactivo
│   ├── 01_exploracion_nasa.ipynb           # Gráficos de dispersión, radiación y temperaturas (Clima)
│   └── 02_analisis_cobertura_icee.ipynb    # EDA sociodemográfico, déficit de viviendas y cobertura
│
├── src/                        # Código fuente modular de la Arquitectura Medallion
│   ├── __init__.py
│   ├── extract/
│   │   ├── __init__.py
│   │   ├── extract_nasa.py     # Conexión y descarga remota desde NASA POWER API (REST)
│   │   ├── extract_PDF.py      # Extracción y estructuración de boletines UPME a CSV
│   │   └── extract_excel.py    # Módulo secundario de respaldo
│   ├── transform/
│   │   ├── __init__.py
│   │   └── transform_datos.py  # Limpieza, imputación de nulos y estandarización para NASA y UPME
│   └── load/
│       ├── __init__.py
│       └── load_gold.py        # Cruce de fuentes (JOIN) y generación de capa Gold (Mock de carga)
│
├── tests/                      # Pruebas unitarias
│   ├── test_extract.py
│   ├── test_quality.py
│   └── test_transform.py
│
├── .env
├── .gitignore
├── evidencias.txt
├── main.py                     # Orquestador principal del Pipeline ETL
├── README.md
└── requirements.txt

# Activar el entorno virtual 

.\venv\Scripts\Activate.ps1

# Instalar dependencias

pip install -r requirements.txt

# Ejecutar el pipeline ETL completo

python main.py
