def detect_cross(df, short_ma=50, long_ma=200):
    # Calculate moving averages manually (no pandas_ta)
    df["short_ma"] = df["close"].rolling(window=short_ma).mean()
    df["long_ma"] = df["close"].rolling(window=long_ma).mean()

    # Need at least 2 candles with MA values
    if len(df) < long_ma + 2:
        return None

    prev = df.iloc[-2]
    curr = df.iloc[-1]

    # Golden Cross
    if prev.short_ma < prev.long_ma and curr.short_ma > curr.long_ma:
        return "GOLDEN"

    # Death Cross
    if prev.short_ma > prev.long_ma and curr.short_ma < curr.long_ma:
        return "DEATH"

    return None
