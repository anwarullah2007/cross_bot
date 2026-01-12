import threading
import time
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

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
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=1, use_context=True)

# ---------- COMMAND ----------
def start(update, context):
    chat_id = str(update.effective_chat.id)

    state = load_state()
    users = state.get("users", [])

    if chat_id not in users:
        users.append(chat_id)
        state["users"] = users
        save_state(state)

    bot.send_message(
        chat_id=chat_id,
        text="✅ Subscribed!\nYou will receive pump alerts 🚀"
    )

dispatcher.add_handler(CommandHandler("start", start))

# ---------- WEBHOOK ----------
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# ---------- SCANNER ----------
def scan_loop():
    print("🚀 CoinGecko Alert Scanner Started")

    while True:
        try:
            state = load_state()
            users = state.get("users", [])
            alerted = state.get("alerted", {})

            data = fetch_market_data(COINS, COINGECKO_API_KEY)

            for coin, info in data.items():
                change = info.get("usd_24h_change", 0)
                price = info.get("usd", 0)

                if change >= ALERT_PERCENT and not alerted.get(coin):
                    for user in users:
                        bot.send_message(
                            chat_id=user,
                            text=(
                                f"🚨 PUMP ALERT 🚨\n\n"
                                f"Coin: {coin.upper()}\n"
                                f"Price: ${price:.2f}\n"
                                f"24h Change: +{change:.2f}%"
                            )
                        )
                    alerted[coin] = True

                if change < ALERT_PERCENT:
                    alerted[coin] = False

            state["alerted"] = alerted
            save_state(state)

        except Exception as e:
            print("⚠️ Scanner error:", e)

        time.sleep(SCAN_INTERVAL)

# ---------- MAIN ----------
if __name__ == "__main__":
    threading.Thread(target=scan_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=8080)
