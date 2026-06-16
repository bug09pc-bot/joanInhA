import streamlit as st
from dotenv import load_dotenv
import os
import requests

load_dotenv()

# Configuração Grok (xAI)
GROK_API_KEY = os.getenv("GROK_API_KEY")

# Modelo fixo (você pode mudar aqui se quiser)
MODEL = "grok-4.3"   # ou grok-3, grok-beta, etc

if not GROK_API_KEY:
    st.error("❌ Coloque sua GROK_API_KEY no arquivo .env")
    st.stop()

# Configuração da página
st.set_page_config(page_title="Grok IA", page_icon="🧠", layout="centered")
st.title("🧠 Grok IA Online")
st.caption("Usando API oficial do Grok (xAI)")

# Histórico da conversa
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Digite sua mensagem..."):
    # Mostra mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta do Grok
    with st.chat_message("assistant"):
        with st.spinner("Grok pensando..."):
            try:
                response = requests.post(
                    "https://api.x.ai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {GROK_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": MODEL,
                        "messages": [{"role": m["role"], "content": m["content"]} 
                                    for m in st.session_state.messages],
                        "temperature": 0.7,
                        "max_tokens": 4096
                    },
                    timeout=60
                )
                
                response.raise_for_status()
                data = response.json()
                resposta = data['choices'][0]['message']['content']
                
                st.markdown(resposta)
                
                # Salva no histórico
                st.session_state.messages.append({"role": "assistant", "content": resposta})
                
            except Exception as e:
                st.error(f"Erro ao conectar com Grok: {str(e)}")

# Botão para limpar conversa
if st.button("🗑️ Limpar Conversa"):
    st.session_state.messages = []
    st.rerun()
