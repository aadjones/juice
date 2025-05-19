import streamlit as st
import pandas as pd
from datetime import date
from modules.storage import upsert_entry


def draw(df_raw):
    st.sidebar.header("Log / Edit Entry  📅")

    # --- choose date -------------------------------------------------------
    sel_date = st.sidebar.date_input("Select date", value=date.today())

    # pre‑fill sliders if date already logged
    if not df_raw.empty and sel_date in df_raw["date"].dt.date.values:
        row = df_raw[df_raw["date"].dt.date == sel_date].iloc[0]
        default_juice = int(row.juice)
        default_anx   = int(row.anxiety)
        default_event = default_event = "" if pd.isna(row.event) else str(row.event)
    else:
        default_juice, default_anx, default_event = 5, 5, ""

    juice   = st.sidebar.slider("Juice (0‑10)", 0, 10, value=default_juice)
    anxiety = st.sidebar.slider("Anxiety (0‑10)", 0, 10, value=default_anx)
    event   = st.sidebar.text_input("Event note (optional)", value=default_event)

    if st.sidebar.button("Save / Update"):
        upsert_entry(sel_date, int(juice), int(anxiety), event.strip())
        st.sidebar.success(f"Entry saved for {sel_date.isoformat()}!")
        st.rerun()
