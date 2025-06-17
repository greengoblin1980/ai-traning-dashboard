import streamlit as st

st.set_page_config(page_title="AI Trading Dashboard", layout="wide")

st.title("📈 AI Trading Dashboard")
st.markdown("Benvenuto! Questa è una dashboard connessa al tuo bot AI su Binance Testnet.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Saldo attuale")
    st.metric(label="USDT", value="10,000")

with col2:
    st.subheader("Posizione attuale")
    st.write("🟢 LONG su BTC/USDT")

st.divider()

st.subheader("Grafico (placeholder)")
st.line_chart([10000, 10010, 10025, 10000, 9950, 10020])

st.divider()

st.subheader("Controlli Bot")

if st.button("▶️ Avvia Bot"):
    st.success("Bot avviato")

if st.button("⏹️ Ferma Bot"):
    st.warning("Bot fermato")

st.divider()
st.caption("Powered by reengoblin1980 • Binance Testnet • v1.0")
