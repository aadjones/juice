# modules/metrics.py
import pandas as pd
import numpy as np

def compute(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    out = df.copy()

    # Core metrics
    out["gq"]      = out["juice"] / out["anxiety"].replace(0, np.nan)
    out["deltaJ"]  = out["juice"] - out["anxiety"]
    out["ohm"]     = 1 / out["gq"]

    # Time deltas (days) for derivatives
    out["days"] = (out["date"] - out["date"].iloc[0]).dt.total_seconds() / 86400
    out["dgqdt"] = out["gq"].diff() / out["days"].diff()

    # 7‑day simple moving average (centered)
    out["dgqdt_7d"] = out["dgqdt"].rolling(window=7, center=True).mean()

    # 4‑week rolling σ of Juice (entropy proxy)
    out["sigma"] = out["juice"].rolling(window=4, min_periods=2).std()

    return out
