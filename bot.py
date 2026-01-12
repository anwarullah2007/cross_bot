import time
from telegram.ext import Updater, CommandHandler
from config import BOT_TOKEN, SCAN_INTERVAL
from scanner import scan_and_alert
from state import load_state, save_state

def start(update, context):
    state = load_state()
    state["chat_id"] = update.message.chat_id
    save_state(state)
    update.message.reply_text("🚀 Crypto Pump Bot Activated")

def status(update, context):
    update.message.reply_text("🟢 Pump bot is running")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))

    updater.start_polling()
    print("Pump bot started...")

    while True:
        state = load_state()
        chat_id = state.get("chat_id")

        if chat_id:
            scan_and_alert(updater.bot, chat_id)

        time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    main()
