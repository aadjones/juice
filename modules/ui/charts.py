# modules/ui/charts.py  – modular version
import altair as alt
import streamlit as st
from pathlib import Path
import pandas as pd

from modules.palette import PAL_BLUE, PAL_ORANGE, PAL_TEAL

EXPORT_DIR = Path("export_charts")
EXPORT_DIR.mkdir(exist_ok=True)


# ── internal helpers ───────────────────────────────────────────────────────
def _base(df: pd.DataFrame) -> alt.Chart:
    """Common x‑encoding (date on x‑axis)."""
    return alt.Chart(df).encode(x="date:T")


def _export_png(chart: alt.Chart, filename: str) -> Path | None:
    """Save chart as PNG; return path or None if export fails."""
    path = EXPORT_DIR / filename
    try:
        import altair_saver  # backend auto‑registered
        chart.save(path, scale_factor=2)
        return path
    except Exception as e:
        st.warning(f"Could not export {filename}: {e}")
        return None


# ── Juice & Anxiety (+ optional events) ────────────────────────────────────
import pandas as pd
import altair as alt
from modules.palette import PAL_BLUE, PAL_ORANGE

# -------------------------------------------------------------------------
def juice_anxiety_chart(df: pd.DataFrame) -> tuple[alt.Chart, Path | None]:
    """
    Build Juice–Anxiety line/point chart with a proper legend.
    Returns (Altair chart, PNG path or None).
    """
    # ---- reshape to long form so Altair can auto‑legend ------------------
    df_long = df.melt(
        id_vars=["date"],
        value_vars=["juice", "anxiety"],
        var_name="metric",
        value_name="value",
    )

    colour_scale = alt.Scale(domain=["juice", "anxiety"],
                             range=[PAL_BLUE, PAL_ORANGE])
    shape_scale  = alt.Scale(domain=["juice", "anxiety"],
                             range=["circle", "square"])

    # ---- line layer (dash carries semantics, but excluded from legend) ---
    line = (
        alt.Chart(df_long)
        .mark_line(strokeWidth=2)
        .encode(
            x="date:T",
            y=alt.Y("value:Q", title="Level"),
            color=alt.Color("metric:N", scale=colour_scale,
                            legend=alt.Legend(title="")),
            strokeDash=alt.StrokeDash(
                "metric:N",
                scale=alt.Scale(domain=["juice", "anxiety"],
                                range=[[1, 0], [6, 3]]),
                legend=None,   # keep dash pattern out of legend swatch
            ),
        )
    )

    # ---- point layer (solid fill drives legend symbols) ------------------
    points = (
        alt.Chart(df_long)
        .mark_point(size=70, filled=True)
        .encode(
            x="date:T",
            y="value:Q",
            color=alt.Color("metric:N", scale=colour_scale, legend=None),
            shape=alt.Shape("metric:N", scale=shape_scale,
                            legend=alt.Legend(title="")),
        )
    )

    # ---- optional event annotations --------------------------------------
    has_evt = ("event" in df.columns
               and df["event"].fillna("").str.strip().ne("").any())

    if has_evt:
        evt_df = df[df["event"].fillna("").str.strip() != ""]
        annot = (
            alt.Chart(evt_df)
            .mark_text(align="left", dx=5, dy=-5, color="#666", fontSize=11)
            .encode(x="date:T", y="juice:Q", text="event:N")
        )
        chart = line + points + annot
        title_txt = "Juice & Anxiety over Time"
    else:
        chart = line + points
        title_txt = "Juice & Anxiety over Time"

    # Apply view configuration to the final combined chart
    chart = (
        chart
        .properties(
            height=260,
            title=alt.TitleParams(text=title_txt, anchor="middle", fontSize=16, fontWeight="bold", dy=-10)
        )
        .configure_view(continuousHeight=240)
    )

    # ---- export PNG for board deck ---------------------------------------
    png_path = _export_png(chart, "juice_anxiety.png")
    return chart, png_path



# ── GQ trend line ──────────────────────────────────────────────────────────
def gq_chart(df: pd.DataFrame) -> alt.Chart:
    """Build GQ line chart."""
    return (
        alt.Chart(df)
        .mark_line(strokeWidth=2)
        .encode(
            x="date:T",
            y=alt.Y("gq:Q", title="GQ = Juice / Anxiety"),
            tooltip=["date:T", alt.Tooltip("gq:Q", format=".2f")],
        )
        .properties(
            title=alt.TitleParams(text="Gumption Quotient Trend", anchor="middle", fontSize=16, fontWeight="bold", dy=-10),
            height=240
        )
    )



# ── dGQ/dt bars + 7‑day trend ─────────────────────────────────────────────
def dgqdt_chart(df: pd.DataFrame) -> alt.Chart:
    """Bar chart for dGQ/dt with 7-day moving average trend line."""
    bars = (
        alt.Chart(df)
        .mark_bar(size=8)
        .encode(
            x="date:T",
            y=alt.Y("dgqdt:Q", title="dGQ/dt"),
            color=alt.condition(
                "datum.dgqdt > 0", alt.value(PAL_TEAL), alt.value(PAL_ORANGE)
            ),
            tooltip=["date:T", alt.Tooltip("dgqdt:Q", format="+.2f")],
        )
    )
    trend = (
        alt.Chart(df)
        .mark_line(color="#222", strokeDash=[4, 2])
        .encode(
            x="date:T",
            y="dgqdt_7d:Q",
        )
    )
    return (
        (bars + trend)
        .properties(
            title=alt.TitleParams(text="Daily & 7-day change in GQ", anchor="middle", fontSize=16, fontWeight="bold", dy=-10),
            height=240
        )
    )


# ── public entrypoint for app.py ───────────────────────────────────────────
def draw(df: pd.DataFrame) -> Path | None:
    """Render all charts to Streamlit; return PNG path for board‑deck."""
    # ① Juice / Anxiety
    juice_chart, png_path = juice_anxiety_chart(df)
    st.altair_chart(juice_chart, use_container_width=True)

    # ② GQ
    st.altair_chart(gq_chart(df), use_container_width=True)

    # ③ derivative
    if len(df) > 1 and df["dgqdt"].abs().sum() > 0:
        st.altair_chart(dgqdt_chart(df), use_container_width=True)

    return png_path
