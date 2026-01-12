import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

# 🔥 ONLY TWO COINS FOR TESTING
PAIRS = ["BTCUSDT", "ETHUSDT"]

TIMEFRAME = "15m"

# Pump conditions
PRICE_PUMP_PERCENT = 3.0      # 3% price jump
VOLUME_MULTIPLIER = 2.0       # 2x volume

SCAN_INTERVAL = 60 * 5        # 5 minutes
