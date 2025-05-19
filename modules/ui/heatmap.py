# modules/ui/heatmap.py
import altair as alt
import streamlit as st
import pandas as pd
import numpy as np
from modules.palette import PAL_TEAL, PAL_ORANGE

def draw(df: pd.DataFrame, title: str = "Surplus Drive Calendar Heat‑map"):
    """Render a calendar-style heat‑map of Surplus Drive (sd)."""
    if df.empty or "sd" not in df.columns:
        st.info("Not enough data for heat‑map.")
        return

    # Use last 90 days so chart doesn't get unwieldy
    df_hm = df.copy().tail(90)

    # Prepare calendar fields
    df_hm["dow"]   = df_hm["date"].dt.weekday            # 0=Mon
    df_hm["week"]  = df_hm["date"].dt.isocalendar().week
    df_hm["month"] = df_hm["date"].dt.strftime("%b")

    # Symmetric colour domain around 0
    max_abs = float(np.abs(df_hm["sd"]).max()) or 1
    colour_scale = alt.Scale(
        domain=[-max_abs, 0, max_abs],
        range=[PAL_ORANGE, "#f0f0f0", PAL_TEAL]
    )

    chart = (
        alt.Chart(df_hm)
        .mark_rect()
        .encode(
            x=alt.X("week:O", title="ISO week"),
            y=alt.Y("dow:O",
                    sort=list(range(7)),
                    title="Day of week",
                    axis=alt.Axis(labelExpr="['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][datum.value]")),
            color=alt.Color("sd:Q", scale=colour_scale, title="SD"),
            tooltip=[
                alt.Tooltip("date:T", title="Date"),
                alt.Tooltip("sd:Q", format="+.1f", title="SD")
            ]
        )
        .properties(
            height=200,
            width=600,
            title={"text": title,
           "subtitle": "SD = Juice - Anxiety  (positive = surplus)",
           "subtitleFontSize":12}
        )
    )

    st.altair_chart(chart, use_container_width=True)