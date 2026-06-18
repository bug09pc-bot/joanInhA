import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# ==================== CONFIGURAÇÃO ====================
st.set_page_config(
    page_title="Groq IA - Chat Rápido",
    page_icon="🤖",
    layout="centered"
)

# Inicializa cliente Groq
if "groq_client" not in st.session_state:
    st.session_state.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Sou uma IA super rápida feita com Groq. Como posso te ajudar hoje? 🚀"}
    ]

# ==================== INTERFACE ====================
st.title("🤖 Groq IA Online")
st.caption("Llama 3.3 70B - Extremamente rápida")

# Exibe histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada
if prompt := st.chat_input("Digite sua mensagem..."):
    # Adiciona mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera resposta da IA
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = st.session_state.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    temperature=0.7,
                    max_tokens=1024,
                    stream=False
                )
                ai_response = response.choices[0].message.content
                st.markdown(ai_response)
                
                # Salva no histórico
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                st.error(f"Erro: {str(e)}")

# Sidebar com informações
with st.sidebar:
    st.header("⚙️ Configurações")
    model = st.selectbox(
        "Modelo",
        ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it"],
        index=0
    )
    st.divider()
    st.info("🔥 Usando Groq LPU — Uma das IAs mais rápidas do mundo!")
    if st.button("Limpar conversa"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Conversa limpa! Como posso ajudar agora?"}
        ]
        st.rerun()
