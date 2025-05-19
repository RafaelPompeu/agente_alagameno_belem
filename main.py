import os
import openai
import google.generativeai as palm
from google.generativeai import GenerativeModel

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

# Carrega a chave da API do ambiente e define para uso global
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key não fornecida! Defina a variável de ambiente GOOGLE_API_KEY.")

os.environ["GOOGLE_API_KEY"] = api_key  # Garante que estará disponível para outros módulos

model = GenerativeModel(model_name="gemini-2.0-flash", api_key=api_key)

@app.route('/api/generate', methods=['POST'])
def generate_text():
    data = request.get_json()
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        generated_text = response.choices[0].text.strip()
        return jsonify({'generated_text': generated_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)