from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL", "llama-3.3-70b-versatile")

if not GROQ_API_KEY:
    print("⚠️ AVISO: GROQ_API_KEY não encontrada no .env")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not GROQ_API_KEY:
        return jsonify({"response": "Erro: Chave da API Groq não configurada."}), 500

    user_message = request.json.get('message')

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": user_message}],
                "temperature": 0.7,
                "max_tokens": 4096
            }
        )

        data = response.json()
        reply = data['choices'][0]['message']['content']
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"response": f"Erro: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
