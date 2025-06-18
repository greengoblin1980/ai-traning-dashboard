import os
import time
import requests
from binance.client import Client

# Funzione per inviare notifiche Telegram
def send_telegram_message(message):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except Exception as e:
        print("Errore invio messaggio Telegram:", e)

# Setup client Binance Testnet
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_SECRET_KEY")
client = Client(api_key, api_secret)
client.API_URL = 'https://testnet.binance.vision/api'

# Logica semplice di esempio (sostituibile con una AI vera)
def run_bot():
    try:
        tickers = client.get_ticker_price()
        symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
        opportunities = []

        for symbol in symbols:
            price = float(next(t['price'] for t in tickers if t['symbol'] == symbol))
            if price > 100:  # Simulazione: condizione fittizia
                opportunities.append((symbol, price))

        if opportunities:
            best = max(opportunities, key=lambda x: x[1])
            message = f"💹 Migliore opportunità: {best[0]} a {best[1]}"
            send_telegram_message(message)
        else:
            send_telegram_message("⚠️ Nessuna opportunità rilevata.")
    except Exception as e:
        send_telegram_message(f"❌ Errore nel bot: {e}")
