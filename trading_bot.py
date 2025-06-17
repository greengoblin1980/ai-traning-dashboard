import time
import pandas as pd
import numpy as np
from binance.client import Client
from binance.enums import *
import ta
import streamlit as st
import toml

# Carica API
secrets = toml.load("secrets.toml")
api_key = secrets["api_key"]
api_secret = secrets["api_secret"]

client = Client(api_key, api_secret, testnet=True)

SYMBOL = "BTCUSDT"
INTERVAL = Client.KLINE_INTERVAL_1MINUTE
LOOKBACK = "500 minutes ago UTC"

# Funzione per scaricare dati storici
def get_historical_klines(symbol, interval, lookback):
    klines = client.get_historical_klines(symbol, interval, lookback)
    df = pd.DataFrame(klines, columns=[
        "open_time", "open", "high", "low", "close", "volume", "close_time",
        "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume",
        "taker_buy_quote_asset_volume", "ignore"])
    df["close"] = df["close"].astype(float)
    df["open_time"] = pd.to_datetime(df["open_time"], unit='ms')
    return df

# Calcolo indicatori tecnici
def add_indicators(df):
    df["EMA20"] = ta.trend.ema_indicator(df["close"], window=20)
    df["RSI"] = ta.momentum.rsi(df["close"], window=14)
    macd = ta.trend.MACD(df["close"])
    df["MACD"] = macd.macd()
    df["MACD_signal"] = macd.macd_signal()
    return df

# Calcolo confidenza trade basata su indicatori
def compute_confidence(row):
    score = 0
    if row["RSI"] < 30:
        score += 40
    if row["close"] > row["EMA20"]:
        score += 30
    if row["MACD"] > row["MACD_signal"]:
        score += 30
    return score

# Ottieni saldo USDT disponibile
def get_usdt_balance():
    balances = client.get_account()["balances"]
    for b in balances:
        if b["asset"] == "USDT":
            return float(b["free"])
    return 0.0

# Funzione per eseguire ordine di mercato
def place_order(symbol, side, quantity):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=ORDER_TYPE_MARKET,
            quantity=quantity)
        st.success(f"Order executed: {side} {quantity} {symbol}")
        return order
    except Exception as e:
        st.error(f"Order failed: {e}")
        return None

# Funzione principale del bot
def trading_bot():
    st.info("Starting trading bot...")

    df = get_historical_klines(SYMBOL, INTERVAL, LOOKBACK)
    df = add_indicators(df)
    latest = df.iloc[-1]
    confidence = compute_confidence(latest)

    st.write(f"Latest price: {latest['close']:.2f} USD")
    st.write(f"RSI: {latest['RSI']:.2f}")
    st.write(f"EMA20: {latest['EMA20']:.2f}")
    st.write(f"MACD: {latest['MACD']:.4f}")
    st.write(f"MACD Signal: {latest['MACD_signal']:.4f}")
    st.write(f"Confidence score: {confidence}")

    usdt_balance = get_usdt_balance()
    st.write(f"USDT balance: {usdt_balance:.2f}")

    # Definizione della quantità in base alla confidenza
    if confidence >= 80:
        invest_amount = min(70, usdt_balance)
    elif confidence >= 60:
        invest_amount = min(30, usdt_balance)
    else:
        invest_amount = 0

    if invest_amount == 0:
        st.warning("Confidence too low, no trade executed.")
        return

    # Calcolo quantità BTC da comprare
    quantity = invest_amount / latest["close"]
    # Binance richiede quantità con precisione, arrotondiamo a 5 decimali
    quantity = round(quantity, 5)

    st.write(f"Placing BUY order for BTC amount: {quantity} (≈ ${invest_amount})")

    order = place_order(SYMBOL, SIDE_BUY, quantity)
    if order:
        st.success("Trade completed!")
    else:
        st.error("Trade failed.")

# Streamlit UI
def main():
    st.title("🤖 AI Trading Bot - Binance Testnet (Advanced Version)")

    if st.button("Start Trading Bot"):
        trading_bot()

if __name__ == "__main__":
    main()
