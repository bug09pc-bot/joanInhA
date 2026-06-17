import streamlit as st
import os
from datetime import datetime
from groq import Groq

st.set_page_config(
    page_title="J.A.R.V.I.S",
    page_icon="🤖",
    layout="centered"
)

st.title("🦾 J.A.R.V.I.S")
st.caption("IA Futurista com Groq")

# Pega a chave direto do Secret do Streamlit
groq_key = os.getenv("GROQ_API_KEY")   # ou st.secrets["GROQ_API_KEY"]

if not groq_key:
    st.error("Chave do Groq não configurada. Vá em Manage app → Secrets e adicione a GROQ_API_KEY")
    st.stop()
