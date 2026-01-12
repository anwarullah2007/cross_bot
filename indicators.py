def detect_pump(df, price_percent, volume_multiplier):
    if len(df) < 20:
        return None

    last = df.iloc[-1]
    prev = df.iloc[-2]

    price_change = ((last.close - prev.close) / prev.close) * 100
    avg_volume = df["volume"].iloc[-20:-1].mean()

    if price_change >= price_percent and last.volume >= avg_volume * volume_multiplier:
        return {
            "price_change": round(price_change, 2),
            "volume": round(last.volume, 2),
            "avg_volume": round(avg_volume, 2)
        }

    return None
