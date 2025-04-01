"""
Módulo inicial del paquete EmotionDetection.

Exporta la función principal emotion_detector para que esté disponible
cuando se importe el paquete directamente.

Ejemplo de uso:
    from EmotionDetection import emotion_detector
    resultado = emotion_detector("texto a analizar")
"""

# Importa la función principal desde el módulo emotion_detection
from .emotion_detection import emotion_detector, error_response

# Define qué elementos se exportan cuando se usa 'from EmotionDetection import *'
__all__ = ['emotion_detector', 'error_response']