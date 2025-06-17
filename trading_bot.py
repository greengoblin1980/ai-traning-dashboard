import ccxt
import pandas as pd
import numpy as np
from twilio.rest import Client

# 🔒 Twilio credentials (usa variabili d’ambiente in produzione!)
TWILIO_ACCOUNT_SID = "INSERISCI_TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "INSERISCI_TWILIO_AUTH_TOKEN"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"
TARGET_WHATSAPP_NUMBER = "whatsapp:+39XXXXXXXXXX"

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_whatsapp_message(message):
    client.messages.create(
        body=message,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=TARGET_WHATSAPP_NUMBER
    )

def run_bot():
    binance = ccxt.binance()
    symbols = ["BTC/USDT", "ETH/USDT", "BNB/USDT"]

    best_symbol = None
    best_score = -np.inf

    for symbol in symbols:
        try:
            ohlcv = binance.fetch_ohlcv(symbol, timeframe='1m', limit=20)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

            df['sma'] = df['close'].rolling(window=5).mean()
            score = df['close'].iloc[-1] - df['sma'].iloc[-1]

            if score > best_score:
                best_score = score
                best_symbol = symbol
        except Exception as e:
            print(f"Errore con {symbol}: {e}")

    if best_symbol:
        message = f"✅ Il bot suggerisce di operare su: {best_symbol}"
        print(message)
        send_whatsapp_message(message)
    else:
        send_whatsapp_message("⚠️ Nessuna opportunità rilevata.")
