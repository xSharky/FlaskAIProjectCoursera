/**
 * Función principal para analizar emociones
 * - Maneja el envío de texto al servidor
 * - Procesa la respuesta
 * - Actualiza la interfaz de usuario
 */
function analizarEmocion() {
    // 1. Obtener elementos del DOM
    const inputTexto = document.getElementById('textToAnalyze');
    const resultadoDiv = document.getElementById('result');
    const botonAnalizar = document.querySelector('button');
    
    // 2. Validar entrada vacía
    if (!inputTexto.value.trim()) {
        resultadoDiv.innerHTML = '<p class="error">Error: Ingrese texto para analizar</p>';
        return;
    }
    
    // 3. Deshabilitar botón durante la solicitud
    botonAnalizar.disabled = true;
    resultadoDiv.innerHTML = '<p class="loading">Analizando...</p>';
    
    // 4. Realizar petición al servidor
    fetch(`/emotionDetector?text=${encodeURIComponent(inputTexto.value)}`)
        .then(response => {
            // 5. Manejar errores HTTP
            if (!response.ok) {
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            // 6. Procesar respuesta exitosa
            if (data.status === 400) {
                // Mostrar errores del servidor
                resultadoDiv.innerHTML = `<p class="error">${data.message}</p>`;
            } else {
                // Mostrar resultados formateados
                resultadoDiv.innerHTML = `
                    <div class="result-container">
                        <p>${data.message}</p>
                        <div class="scores">
                            <div class="emotion-bar" style="width: ${data.scores.anger * 100}%">Ira</div>
                            <div class="emotion-bar" style="width: ${data.scores.disgust * 100}%">Disgusto</div>
                            <div class="emotion-bar" style="width: ${data.scores.fear * 100}%">Miedo</div>
                            <div class="emotion-bar" style="width: ${data.scores.joy * 100}%">Alegría</div>
                            <div class="emotion-bar" style="width: ${data.scores.sadness * 100}%">Tristeza</div>
                        </div>
                        <p class="dominant">Emoción dominante: <strong>${data.dominant_emotion}</strong></p>
                    </div>
                `;
            }
        })
        .catch(error => {
            // 7. Manejar errores de red/JS
            console.error('Error en fetch:', error);
            resultadoDiv.innerHTML = `<p class="error">Error de conexión: ${error.message}</p>`;
        })
        .finally(() => {
            // 8. Rehabilitar botón
            botonAnalizar.disabled = false;
        });
}

/**
 * Manejador de eventos para el botón
 */
document.querySelector('button').addEventListener('click', analizarEmocion);

/**
 * Manejador para la tecla Enter
 */
document.getElementById('textToAnalyze').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        analizarEmocion();
    }
});