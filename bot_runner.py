import os
import time
from binance.client import Client
import pandas as pd
import ta
from twilio.rest import Client as TwilioClient

# =======================
# CONFIGURAZIONE API DA VARIABILI D’AMBIENTE (tranne numero WhatsApp)
# =======================
API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_SECRET_KEY')
binance_client = Client(API_KEY, API_SECRET, testnet=True)

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_FROM = os.getenv('TWILIO_WHATSAPP_FROM')

# Numero WhatsApp di destinazione hardcoded (tuo numero)
TWILIO_WHATSAPP_TO = 'whatsapp:+393474595534'

twilio_client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]

def send_whatsapp_message(msg):
    message = twilio_client.messages.create(
        body=msg,
        from_=TWILIO_WHATSAPP_FROM,
        to=TWILIO_WHATSAPP_TO
    )
    print(f"WhatsApp message sent: {msg}")

def get_klines(symbol, interval='1m', lookback=100):
    klines = binance_client.get_klines(symbol=symbol, interval=interval, limit=lookback)
    df = pd.DataFrame(klines, columns=[
        'open_time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['close'] = df['close'].astype(float)
    return df

def analyze_symbol(symbol):
    df = get_klines(symbol)
    df['ema10'] = ta.trend.EMAIndicator(df['close'], window=10).ema_indicator()
    df['ema50'] = ta.trend.EMAIndicator(df['close'], window=50).ema_indicator()
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    df['macd'] = ta.trend.MACD(df['close']).macd_diff()

    score = 0
    if df['ema10'].iloc[-1] > df['ema50'].iloc[-1]:
        score += 1
    if df['rsi'].iloc[-1] < 30:
        score += 1
    if df['macd'].iloc[-1] > 0:
        score += 1
    return score

def choose_best_symbol(symbols):
    best_score = -1
    best_symbol = None
    for s in symbols:
        try:
            score = analyze_symbol(s)
            print(f"Symbol: {s} Score: {score}")
            if score > best_score:
                best_score = score
                best_symbol = s
        except Exception as e:
            print(f"Errore analisi {s}: {e}")
    return best_symbol, best_score

def place_order(symbol, usdt_amount):
    try:
        price = float(binance_client.get_symbol_ticker(symbol=symbol)['price'])
        qty = round(usdt_amount / price, 5)
        order = binance_client.create_order(
            symbol=symbol,
            side='BUY',
            type='MARKET',
            quantity=qty
        )
        return order
    except Exception as e:
        print(f"Errore ordine: {e}")
        return None

def trading_bot():
    usdt_balance = float([b['free'] for b in binance_client.get_account()['balances'] if b['asset'] == 'USDT'][0])
    print(f"USDT Balance: {usdt_balance:.2f}")

    best_symbol, best_score = choose_best_symbol(symbols)
    if best_symbol is None:
        print("Nessun simbolo valido trovato.")
        return

    invest_amount = min(usdt_balance, 10 * best_score)
    if invest_amount < 5:
        print("Saldo troppo basso o punteggio basso per investire.")
        return

    print(f"Best symbol: {best_symbol} con punteggio {best_score}, investo {invest_amount:.2f} USDT")
    order = place_order(best_symbol, invest_amount)

    if order:
        msg = f"🚀 Ordine eseguito: {best_symbol} - Quantità: {order['executedQty']} - Prezzo: {order['fills'][0]['price']}"
        send_whatsapp_message(msg)
    else:
        send_whatsapp_message(f"⚠️ Errore durante l'ordine su {best_symbol}")

if __name__ == "__main__":
    send_whatsapp_message("🤖 Bot trading AI avviato e operativo!")
    while True:
        try:
            trading_bot()
        except Exception as e:
            print(f"Errore nel bot: {e}")
            send_whatsapp_message(f"⚠️ Errore nel bot: {e}")
        time.sleep(60)
