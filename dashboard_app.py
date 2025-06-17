import streamlit as st
from binance.client import Client
import toml
import trading_bot  # Import del tuo bot AI

# Configurazione pagina
st.set_page_config(page_title="AI Trading Dashboard", layout="wide")
st.title("🤖 AI Trading Dashboard – Binance Testnet")

# Saldo reale USDT
secrets = toml.load("secrets.toml")
api_key = secrets["api_key"]
api_secret = secrets["api_secret"]
client = Client(api_key, api_secret, testnet=True)

def get_usdt_balance():
    balances = client.get_account()["balances"]
    for b in balances:
        if b["asset"] == "USDT":
            return float(b["free"])
    return 0.0

usdt = get_usdt_balance()
st.metric("💰 USDT Testnet Balance", f"{usdt:.2f}")

st.markdown("---")
st.header("📊 Trading Bot Controls")

# Bottone per eseguire il bot AI avanzato
if st.button("▶️ Run AI Trading Bot"):
    trading_bot.trading_bot()

st.markdown("---")
st.caption("Powered by greengoblin1980 • Binance Testnet • v2.0")
