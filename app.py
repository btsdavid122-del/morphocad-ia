import os
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS

# =========================================
# MORPHO-AI - Servidor en la nube
# =========================================

app = Flask(__name__)
CORS(app)  # permite conexiones desde ESP32 o web

# Leer la API Key desde variable de entorno (NO ponerla en el código)
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Ruta principal para recibir preguntas
@app.route("/morpho", methods=["POST"])
def morpho():
    data = request.get_json()
    pregunta = data.get("texto", "")

    try:
        # Llamada a la IA de OpenAI
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": pregunta}]
        )
        texto_respuesta = respuesta['choices'][0]['message']['content']
        return jsonify(texto_respuesta)
    except Exception as e:
        # En caso de error, devuelve mensaje de error
        return jsonify(f"Error: {str(e)}")

# Para iniciar el servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
