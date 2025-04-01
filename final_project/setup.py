"""
Script de configuración para empaquetar la aplicación.

Define metadatos y dependencias necesarias para instalar el paquete.
"""

from setuptools import setup, find_packages

setup(
    # Nombre oficial del paquete (como se instalará)
    name="EmotionDetection",
    
    # Versión actual (debe coincidir con version.py)
    version="1.0.0",
    
    # Encuentra automáticamente todos los paquetes Python
    packages=find_packages(),
    
    # Dependencias requeridas (se instalarán automáticamente)
    install_requires=[
        'requests>=2.25.1',  # Mínima versión estable probada
    ],
    
    # Metadatos opcionales
    author="Bastian Araya",
    description="Paquete para detección de emociones usando Watson NLP",
    
    # Clasificadores estándar (opcional)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)