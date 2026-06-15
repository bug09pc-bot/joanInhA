from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL", "llama-3.3-70b-versatile")

@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Groq IA</title>
      <script src="https://cdn.tailwindcss.com"></script>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">
    </head>
    <body class="bg-gray-950 text-white min-h-screen">
      <div class="max-w-4xl mx-auto p-6">
        <h1 class="text-4xl font-bold text-center mb-8 flex items-center justify-center gap-3">
          <i class="fas fa-bolt text-yellow-400"></i> Groq IA
        </h1>
        
        <div id="chat" class="h-[70vh] bg-gray-900 rounded-3xl p-6 overflow-y-auto border border-gray-700 mb-6"></div>

        <div class="flex gap-3">
          <input id="userInput" type="text" placeholder="Digite sua mensagem..." 
                 class="flex-1 bg-gray-800 border border-gray-700 rounded-2xl px-6 py-4 focus:outline-none focus:border-yellow-500 text-lg"
                 onkeypress="if(event.key === 'Enter') sendMessage()">
          <button onclick="sendMessage()" 
                  class="bg-yellow-500 hover:bg-yellow-600 text-black px-10 rounded-2xl font-semibold transition">
            Enviar
          </button>
        </div>
      </div>

      <script>
        async function sendMessage() {
          const input = document.getElementById('userInput');
          const message = input.value.trim();
          if (!message) return;

          addMessage(message, true);
          input.value = '';

          const thinking = addMessage("Groq pensando...", false);

          try {
            const res = await fetch('/chat', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({message: message})
            });
            const data = await res.json();
            thinking.remove();
            addMessage(data.response, false);
          } catch (e) {
            thinking.remove();
            addMessage("Erro de conexão.", false);
          }
        }

        function addMessage(text, isUser) {
          const chat = document.getElementById('chat');
          const div = document.createElement('div');
          div.className = `mb-6 ${isUser ? 'text-right' : 'text-left'}`;
          div.innerHTML = `
            <div class="${isUser ? 'bg-blue-600 ml-auto' : 'bg-gray-800'} inline-block max-w-[85%] rounded-2xl px-6 py-4">
              ${text}
            </div>
          `;
          chat.appendChild(div);
          chat.scrollTop = chat.scrollHeight;
          return div;
        }
      </script>
    </body>
    </html>
    """
    return html

@app.route('/chat', methods=['POST'])
def chat():
    if not GROQ_API_KEY:
        return jsonify({"response": "Erro: Coloque sua chave no arquivo .env"}), 500

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
