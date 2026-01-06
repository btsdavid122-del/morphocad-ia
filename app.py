from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "Morpho AI está online 🤖"

@app.route("/morpho", methods=["POST"])
def morpho():
    texto = request.json.get("texto", "")

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres Morpho, un asistente virtual doméstico"},
            {"role": "user", "content": texto}
        ]
    )

    accion = "ninguna"
    t = texto.lower()
    if "apaga la luz" in t:
        accion = "apagar_luz"
    if "enciende la luz" in t:
        accion = "encender_luz"
    if "reproduce" in t:
        accion = "reproducir_musica"

    return jsonify({
        "respuesta": completion.choices[0].message.content,
        "accion": accion
    })

app.run(host="0.0.0.0", port=10000)
