from modules.ui import charts
import pandas as pd
import pytest
def test_png_export(tmp_path):
    df = pd.DataFrame({
        "date": ["2025-05-19"],
        "juice": [5],
        "anxiety": [4]
    })
    df["date"] = pd.to_datetime(df["date"])

    charts.EXPORT_DIR = tmp_path
    _, png = charts.juice_anxiety_chart(df)

    # Skip assertion if PNG export unavailable on CI runner
    if png is None:
        pytest.skip("PNG backend not available in CI container")
    assert png.exists() and png.stat().st_size > 0

