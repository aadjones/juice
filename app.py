import streamlit as st
from modules.report import build_deck
from modules.storage import load_log
from modules.metrics import compute
from modules.units import UNIT_DEFS
from modules.ui import sidebar, kpi, charts, heatmap

st.set_page_config(page_title="Demby Analytics™", layout="wide")

df_raw = load_log()
sidebar.draw(df_raw)           # sidebar first (may rerun)

df = compute(df_raw)
if df.empty:
    st.warning("No data yet. Use the sidebar to log your first entry.")
    st.stop()

latest = df.iloc[-1]
kpi.draw(df, latest)
st.caption(UNIT_DEFS)

chart_path = charts.draw(df)   # main charts
heatmap.draw(df)               # calendar view

# after all charts rendered
pptx_file  = build_deck(df, {"juice_anx": chart_path})

with open(pptx_file, "rb") as f:
    st.download_button(
        "Download Board Deck",
        data=f,
        file_name=pptx_file.name,
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )
