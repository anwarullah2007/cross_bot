import os
import sys

BOT_TOKEN = os.getenv("BOT_TOKEN")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

if not BOT_TOKEN:
    print("❌ BOT_TOKEN not set")
    sys.exit(1)

if not COINGECKO_API_KEY:
    print("❌ COINGECKO_API_KEY not set")
    sys.exit(1)

# Coins to monitor (CoinGecko IDs)
COINS = ["bitcoin", "ethereum"]

# Alert threshold
ALERT_PERCENT = 1.0  # 1%

# Scan interval (seconds)
SCAN_INTERVAL = 60

# Telegram chat
CHAT_ID = 123456789  # <-- REPLACE WITH YOUR CHAT ID
