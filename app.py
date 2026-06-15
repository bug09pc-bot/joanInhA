
from flask import Flask, request, jsonify
import os
from groq import Groq
from dotenv import load_dotenv
import hmac
import hashlib

load_dotenv()

app = Flask(__name__)

# ==================== CONFIGURAÇÕES ====================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")

client = Groq(api_key=GROQ_API_KEY)

def verify_signature(payload: bytes, signature: str) -> bool:
    if not GITHUB_WEBHOOK_SECRET:
        return True
    mac = hmac.new(GITHUB_WEBHOOK_SECRET.encode(), payload, hashlib.sha256)
    expected = "sha256=" + mac.hexdigest()
    return hmac.compare_digest(expected, signature)

@app.route('/webhook', methods=['POST'])
def github_webhook():
    # Verificação de segurança do GitHub
    signature = request.headers.get('X-Hub-Signature-256')
    if not verify_signature(request.get_data(), signature):
        return jsonify({"error": "Invalid signature"}), 403

    event = request.headers.get('X-GitHub-Event')
    data = request.json

    # Responder quando uma nova Issue for aberta
    if event == "issues" and data.get("action") == "opened":
        issue = data["issue"]
        repo = data["repository"]

        prompt = f"""Você é um assistente técnico útil para repositórios GitHub.
Repositório: {repo['full_name']}
Título: {issue['title']}
Descrição: {issue.get('body') or 'Sem descrição fornecida.'}

Responda de forma clara, educada e objetiva. Seja útil e técnico quando necessário."""

        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",   # Rápido e bom
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=700
            )

            ai_reply = completion.choices[0].message.content

            # Postar comentário na Issue
            from github import Github
            g = Github(GITHUB_TOKEN)
            repo_obj = g.get_repo(repo['full_name'])
            issue_obj = repo_obj.get_issue(issue['number'])
            
            issue_obj.create_comment(
                f"🤖 **Groq Assistant** respondeu automaticamente:\n\n{ai_reply}"
            )

            print(f"✅ Respondeu issue #{issue['number']} em {repo['full_name']}")

        except Exception as e:
            print(f"❌ Erro ao processar issue: {e}")

    return jsonify({"status": "success"}), 200


@app.route('/')
def home():
    return "✅ GitHub Groq Bot está rodando!"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
