from inference_sdk import InferenceHTTPClient, InferenceConfiguration

# Configuración del cliente de inferencia
API_URL = "https://detect.roboflow.com"
API_KEY = "O9O8mwpy2WXTtXuYDXOm"
CONFIDENCE_THRESHOLD = 0.65

# Inicialización del cliente de inferencia
CLIENT = InferenceHTTPClient(api_url=API_URL, api_key=API_KEY)
CLIENT.configure(InferenceConfiguration(confidence_threshold=CONFIDENCE_THRESHOLD))
