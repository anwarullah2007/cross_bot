from data import fetch_data
from indicators import detect_cross
from config import PAIRS, TIMEFRAME, SHORT_MA, LONG_MA
from state import load_state, save_state

async def scan_and_alert(bot, chat_id):
    state = load_state()

    for pair in PAIRS:
        df = fetch_data(pair, TIMEFRAME)
        signal = detect_cross(df, SHORT_MA, LONG_MA)

        if not signal:
            continue

        last = state.get(pair)
        if last == signal:
            continue

        state[pair] = signal
        save_state(state)

        message = (
            f"📊 {pair}\n"
            f"{'🟢 Golden Cross' if signal == 'GOLDEN' else '🔴 Death Cross'}\n"
            f"MA: {SHORT_MA}/{LONG_MA}\n"
            f"Timeframe: {TIMEFRAME}"
        )

        await bot.send_message(chat_id=chat_id, text=message)
