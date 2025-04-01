"""Flask server for emotion detection API.

Exposes endpoints for:
- Emotion analysis (/emotionDetector)
- Main application interface (/)
"""

from flask import Flask, request, jsonify, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/emotionDetector')
def emotion_analyzer():
    """Analyze emotion in input text.

    Returns:
        JSON: {
            "status": int,
            "message": str,
            "scores": dict,
            "dominant_emotion": str
        }

    Example:
        >>> response = emotion_analyzer()
        >>> response.status_code
        200
    """
    text = request.args.get('text', '').strip()

    if not text:
        return jsonify({
            "status": 400,
            "message": "Invalid text! Please try again.",
            "scores": {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None
            },
            "dominant_emotion": None
        }), 400

    result = emotion_detector(text)

    if not result['dominant_emotion']:
        return jsonify({
            "status": 400,
            "message": "Invalid text! Please try again.",
            "scores": result,
            "dominant_emotion": None
        }), 400

    return jsonify({
        "status": 200,
        "message": format_response(result),
        "scores": result,
        "dominant_emotion": result['dominant_emotion']
    })

def format_response(result):
    """Format emotion analysis results into readable string.
    
    Args:
        result (dict): Emotion scores and dominant emotion
        
    Returns:
        str: Formatted analysis string
    """
    return (f"For the given statement, the system response is: "
            f"anger: {result['anger']}, "
            f"disgust: {result['disgust']}, "
            f"fear: {result['fear']}, "
            f"joy: {result['joy']}, "
            f"sadness: {result['sadness']}. "
            f"The dominant emotion is {result['dominant_emotion']}.")

@app.route('/')
def home():
    """Render main application interface.
    
    Returns:
        HTML: Rendered template
    """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
