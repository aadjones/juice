# modules/storage.py
from pathlib import Path
from datetime import date
import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "log.csv"
_COLUMNS  = ["date", "juice", "anxiety", "event"]   # add event column

def _init_csv():
    DATA_PATH.parent.mkdir(exist_ok=True)
    if not DATA_PATH.exists():
        pd.DataFrame(columns=_COLUMNS).to_csv(DATA_PATH, index=False)
    else:
        # if header is missing event, repair in place
        df = pd.read_csv(DATA_PATH)
        if "event" not in df.columns:
            df["event"] = ""
            df.to_csv(DATA_PATH, index=False)

def load_log() -> pd.DataFrame:
    _init_csv()
    return pd.read_csv(DATA_PATH, parse_dates=["date"])

def append_entry(juice: int, anxiety: int, event: str = "") -> None:
    """Append one row to the CSV."""
    _init_csv()
    row = {
        "date": date.today(),
        "juice": juice,
        "anxiety": anxiety,
        "event": event
    }
    pd.DataFrame([row]).to_csv(DATA_PATH, mode="a", header=False, index=False)

def upsert_entry(day, juice: int, anxiety: int, event: str = "") -> None:
    """
    Insert or update a record for `day` (datetime.date).
    """
    _init_csv()
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])

    mask = df["date"].dt.date == day
    if mask.any():
        # update existing row
        df.loc[mask, ["juice", "anxiety", "event"]] = [juice, anxiety, event]
    else:
        # append new row
        new_row = {"date": day, "juice": juice, "anxiety": anxiety, "event": event}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df.sort_values("date").to_csv(DATA_PATH, index=False)
