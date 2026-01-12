from data import fetch_data
from indicators import detect_pump
from config import PAIRS, TIMEFRAME, PRICE_PUMP_PERCENT, VOLUME_MULTIPLIER
from state import load_state, save_state

def scan_and_alert(bot, chat_id):
    state = load_state()
    alerts = state.get("alerts", {})

    for pair in PAIRS:
        try:
            df = fetch_data(pair, TIMEFRAME)
            pump = detect_pump(df, PRICE_PUMP_PERCENT, VOLUME_MULTIPLIER)
        except Exception as e:
            print(f"[ERROR] {pair}: {e}")
            continue

        if not pump:
            continue

        # Avoid spam (one alert per candle)
        last_time = str(df.iloc[-1]["time"])
        if alerts.get(pair) == last_time:
            continue

        alerts[pair] = last_time
        state["alerts"] = alerts
        save_state(state)

        message = (
            f"🚀 *PUMP ALERT*\n\n"
            f"📊 Coin: *{pair}*\n"
            f"📈 Price Change: *{pump['price_change']}%*\n"
            f"🔊 Volume: *{pump['volume']}*\n"
            f"📊 Avg Volume: *{pump['avg_volume']}*\n"
            f"⏱ Timeframe: {TIMEFRAME}"
        )

        bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
