import requests
import pandas as pd

# ── CONFIG ──────────────────────────────────────────────
TELEGRAM_TOKEN = "8707758476:AAE2tFYu-VJxZYDwr9n3w2WXffd3WgENtkI"
CHAT_ID        = "451489432"
FAST_EMA       = 9
SLOW_EMA       = 20
TIMEFRAME      = "5m"   # change to 15m, 4h etc if you want
# ────────────────────────────────────────────────────────

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def get_xauusd_prices():
    import yfinance as yf
    data = yf.download("GC=F", period="5d", interval=TIMEFRAME, progress=False)
    return data["Close"]

def check_crossover():
    prices = get_xauusd_prices()
    fast = prices.ewm(span=FAST_EMA, adjust=False).mean()
    slow = prices.ewm(span=SLOW_EMA, adjust=False).mean()

    # Extract single float values from last two candles
    prev_fast = float(fast.iloc[-2].item())
    prev_slow = float(slow.iloc[-2].item())
    curr_fast = float(fast.iloc[-1].item())
    curr_slow = float(slow.iloc[-1].item())
    price     = round(float(prices.iloc[-1].item()), 2)

    if prev_fast <= prev_slow and curr_fast > curr_slow:
        send_telegram(
            f"🟢 XAUUSD BULLISH CROSSOVER\n"
            f"EMA{FAST_EMA} crossed ABOVE EMA{SLOW_EMA}\n"
            f"Price: {price}\n"
            f"Timeframe: {TIMEFRAME}\n"
            f"Consider: BUY opportunity"
        )
        print("Bullish crossover detected — alert sent!")

    elif prev_fast >= prev_slow and curr_fast < curr_slow:
        send_telegram(
            f"🔴 XAUUSD BEARISH CROSSOVER\n"
            f"EMA{FAST_EMA} crossed BELOW EMA{SLOW_EMA}\n"
            f"Price: {price}\n"
            f"Timeframe: {TIMEFRAME}\n"
            f"Consider: SELL opportunity"
        )
        print("Bearish crossover detected — alert sent!")

    else:
        print("No crossover right now. Script working fine!")

if __name__ == "__main__":
    check_crossover()
