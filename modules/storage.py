# modules/storage.py
from pathlib import Path
import pandas as pd
from datetime import date

DATA_PATH = Path("data/log.csv")
_COLUMNS  = ["date", "juice", "anxiety"]

def _ensure_csv():
    """Create or repair the CSV so it always has headers."""
    DATA_PATH.parent.mkdir(exist_ok=True)
    expected_header = ','.join(_COLUMNS)
    if not DATA_PATH.exists() or DATA_PATH.stat().st_size == 0:
        pd.DataFrame(columns=_COLUMNS).to_csv(DATA_PATH, index=False)
    else:
        with open(DATA_PATH, 'r') as f:
            first_line = f.readline().strip()
        if first_line != expected_header:
            # Read the rest of the file
            df = pd.read_csv(DATA_PATH, header=None, names=_COLUMNS)
            # Overwrite with correct header
            df.to_csv(DATA_PATH, index=False)

def load_log() -> pd.DataFrame:
    _ensure_csv()
    try:
        return pd.read_csv(DATA_PATH, parse_dates=["date"])
    except ValueError:                      # headers missing or corrupted
        return pd.DataFrame(columns=_COLUMNS)

def append_entry(juice: int, anxiety: int) -> None:
    _ensure_csv()
    df = pd.DataFrame([[date.today(), juice, anxiety]], columns=_COLUMNS)
    df.to_csv(DATA_PATH, mode="a", header=False, index=False)
