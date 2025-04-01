"""
Módulo principal para detección de emociones usando el servicio Watson NLP.

Contiene la función emotion_detector que analiza texto y devuelve:
- Puntuaciones para 5 emociones básicas
- La emoción dominante detectada
- Manejo robusto de errores para entradas vacías y fallos de API
"""

import requests  # Para hacer peticiones HTTP al servicio
import json      # Para manejar respuestas en formato JSON
from typing import Dict  # Para anotaciones de tipo

def emotion_detector(text_to_analyze: str) -> Dict[str, float]:
    """
    Analiza las emociones en un texto usando el servicio Watson NLP con manejo completo de errores.
    
    Args:
        text_to_analyze (str): Texto a analizar (inglés). Cadenas vacías o solo espacios devuelven None en todos los campos.
        
    Returns:
        dict: Diccionario con:
            - anger (float): Puntuación de enojo (0-1) o None si hay error
            - disgust (float): Puntuación de disgusto (0-1) o None si hay error
            - fear (float): Puntuación de miedo (0-1) o None si hay error
            - joy (float): Puntuación de alegría (0-1) o None si hay error
            - sadness (float): Puntuación de tristeza (0-1) o None si hay error
            - dominant_emotion (str): Nombre de la emoción dominante o None si hay error
            
    Ejemplo de éxito:
        {
            'anger': 0.02,
            'disgust': 0.01,
            'fear': 0.01,
            'joy': 0.95,
            'sadness': 0.01,
            'dominant_emotion': 'joy'
        }
        
    Ejemplo de error:
        error_response()  # Todos los valores None
    """
    # Validación inicial para entrada vacía o solo espacios
    if not text_to_analyze or not text_to_analyze.strip():
        print("Error: Texto de entrada vacío")  # Log para depuración
        return error_response()

    # Configuración del endpoint de Watson NLP
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    
    # Headers requeridos por el servicio
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    
    # Estructura de datos que espera recibir el servicio
    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        # 1. Enviar petición HTTP POST al servicio con timeout de 5 segundos
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        
        # 2. Verificar si la respuesta fue exitosa (código 200)
        if response.status_code == 400:  # Caso especial para entradas inválidas
            print(f"Error 400 del API: {response.text}")  # Log detallado
            return error_response()
        elif response.status_code != 200:  # Cualquier otro código de error
            print(f"Error HTTP {response.status_code}: {response.text}")
            return error_response()
        
        # 3. Convertir la respuesta JSON a un diccionario Python
        response_dict = json.loads(response.text)
        
        # 4. Extracción segura de valores emocionales con manejo de KeyError
        try:
            # La estructura contiene emotionMentions con análisis detallados
            emotion_data = response_dict['emotionPredictions'][0]['emotionMentions'][0]['emotion']
            
            # 5. Crear diccionario con las 5 emociones requeridas
            emotions = {
                'anger': float(emotion_data['anger']),
                'disgust': float(emotion_data['disgust']),
                'fear': float(emotion_data['fear']),
                'joy': float(emotion_data['joy']),
                'sadness': float(emotion_data['sadness'])
            }
            
            # 6. Calcular la emoción dominante (la de mayor puntuación)
            # max() encuentra el par (clave, valor) con el valor más alto
            dominant = max(emotions.items(), key=lambda item: item[1])[0]
            
            # 7. Retornar el formato requerido combinando ambos diccionarios
            return {
                **emotions,  # Desempaqueta todas las emociones
                'dominant_emotion': dominant  # Añade la dominante
            }
            
        except (KeyError, IndexError) as e:
            print(f"Error procesando estructura de respuesta: {str(e)}")
            return error_response()
            
    except requests.exceptions.Timeout:
        print("Error: Tiempo de espera agotado al conectar con el servicio")
        return error_response()
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {str(e)}")
        return error_response()
    except json.JSONDecodeError as e:
        print(f"Error decodificando JSON: {str(e)}")
        return error_response()
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return error_response()

def error_response() -> Dict[str, None]:
    """
    Devuelve una respuesta estandarizada cuando ocurren errores.
    
    Returns:
        dict: Diccionario con todos los valores emocionales como None.
        Ejemplo:
        {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    """
    return {
        'anger': None,
        'disgust': None,
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None
    }