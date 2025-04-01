"""
Módulo principal para detección de emociones usando el servicio Watson NLP.

Contiene la función emotion_detector que analiza texto y devuelve:
- Puntuaciones para 5 emociones básicas
- La emoción dominante detectada
"""

import requests  # Para hacer peticiones HTTP al servicio
import json      # Para manejar respuestas en formato JSON

def emotion_detector(text_to_analyze):
    """
    Analiza las emociones en un texto usando el servicio Watson NLP.
    
    Args:
        text_to_analyze (str): Texto a analizar, preferiblemente en inglés.
        
    Returns:
        dict: Diccionario con:
            - anger: Puntuación de enojo (0-1)
            - disgust: Puntuación de disgusto (0-1)
            - fear: Puntuación de miedo (0-1)
            - joy: Puntuación de alegría (0-1)
            - sadness: Puntuación de tristeza (0-1)
            - dominant_emotion: Nombre de la emoción con mayor puntuación
            
        Si hay errores, todos los valores serán None.
    """
    # Configuración del endpoint de Watson NLP
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    
    # Headers requeridos por el servicio
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    
    # Estructura de datos que espera recibir el servicio
    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        # 1. Enviar petición HTTP POST al servicio
        response = requests.post(url, json=payload, headers=headers)
        
        # 2. Verificar si la respuesta fue exitosa (código 200)
        if response.status_code != 200:
            return error_response()  # Retorna valores None si falla
        
        # 3. Convertir la respuesta JSON a un diccionario Python
        response_dict = json.loads(response.text)
        
        # 4. Extraer los valores emocionales específicos
        # La estructura contiene emotionMentions con análisis detallados
        emotion_data = response_dict['emotionPredictions'][0]['emotionMentions'][0]['emotion']
        
        # 5. Crear diccionario con las 5 emociones requeridas
        emotions = {
            'anger': emotion_data['anger'],
            'disgust': emotion_data['disgust'],
            'fear': emotion_data['fear'],
            'joy': emotion_data['joy'],
            'sadness': emotion_data['sadness']
        }
        
        # 6. Calcular la emoción dominante (la de mayor puntuación)
        # max() encuentra el par (clave, valor) con el valor más alto
        dominant = max(emotions.items(), key=lambda item: item[1])[0]
        
        # 7. Retornar el formato requerido combinando ambos diccionarios
        return {
            **emotions,  # Desempaqueta todas las emociones
            'dominant_emotion': dominant  # Añade la dominante
        }
        
    except Exception as e:
        # Manejo de cualquier error inesperado
        print(f"Error procesando respuesta: {e}")
        return error_response()

def error_response():
    """
    Devuelve una respuesta estandarizada cuando ocurren errores.
    
    Returns:
        dict: Diccionario con todos los valores emocionales como None
    """
    return {
        'anger': None,
        'disgust': None,
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None
    }