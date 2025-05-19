# app.py
import streamlit as st
import altair as alt
from modules.storage import load_log, append_entry
from modules.metrics import compute

st.set_page_config(
    page_title="Aaron Analytics™ — Psychic KPI Dashboard",
    layout="wide",
)

# ---- Sidebar input ---------------------------------------------------------
st.sidebar.header("Daily Log  📈")
juice   = st.sidebar.slider("Juice (0 – 10)", 0, 10, 5)
anxiety = st.sidebar.slider("Anxiety (0 – 10)", 0, 10, 5)
if st.sidebar.button("Save today"):
    append_entry(juice, anxiety)
    st.sidebar.success("Entry saved!")
    st.rerun()

# ---- Load + compute --------------------------------------------------------
df_raw = load_log()
df     = compute(df_raw)

st.title("Aaron Analytics™ — Psychic Physics Dashboard")

if df.empty:
    st.warning("No data yet. Use the sidebar to log your first entry.")
    st.stop()

latest = df.iloc[-1]

# ---- KPI row ---------------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
k1.metric("Volt‑of‑Vibes (Vv)",      f"{latest.vv:0.2f}")
k2.metric("ΔJ Net Thrust (Jc)",      f"{latest.deltaJ:+.1f}")
k3.metric("Ωo Overwhelm (Ax·Jc⁻¹)", f"{latest.ohm:0.2f}")
k4.metric("Ξσ Focus Entropy (Jc)",  f"{latest.sigma:0.2f}" if latest.sigma==latest.sigma else "—")

st.caption(
    "_Unit definitions: 1 Jc raises dopamine 5 µmol·60 s⁻¹ in the D‑70 brain phantom. "
    "1 Ax raises salivary cortisol 10 nmol L⁻¹ plus +1 BPM for same phantom._"
)

# ---- Charts ---------------------------------------------------------------
line_base = alt.Chart(df).encode(x="date:T")

juice_line = line_base.mark_line(point=True, color="#0B5FFF").encode(y="juice:Q")
anx_line   = line_base.mark_line(point=True, color="#FF5E5B").encode(y="anxiety:Q")
st.altair_chart((juice_line + anx_line).properties(height=250), use_container_width=True)

vv_line = line_base.mark_line(point=True, color="#00A693").encode(y="vv:Q")
st.altair_chart(vv_line.properties(height=200, title="Volt‑of‑Vibes"), use_container_width=True)

bar = line_base.mark_bar().encode(
    y="dvdt:Q",
    color=alt.condition("datum.dvdt > 0", alt.value("#22B8CF"), alt.value("#FF5E5B"))
)
st.altair_chart(bar.properties(height=150, title="d Vv / d t  (per day)"), use_container_width=True)

# ---- Raw table (optional) --------------------------------------------------
with st.expander("Raw data"):
    st.dataframe(df_raw, use_container_width=True)
