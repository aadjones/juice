# modules/metrics.py
# ---------------------------------------------------------------------
# Central math engine for the Psychic‑Physics dashboard
#
# INPUT  : DataFrame with columns ["date", "juice", "anxiety"]
# OUTPUT : Same rows plus derived metrics
# ---------------------------------------------------------------------

import pandas as pd
import numpy as np


def _days_since_start(series: pd.Series) -> pd.Series:
    """Return float days from first date in series."""
    seconds = (series - series.iloc[0]).dt.total_seconds()
    return seconds / 86_400  # seconds → days


def compute(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add all derived psychic‑physics metrics.

    Columns created
    ---------------
    gq        – Gumption Quotient (Juice ÷ Anxiety)
    sd        – Surplus Drive    (Juice − Anxiety)      [hidden KPI]
    dJdt      – First derivative of Juice (per day)
    focus_flux– Φf  = dJdt · sign(sd)                   (momentum)
    dgqdt     – Instant slope of GQ (per day)
    dgqdt_7d  – 7‑day moving average of dgqdt
    sigma     – Rolling 4‑entry σ of Juice  (Focus‑Entropy)
    fortitude – 30‑day running sum of positive sd (Fortitude Farad)
    """
    if df.empty:
        return df.copy()

    out = df.sort_values("date").reset_index(drop=True).copy()

    # -----------------------------------------------------------------
    # Core ratios / differences
    # -----------------------------------------------------------------
    out["gq"] = out["juice"] / out["anxiety"].replace(0, np.nan)
    out["sd"] = out["juice"] - out["anxiety"]                 # hidden but useful

    # -----------------------------------------------------------------
    # Time axis & first derivatives
    # -----------------------------------------------------------------
    out["days"] = _days_since_start(out["date"])
    out["dJdt"] = out["juice"].diff() / out["days"].diff()    # Juice velocity
    out["dgqdt"] = out["gq"].diff() / out["days"].diff()      # GQ slope

    # Signed momentum: only "productive" if surplus drive is positive
    out["focus_flux"] = out["dJdt"] * np.sign(out["sd"])

    # -----------------------------------------------------------------
    # Rolling & cumulative stats
    # -----------------------------------------------------------------
    out["dgqdt_7d"] = out["dgqdt"].rolling(window=7, min_periods=2).mean()
    out["sigma"]    = out["juice"].rolling(window=4,  min_periods=2).std()
    out["fortitude"] = (
        out["sd"].clip(lower=0)           # only positive surplus
            .rolling(window=30, min_periods=1)
            .sum()
    )

    # replace single-row NaNs with 0 for display purposes
    for col in ["dJdt", "dgqdt", "dgqdt_7d", "focus_flux", "sigma"]:
        out[col] = out[col].fillna(0)

    return out