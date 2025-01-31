import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw
from download_img import descargar_imagenes_en_zona
from draw_bounding_box import procesar_todas_imagenes
import os
from config import OUTPUT_DIR, INPUT_DIR, MODEL_IDS, MODEL_SELECTED

# Configuración inicial
if not os.path.exists(INPUT_DIR):
    os.makedirs(INPUT_DIR)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Configuración de la aplicación
st.title("Aplicación de Descarga de Imágenes Satelitales")
st.write("Dibuja un rectángulo en el mapa para seleccionar el área.")

# --- Barra lateral ---
st.sidebar.header("Controles de la Aplicación")

# Mapa interactivo
m = folium.Map(location=[23.1200, -82.3830], zoom_start=12)
output_dir = OUTPUT_DIR
input_dir = INPUT_DIR

# Añadir la herramienta de dibujo limitada a rectángulos y borrar
draw = Draw(
    draw_options={
        'polyline': False,
        'polygon': False,
        'circle': False,
        'circlemarker': False,
        'marker': False,
        'rectangle': True
    },
    edit_options={'edit': False, 'remove': True}
)
draw.add_to(m)

# Mostrar el mapa interactivo
map_data = st_folium(m, width=800, height=500)

# --- API Key ---
st.sidebar.write("### Configuración de la API de Google Maps")
api_key = st.sidebar.text_input("API Key:", "YOUR_API_KEY")

# --- Selección del modelo ---
st.sidebar.write("### Selección del modelo de detección")
modelo_seleccionado = st.sidebar.selectbox(
    "Selecciona el modelo para detectar objetos:",
    options=list(MODEL_IDS.keys()),
    index=list(MODEL_IDS.keys()).index("Google Earth Tomb (Automático)")  # Por defecto el último
)
MODEL_SELECTED = MODEL_IDS[modelo_seleccionado]

# --- Captura de coordenadas desde el mapa ---
if map_data and map_data.get("last_active_drawing"):
    drawing = map_data["last_active_drawing"]

    if drawing["geometry"]["type"] == "Polygon":
        coordinates = drawing["geometry"]["coordinates"][0]

        # Obtener las coordenadas mínimas y máximas del rectángulo
        lat_min = min([point[1] for point in coordinates])
        lon_min = min([point[0] for point in coordinates])
        lat_max = max([point[1] for point in coordinates])
        lon_max = max([point[0] for point in coordinates])

        st.sidebar.subheader("Coordenadas seleccionadas:")
        st.sidebar.write(f"**Latitud mínima:** {lat_min:.4f}")
        st.sidebar.write(f"**Longitud mínima:** {lon_min:.4f}")
        st.sidebar.write(f"**Latitud máxima:** {lat_max:.4f}")
        st.sidebar.write(f"**Longitud máxima:** {lon_max:.4f}")

        # Slider para el nivel de zoom
        zoom = st.sidebar.slider("Selecciona el nivel de zoom (más alto = más detalle):", 12, 20, 16)

        # Botón para descargar imágenes
        if st.sidebar.button("Descargar imágenes"):
            if api_key == "YOUR_API_KEY" or not api_key:
                st.sidebar.error("Por favor, ingresa una API Key válida.")
            else:
                status_text = st.sidebar.empty()  # Crear un contenedor vacío para actualizar el texto
                status_text.info("Descargando, por favor espere...")  # Mostrar el mensaje inicial

                # Ejecutar la descarga y actualizar el texto
                descargar_imagenes_en_zona(lat_min, lon_min, lat_max, lon_max, zoom=zoom, output_dir=INPUT_DIR, api_key=api_key)
                
                status_text.success("Descarga completada.")  # Actualizar cuando termine

        # Verificar si hay imágenes disponibles para procesar
        if os.listdir(input_dir):
            if st.sidebar.button("Procesar imágenes"):
                status_text = st.sidebar.empty()  # Crear un contenedor vacío para actualizar el texto
                status_text.info("Procesando imágenes, por favor espere...")  # Mostrar el mensaje inicial

                # Ejecutar el procesamiento y actualizar el texto
                procesar_todas_imagenes(MODEL_SELECTED)

                status_text.success("Procesamiento completado.")  # Actualizar cuando termine
        else:
            st.sidebar.warning("Primero debes descargar las imágenes antes de procesarlas.")
