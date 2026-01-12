import time
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

from config import (
    BOT_TOKEN,
    COINGECKO_API_KEY,
    COINS,
    ALERT_PERCENT,
    SCAN_INTERVAL
)
from scanner import fetch_market_data
from state import load_state, save_state

bot = Bot(token=BOT_TOKEN)

# ---- USER COMMAND ----
def start(update: Update, context: CallbackContext):
    chat_id = str(update.effective_chat.id)

    state = load_state()
    users = state.get("users", [])

    if chat_id not in users:
        users.append(chat_id)
        state["users"] = users
        save_state(state)

    update.message.reply_text(
        "✅ You are subscribed!\n"
        "You will receive pump alerts automatically 🚀"
    )

# ---- ALERT FUNCTION ----
def send_alert(users, coin, price, change):
    message = (
        f"🚨 PUMP ALERT 🚨\n\n"
        f"Coin: {coin.upper()}\n"
        f"Price: ${price:.2f}\n"
        f"24h Change: +{change:.2f}%"
    )

    for chat_id in users:
        try:
            bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"⚠️ Failed to send to {chat_id}: {e}")

# ---- BACKGROUND SCANNER ----
def scan_loop():
    print("🚀 CoinGecko Personal Alert Bot Started")

    state = load_state()
    alerted = state.get("alerted", {})

    while True:
        try:
            data = fetch_market_data(COINS, COINGECKO_API_KEY)
            users = state.get("users", [])

            for coin, info in data.items():
                change = info.get("usd_24h_change", 0)
                price = info.get("usd", 0)

                already_alerted = alerted.get(coin, False)

                if change >= ALERT_PERCENT and not already_alerted:
                    send_alert(users, coin, price, change)
                    alerted[coin] = True

                if change < ALERT_PERCENT:
                    alerted[coin] = False

            state["alerted"] = alerted
            save_state(state)

        except Exception as e:
            print("⚠️ Scanner error:", e)

        time.sleep(SCAN_INTERVAL)

# ---- MAIN ----
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()

    scan_loop()

if __name__ == "__main__":
    main()
