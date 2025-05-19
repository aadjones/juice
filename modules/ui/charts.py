# modules/ui/charts.py
import altair as alt
import streamlit as st
from modules.palette import PAL_BLUE, PAL_ORANGE, PAL_TEAL

def _base(df):
    return alt.Chart(df).encode(x="date:T")

def draw(df):
    # ── Juice & Anxiety layers ────────────────────────────────────────────
    juice_line = (
        _base(df)
        .mark_line(point=alt.OverlayMarkDef(shape="circle", size=50),
                   strokeWidth=2, color=PAL_BLUE)
        .encode(
            y=alt.Y("juice:Q",
                    title="Jc (solid) | Ax (dashed)",
                    scale=alt.Scale(domain=[0, 10]))
        )
    )

    anx_line = (
        _base(df)
        .mark_line(point=alt.OverlayMarkDef(shape="square", size=50),
                   strokeDash=[6, 3], strokeWidth=2, color=PAL_ORANGE)
        .encode(y="anxiety:Q")
    )

    # ── Optional annotation layer ────────────────────────────────────────
    has_events = (
        "event" in df.columns and
        df["event"].fillna("").str.strip().ne("").any()
    )

    if has_events:
        df_annot = df[df["event"].fillna("").str.strip() != ""]
        annot = (
            alt.Chart(df_annot)
            .mark_text(align="left", dx=5, dy=-5, color="#666", fontSize=11)
            .encode(x="date:T", y="juice:Q", text="event:N")
        )
        main_chart = juice_line + anx_line + annot
        title_txt  = "Juice, Anxiety & Events"
    else:
        main_chart = juice_line + anx_line
        title_txt  = "Juice vs. Anxiety"

    st.altair_chart(
        main_chart.properties(height=260, title=title_txt),
        use_container_width=True
    )

    # ── GQ line ───────────────────────────────────────────────────────────
    gq_line = (
        _base(df)
        .mark_line(point=True, strokeWidth=2, color=PAL_TEAL)
        .encode(
            y=alt.Y("gq:Q", title="GQ",
                    scale=alt.Scale(domain=[0, max(2.5, float(df.gq.max())*1.1)]))
        )
        .properties(height=200)
    )
    st.altair_chart(gq_line, use_container_width=True)

    # ── dGQ/dt bars & trend ───────────────────────────────────────────────
    bars = (
        _base(df)
        .mark_bar(size=6)
        .encode(
            y=alt.Y("dgqdt:Q", title="d GQ / d t"),
            color=alt.condition("datum.dgqdt > 0",
                                alt.value(PAL_TEAL),
                                alt.value(PAL_ORANGE))
        )
    )
    trend = _base(df).mark_line(color="black", strokeDash=[4, 2])\
                     .encode(y="dgqdt_7d:Q")

    st.altair_chart(
        (bars + trend)
        .properties(height=200, title="Daily & 7‑day change in GQ"),
        use_container_width=True
    )