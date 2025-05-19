import streamlit as st
from modules.storage import load_log
from modules.metrics import compute
from modules.units import UNIT_DEFS
from modules.ui import sidebar, kpi, charts   # __init__.py re‑exports

st.set_page_config(page_title="Aaron Analytics™", layout="wide")

df_raw = load_log()
sidebar.draw(df_raw)           # sidebar first (may rerun)

df = compute(df_raw)
if df.empty:
    st.warning("No data yet. Use the sidebar to log your first entry.")
    st.stop()

latest = df.iloc[-1]
kpi.draw(df, latest)
st.caption(UNIT_DEFS)

charts.draw(df)                # main charts
