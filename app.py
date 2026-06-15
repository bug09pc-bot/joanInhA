import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

# Configuração da Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL", "llama-3.3-70b-versatile")

if not GROQ_API_KEY:
    st.error("❌ Coloque sua GROQ_API_KEY no arquivo .env")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# Configuração da página
st.set_page_config(page_title="Groq IA", page_icon="🚀", layout="centered")
st.title("🚀 Groq IA Online")
st.caption("Respostas rápidas com Groq")

# Inicializar histórico
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de input
if prompt := st.chat_input("Digite sua mensagem..."):
    # Adiciona mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta da IA
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": m["role"], "content": m["content"]} 
                             for m in st.session_state.messages],
                    temperature=0.7,
                    max_tokens=4000
                )
                resposta = response.choices[0].message.content
                st.markdown(resposta)
                
                # Salva no histórico
                st.session_state.messages.append({"role": "assistant", "content": resposta})
                
            except Exception as e:
                st.error(f"Erro: {str(e)}")

# Botão para limpar conversa
if st.button("Limpar Conversa"):
    st.session_state.messages = []
    st.rerun()
