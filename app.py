from flask import Flask, render_template, request, jsonify
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configurações
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# Histórico de conversa (por sessão)
conversations = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    session_id = data.get('session_id', 'default')

    if not user_message:
        return jsonify({"error": "Mensagem vazia"}), 400

    # Inicializa histórico da sessão
    if session_id not in conversations:
        conversations[session_id] = [
            {"role": "system", "content": "Você é um assistente útil, inteligente e amigável. Responda em português do Brasil de forma clara e natural."}
        ]

    conversations[session_id].append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # Excelente equilíbrio de velocidade e qualidade
            messages=conversations[session_id],
            temperature=0.7,
            max_tokens=1024
        )

        ai_reply = response.choices[0].message.content
        conversations[session_id].append({"role": "assistant", "content": ai_reply})

        return jsonify({"reply": ai_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
