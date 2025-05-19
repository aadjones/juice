import streamlit as st
import pandas as pd
from datetime import date
from modules.storage import upsert_entry, DATA_DIR, DEMO_FILE
import shutil
import os

def _nickname_prompt():
    """Ask first‑time visitors for a nickname; allow switch later."""
    if "nickname" not in st.session_state:
        st.sidebar.subheader("👋 First time here?")
        nick = st.sidebar.text_input(
            "Pick a nickname to start your own log:",
            placeholder="e.g. nebula42"
        )
        if nick:
            st.session_state["nickname"] = nick.strip()
            st.rerun()               # reload so the rest of the UI sees it
    else:
        st.sidebar.caption(f"Active profile: **{st.session_state.nickname}**")
        if st.sidebar.button("Switch profile"):
            del st.session_state["nickname"]
            st.rerun()


def draw(df_raw):
    _nickname_prompt()
    st.sidebar.header("Log / Edit Entry  📅")

    # --- choose date -------------------------------------------------------
    sel_date = st.sidebar.date_input("Select date", value=date.today())

    # pre‑fill sliders if date already logged
    if not df_raw.empty and sel_date in df_raw["date"].dt.date.values:
        row = df_raw[df_raw["date"].dt.date == sel_date].iloc[0]
        default_juice = int(row.juice)
        default_anx   = int(row.anxiety)
        default_event = "" if pd.isna(row.event) else str(row.event)
    else:
        default_juice, default_anx, default_event = 5, 5, ""

    juice   = st.sidebar.slider("Juice (0-10)", 0, 10, value=default_juice)
    anxiety = st.sidebar.slider("Anxiety (0-10)", 0, 10, value=default_anx)
    event   = st.sidebar.text_input("Event note (optional)", value=default_event)

    if st.sidebar.button("Save / Update"):
        # Save to the correct file based on nickname
        if "nickname" in st.session_state:
            user_file = DATA_DIR / f"{st.session_state['nickname']}.csv"
            upsert_entry(sel_date, int(juice), int(anxiety), event.strip())
            st.sidebar.success(f"Entry saved for {sel_date.isoformat()}!")
            st.rerun()
        else:
            st.sidebar.warning("Pick a nickname to start your own log!")
