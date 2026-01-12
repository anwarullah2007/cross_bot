import time
from telegram import Bot
from config import (
    BOT_TOKEN,
    COINGECKO_API_KEY,
    COINS,
    ALERT_PERCENT,
    SCAN_INTERVAL,
    CHAT_ID
)
from scanner import fetch_market_data
from state import load_state, save_state

bot = Bot(token=BOT_TOKEN)

def send_alert(coin, price, change):
    message = (
        f"🚨 PUMP ALERT 🚨\n\n"
        f"Coin: {coin.upper()}\n"
        f"Price: ${price:.2f}\n"
        f"24h Change: +{change:.2f}%"
    )
    bot.send_message(chat_id=CHAT_ID, text=message)

def main():
    print("🚀 CoinGecko Pump Alert Bot Started")

    state = load_state()

    while True:
        try:
            data = fetch_market_data(COINS, COINGECKO_API_KEY)

            for coin, info in data.items():
                change = info.get("usd_24h_change", 0)
                price = info.get("usd", 0)

                last_alerted = state.get(coin, False)

                if change >= ALERT_PERCENT and not last_alerted:
                    send_alert(coin, price, change)
                    state[coin] = True

                if change < ALERT_PERCENT:
                    state[coin] = False

            save_state(state)

        except Exception as e:
            print("⚠️ Error:", e)

        time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    main()
