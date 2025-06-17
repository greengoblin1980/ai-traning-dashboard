import streamlit as st
from binance.client import Client
import toml

# Carica le API dal file secrets.toml
secrets = toml.load("secrets.toml")
api_key = secrets["api_key"]
api_secret = secrets["api_secret"]

# Collega alla Binance Testnet
client = Client(api_key, api_secret, testnet=True)

# Funzione per ottenere il saldo USDT
def get_usdt_balance():
    account_info = client.get_account()
    balances = account_info['balances']
    for b in balances:
        if b['asset'] == 'USDT':
            return float(b['free'])
    return 0.0

# Dashboard Streamlit
st.set_page_config(page_title="AI Trading Dashboard", layout="wide")
st.title("🤖 AI Trading Dashboard – Binance Testnet")

usdt = get_usdt_balance()
st.metric("💰 USDT Testnet Balance", f"{usdt:.2f}")

st.write("🚀 Pronto per collegare la logica AI e iniziare il trading automatico!")
