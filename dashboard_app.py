import streamlit as st
from trading_bot import run_bot

st.set_page_config(page_title="AI Trading Dashboard", layout="wide")

st.title("📈 AI Trading Dashboard")
st.markdown("Benvenuto nel tuo bot di trading AI automatizzato con notifiche WhatsApp!")

if st.button("▶️ Avvia il bot di trading AI"):
    st.success("Bot avviato! Controlla le notifiche WhatsApp.")
    run_bot()
