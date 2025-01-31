import cv2
import csv
import os
from inference_sdk import InferenceHTTPClient, InferenceConfiguration

# Configuración del cliente de inferencia con umbral de confianza
custom_configuration = InferenceConfiguration(confidence_threshold=0.75)


CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="O9O8mwpy2WXTtXuYDXOm"
)

# Directorios de entrada y salida
input_dir = 'imagenes_satelitales_google_maps'
output_dir = 'imagenes_con_circulos'
output_csv = 'detecciones.csv'

# Crear el directorio de salida si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Crear el archivo CSV y escribir el encabezado
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
        "Imagen", "Latitud Mínima", "Longitud Mínima", "Latitud Máxima", "Longitud Máxima", 
        "x", "y", "Ancho", "Alto", "Confianza", "Clase"
    ])

# Función para dibujar los cuadros delimitadores y guardar la información
def procesar_imagen(nombre_imagen, modelo_id="710robotrain/3"):
    try:
        # Cargar la imagen
        image_path = os.path.join(input_dir, nombre_imagen)
        image = cv2.imread(image_path)
        if image is None:
            print(f"No se pudo cargar la imagen: {nombre_imagen}")
            return

        # Realizar la inferencia en la imagen
        CLIENT.configure(custom_configuration)
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
        print(f"Imagen procesada y guardada en: {output_path}")

    except Exception as e:
        print(f"Error procesando la imagen {nombre_imagen}: {str(e)}")

# Procesar todas las imágenes en el directorio de entrada
for imagen in os.listdir(input_dir):
    if imagen.endswith(".png"):
        procesar_imagen(imagen)
