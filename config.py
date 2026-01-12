import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

PAIRS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
TIMEFRAME = "1d"        # 1d recommended for crosses
SHORT_MA = 50
LONG_MA = 200
SCAN_INTERVAL = 60 * 30  # 30 minutes
