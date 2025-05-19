from modules.ui import charts
import pandas as pd

def test_png_export(tmp_path):
    df = pd.DataFrame({"date":["2025-05-19"],"juice":[5],"anxiety":[4]})
    df["date"] = pd.to_datetime(df["date"])
    charts.EXPORT_DIR = tmp_path        # redirect export dir
    _, png = charts.juice_anxiety_chart(df)
    assert png and png.exists() and png.stat().st_size > 0
