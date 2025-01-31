KEY = "YOUR_API_KEY"
OUTPUT_DIR = 'imagenes_satelitales_google_maps'

LAT_MIN = 23.1000 
LON_MIN = -82.4100  
LAT_MAX = 23.1600  
LON_MAX = -82.3400

# Directorios de entrada y salida
BASE_DIR = 'outputs'
INPUT_DIR = f'{BASE_DIR}/imagenes_satelitales_google_maps'
OUTPUT_DIR = f'{BASE_DIR}/imagenes_con_circulos'
OUTPUT_CSV = f'{BASE_DIR}/detecciones.csv'

# IDs de modelos de detección disponibles
MODEL_IDS = {
    "Robot Train": "710robotrain/3",
    "Círculos Geométricos": "circulos-gcomj/31",
    "Google Earth Tomb (Automático)": "googleearthtomb/12"
}

# Modelo predeterminado (último)
MODEL_SELECTED = "googleearthtomb/12"