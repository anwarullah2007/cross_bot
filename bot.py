import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
from config import BOT_TOKEN, SCAN_INTERVAL
from scanner import scan_and_alert

CHAT_ID = None

async def start(update, context):
    global CHAT_ID
    CHAT_ID = update.effective_chat.id
    await update.message.reply_text("✅ Cross Bot Activated")

async def background_scanner(app):
    while True:
        if CHAT_ID:
            await scan_and_alert(app.bot, CHAT_ID)
        await asyncio.sleep(SCAN_INTERVAL)

async def post_init(app):
    # Start background task once bot is fully initialized
    asyncio.create_task(background_scanner(app))

def main():
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler("start", start))

    # PTB owns the event loop
    app.run_polling()

if __name__ == "__main__":
    main()
