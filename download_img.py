import requests
import time
import math

from config import KEY, INPUT_DIR

# Configuración inicial
API_KEY = KEY
output_dir = INPUT_DIR

# Función para calcular el área cubierta por una imagen en km, basado en el nivel de zoom
def calcular_paso_adecuado(zoom, tamaño_imagen_pixeles, latitud_centro):
    # Conversión del área cubierta por la imagen a kilómetros
    escala = (156543.03 * math.cos(math.radians(latitud_centro))) / (2 ** zoom)
    area_km = (escala * tamaño_imagen_pixeles) / 1000  # Convertimos a km
    return area_km

# Función para descargar imágenes satelitales
def descargar_imagen_satelital(lat_min, lon_min, lat_max, lon_max, centro_lat, centro_lon, zoom=16, size="640x640"):
    url = f"https://maps.googleapis.com/maps/api/staticmap?center={centro_lat},{centro_lon}&zoom={zoom}&size={size}&maptype=satellite&key={API_KEY}"
    try:
        response = requests.get(url)

        if response.status_code == 200:
            # Nombrar la imagen usando las coordenadas del cuadro delimitador
            filename = f"{output_dir}/imagen_{lat_min}_{lon_min}_{lat_max}_{lon_max}.png"
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"Imagen guardada: {filename}")
        else:
            print(f"Error {response.status_code} para ({centro_lat}, {centro_lon}): {response.text}")

    except Exception as e:
        print(f"Error descargando la imagen ({centro_lat}, {centro_lon}): {str(e)}")

# Función principal para calcular la cuadrícula y descargar las imágenes sin superposición
def descargar_imagenes_en_zona(lat_min, lon_min, lat_max, lon_max, zoom=16, tamaño_imagen_pixeles=640):
    # Calcular el paso en km basado en el nivel de zoom y el tamaño de la imagen
    paso_km = calcular_paso_adecuado(zoom, tamaño_imagen_pixeles, (lat_min + lat_max) / 2)

    # Convertir el paso de kilómetros a grados
    paso_lat, paso_lon = km_a_grados(paso_km, (lat_min + lat_max) / 2)

    # Calcular el número de pasos necesarios en cada dirección
    num_pasos_lat = int((lat_max - lat_min) / paso_lat) + 1
    num_pasos_lon = int((lon_max - lon_min) / paso_lon) + 1

    print(f"Calculando {num_pasos_lat} pasos en latitud y {num_pasos_lon} en longitud. Paso aproximado: {paso_km:.2f} km")

    # Recorrer la cuadrícula y descargar las imágenes
    for i in range(num_pasos_lat):
        for j in range(num_pasos_lon):
            # Coordenadas del cuadro delimitador de la imagen
            cuadro_lat_min = lat_min + (i * paso_lat)
            cuadro_lon_min = lon_min + (j * paso_lon)
            cuadro_lat_max = cuadro_lat_min + paso_lat
            cuadro_lon_max = cuadro_lon_min + paso_lon

            # Coordenadas del centro de la imagen
            centro_lat = (cuadro_lat_min + cuadro_lat_max) / 2
            centro_lon = (cuadro_lon_min + cuadro_lon_max) / 2

            print(f"Descargando imagen para: ({centro_lat}, {centro_lon}) con cuadro delimitador: ({cuadro_lat_min}, {cuadro_lon_min}, {cuadro_lat_max}, {cuadro_lon_max})")

            # Descargar la imagen satelital
            descargar_imagen_satelital(cuadro_lat_min, cuadro_lon_min, cuadro_lat_max, cuadro_lon_max, centro_lat, centro_lon, zoom)

            # Pausa para evitar exceder el límite de solicitudes por segundo
            time.sleep(1)

# Función para convertir kilómetros a grados (aproximación)
def km_a_grados(km, latitud):
    grados_lat = km / 111  # 1° de latitud = ~111 km
    grados_lon = km / (111 * abs(math.cos(math.radians(latitud)))) 
    return grados_lat, grados_lon

# Ejecutar la descarga
#descargar_imagenes_en_zona(LAT_MIN, LON_MIN, LAT_MAX, LON_MAX, zoom=16, tamaño_imagen_pixeles=640)
