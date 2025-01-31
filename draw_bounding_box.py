import cv2
import csv
import os
from inference_sdk import InferenceHTTPClient, InferenceConfiguration
from config import MODEL_ID

# Configuración inicial del cliente de inferencia
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="O9O8mwpy2WXTtXuYDXOm"
)
CLIENT.configure(InferenceConfiguration(confidence_threshold=0.75))

# Directorios de entrada y salida
input_dir = 'imagenes_satelitales_google_maps'
output_dir = 'imagenes_con_circulos'
output_csv = 'detecciones.csv'

# Crear el directorio de salida si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Función para procesar una imagen y guardar resultados
def procesar_imagen(image_path, modelo_id):
    try:
        nombre_imagen = os.path.basename(image_path)
        # Cargar la imagen
        image = cv2.imread(image_path)
        if image is None:
            return f"No se pudo cargar la imagen: {nombre_imagen}"

        # Realizar la inferencia
        result = CLIENT.infer(image_path, model_id=modelo_id)

        # Extraer las coordenadas del nombre de la imagen
        coordenadas = nombre_imagen.replace(".png", "").replace("imagen_", "").split("_")
        lat_min, lon_min, lat_max, lon_max = map(float, coordenadas)

        # Dibujar cada predicción en la imagen
        for prediccion in result['predictions']:
            confianza = prediccion['confidence']
            if confianza >= 0.75:  # Confirmar el umbral de confianza
                x = int(prediccion['x'])
                y = int(prediccion['y'])
                ancho = int(prediccion['width'])
                alto = int(prediccion['height'])
                clase = prediccion['class']

                # Calcular la esquina superior izquierda del cuadro delimitador
                esquina_sup_izq = (x - ancho // 2, y - alto // 2)
                esquina_inf_der = (x + ancho // 2, y + alto // 2)

                # Dibujar el cuadro delimitador y añadir texto
                cv2.rectangle(image, esquina_sup_izq, esquina_inf_der, (0, 255, 0), 2)
                texto = f"{clase} ({confianza:.2f})"
                cv2.putText(image, texto, (esquina_sup_izq[0], esquina_sup_izq[1] - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                # Guardar la información en el archivo CSV
                with open(output_csv, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        nombre_imagen, lat_min, lon_min, lat_max, lon_max, x, y, ancho, alto, confianza, clase
                    ])

        # Guardar la imagen con los cuadros delimitadores
        output_path = os.path.join(output_dir, nombre_imagen)
        cv2.imwrite(output_path, image)
        return f"Imagen procesada y guardada en: {output_path}"

    except Exception as e:
        return f"Error procesando la imagen {image_path}: {str(e)}"

# Función para procesar todas las imágenes en el directorio de entrada
def procesar_todas_imagenes(input_dir, modelo_id):
    # Crear el csv aqui
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Imagen", "Latitud Mínima", "Longitud Mínima", "Latitud Máxima", "Longitud Máxima",
            "x", "y", "Ancho", "Alto", "Confianza", "Clase"
        ])
    mensajes = []
    for imagen in os.listdir(input_dir):
        if imagen.endswith(".png"):
            image_path = os.path.join(input_dir, imagen)
            mensaje = procesar_imagen(image_path, modelo_id)
            mensajes.append(mensaje)
    return mensajes
