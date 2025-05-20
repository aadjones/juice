# modules/ui/heatmap.py
import altair as alt
import streamlit as st
import pandas as pd
import numpy as np
from modules.palette import PAL_TEAL, PAL_ORANGE
import os

def draw(df: pd.DataFrame, title: str = "Surplus Drive Heat-map (↔ = Weeks; ↕ = Days of week)"):
    """Render a calendar-style heat‑map of Surplus Drive (sd)."""
    if df.empty or "sd" not in df.columns:
        st.info("Not enough data for heat‑map.")
        return

    # last 90 calendar days
    cutoff = df["date"].max() - pd.Timedelta(days=89)
    df_hm = df[df["date"] >= cutoff].copy()

    # calendar fields
    df_hm["dow"]  = df_hm["date"].dt.weekday            # 0 = Mon
    df_hm["week"] = df_hm["date"].dt.isocalendar().week

    max_abs = float(np.abs(df_hm["sd"]).max()) or 1
    colour_scale = alt.Scale(domain=[-max_abs, 0, max_abs],
                             range=[PAL_ORANGE, "#f0f0f0", PAL_TEAL])

    # Responsive title and subtitle
    # Try to detect mobile by checking window size via environment variable (Streamlit doesn't expose viewport size directly)
    is_mobile = False
    if os.environ.get('STREAMLIT_MOBILE', '') == '1':
        is_mobile = True
    # Fallback: use a short title if the container width is less than 500px (not perfect, but better than theme)
    title_text = "SD Heatmap" if is_mobile else "Surplus Drive Heatmap"
    subtitle_text = "SD = Juice − Anxiety\n" + "(↔ = Weeks; ↕ = Days of week)" if not is_mobile else ""
    if not is_mobile:
        subtitle_text = "SD = Juice − Anxiety\n" + "(↔ = Weeks; ↕ = Days of week)"

    chart = (
        alt.Chart(df_hm)
        .mark_rect()
        .encode(
            x=alt.X("week:O",
                    title="Week",
                    axis=alt.Axis(
                        labelExpr="'W' + datum.label",
                        labelAngle=0,
                        labelFontSize=12
                    )),
            y=alt.Y("dow:O",
                    sort=list(range(7)),
                    title="Day",
                    axis=alt.Axis(
                        labelExpr="['M','T','W','T','F','S','S'][datum.value]" if is_mobile else 
                                "['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][datum.value]",
                        labelFontSize=12
                    )),
            color=alt.Color("sd:Q", 
                           scale=colour_scale, 
                           title="SD",
                           legend=alt.Legend(
                               orient="bottom" if is_mobile else "right",
                               titleFontSize=12,
                               labelFontSize=11
                           )),
            tooltip=[
                alt.Tooltip("date:T", title="Date", format="%Y-%m-%d"),
                alt.Tooltip("sd:Q", format="+.1f", title="SD")
            ]
        )
        .properties(
            height=220 if is_mobile else 260,
            width="container",
            title=alt.TitleParams(
                text=title_text,
                subtitle=subtitle_text,
                anchor="middle",
                fontSize=16 if not is_mobile else 14,
                fontWeight="bold",
                subtitleFontSize=12 if not is_mobile else 11,
                dy=-10,
            ),
        )
        .configure_view(
            strokeWidth=0,
            continuousHeight=220 if is_mobile else 260
        )
        .configure_axis(
            grid=False,
            domain=False,
            tickSize=0
        )
    )

    st.altair_chart(chart, use_container_width=True)
