import streamlit as st
import os
from groq import Groq

st.set_page_config(
    page_title="J.A.R.V.I.S",
    page_icon="🤖",
    layout="centered"
)

st.title("🦾 J.A.R.V.I.S")
st.caption("IA Futurista com Groq")

# Pega a chave do Secret do Streamlit
groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    st.error("🔑 Chave do Groq não encontrada!")
    st.info("Vá em 'Gerenciar aplicativo' → Secrets e adicione GROQ_API_KEY")
    st.stop()

if "historico" not in st.session_state:
    st.session_state.historico = []

for msg in st.session_state.historico:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Digite sua mensagem..."):
    st.session_state.historico.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("J.A.R.V.I.S pensando..."):
            try:
                client = Groq(api_key=groq_key)
                
                messages = [
                    {"role": "system", "content": "Você é J.A.R.V.I.S, uma IA futurista, sarcástica, leal e extremamente útil. Responda sempre em português do Brasil de forma natural e divertida."}
                ] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.historico]

                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=800
                )
                
                resposta = response.choices[0].message.content
                st.markdown(resposta)
                
            except Exception as e:
                st.error("Limite temporário atingido. Aguarde 20 segundos e tente novamente.")
                resposta = "Estou com um pouco de carga agora... Tenta de novo em alguns segundos!"

    st.session_state.historico.append({"role": "assistant", "content": resposta})
