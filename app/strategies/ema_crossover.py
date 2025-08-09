
import pandas as pd

def ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()

def generate_signal(df: pd.DataFrame, fast: int, slow: int) -> str:
    df = df.copy()
    df["ema_fast"] = ema(df["close"], fast)
    df["ema_slow"] = ema(df["close"], slow)
    # Signal on the last two bars cross
    if len(df) < slow + 2:
        return "HOLD"
    prev_fast, prev_slow = df["ema_fast"].iloc[-2], df["ema_slow"].iloc[-2]
    curr_fast, curr_slow = df["ema_fast"].iloc[-1], df["ema_slow"].iloc[-1]
    if prev_fast <= prev_slow and curr_fast > curr_slow:
        return "BUY"
    if prev_fast >= prev_slow and curr_fast < curr_slow:
        return "SELL"
    return "HOLD"
