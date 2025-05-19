# modules/storage.py
from pathlib import Path
import os, pandas as pd, streamlit as st

DATA_DIR  = Path(os.getenv("DATA_DIR", "data"))
DATA_DIR.mkdir(exist_ok=True)

DEMO_FILE = DATA_DIR / "demo.csv"
_COLUMNS  = ["date", "juice", "anxiety", "event"]

# ------------------------------------------------------------------
def _uid() -> str | None:
    return st.session_state.get("nickname")

def _path() -> Path:
    """Active CSV path."""
    return DEMO_FILE if _uid() is None else DATA_DIR / f"{_uid()}.csv"

def _ensure():
    """If active CSV is missing, create blank file with headers."""
    p = _path()
    if not p.exists():
        pd.DataFrame(columns=_COLUMNS).to_csv(p, index=False)

# ------------------------------------------------------------------
def load_log() -> pd.DataFrame:
    _ensure()
    return pd.read_csv(_path(), parse_dates=["date"])

def upsert_entry(day, juice: int, anxiety: int, event: str = ""):
    _ensure()
    path = _path()
    df = pd.read_csv(path, parse_dates=["date"])

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    day_ts     = pd.Timestamp(day)
    mask       = df["date"].dt.date == day_ts.date()

    if mask.any():
        df.loc[mask, ["juice", "anxiety", "event"]] = [juice, anxiety, event]
    else:
        df = pd.concat(
            [df, pd.DataFrame([{
                "date": day_ts, "juice": juice, "anxiety": anxiety, "event": event
            }])], ignore_index=True)

    df.sort_values("date").to_csv(path, index=False)
