import os
import sys

BOT_TOKEN = os.getenv("BOT_TOKEn")

if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN environment variable is NOT set")
    sys.exit(1)

PAIRS = ["BTCUSDT", "ETHUSDT"]
TIMEFRAME = "15m"

PRICE_PUMP_PERCENT = 3.0
VOLUME_MULTIPLIER = 2.0

SCAN_INTERVAL = 60 * 5

