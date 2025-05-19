import pandas as pd
from modules.metrics import compute  # hypothetical

def test_single_row_has_no_nans():
    df = pd.DataFrame({"date":["2025-05-19"],"juice":[5],"anxiety":[4]})
    df["date"] = pd.to_datetime(df["date"])
    out = compute(df)
    assert not out.isna().any().any()
