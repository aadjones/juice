# app.py
import streamlit as st
import altair as alt
from modules.storage import load_log, append_entry
from modules.metrics import compute

st.set_page_config(
    page_title="Aaron Analytics™ — Psychic KPI Dashboard",
    layout="wide",
)
# ---- Load + compute --------------------------------------------------------
df_raw = load_log()
df     = compute(df_raw)

# ---- Sidebar input ---------------------------------------------------------
from datetime import date

st.sidebar.header("Daily Log  📈")

# fetch previous values (or mid‑scale defaults on first run)
if "last_juice" not in st.session_state:
    if not df_raw.empty:
        st.session_state.last_juice   = int(df_raw.juice.iloc[-1])
        st.session_state.last_anxiety = int(df_raw.anxiety.iloc[-1])
    else:
        st.session_state.last_juice   = 5
        st.session_state.last_anxiety = 5

juice = st.sidebar.slider(
    "Juice (0 - 10)",
    0, 10,
    value=st.session_state.last_juice,
    key="juice",
)

anxiety = st.sidebar.slider(
    "Anxiety (0 - 10)",
    0, 10,
    value=st.session_state.last_anxiety,
    key="anxiety",
)

if st.sidebar.button("Save today"):
    append_entry(int(juice), int(anxiety))
    st.session_state.last_juice   = int(juice)
    st.session_state.last_anxiety = int(anxiety)
    st.sidebar.success(f"Entry saved for {date.today().isoformat()}  ✅")
    st.rerun()

st.title("Aaron Analytics™ — Psychic Physics Dashboard")

if df.empty:
    st.warning("No data yet. Use the sidebar to log your first entry.")
    st.stop()

latest = df.iloc[-1]

# ---- KPI row ---------------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
k1.metric("Gumption Quotient (GQ)",      f"{latest.gq:0.2f}")
k2.metric("ΔJ Net Thrust (Jc)",      f"{latest.deltaJ:+.1f}")
k3.metric("Ωo Overwhelm (Ax·Jc⁻¹)", f"{latest.ohm:0.2f}")
k4.metric("Ξσ Focus Entropy (Jc)",  f"{latest.sigma:0.2f}" if latest.sigma==latest.sigma else "—")

st.caption(
    "Unit definitions: 1 Jc raises dopamine 5 µmol·60 s⁻¹ in the D-70 brain phantom."
    "1 Ax raises salivary cortisol 10 nmol L⁻¹ plus +1 BPM for same phantom."
)

# ---- Charts ---------------------------------------------------------------
line_base = alt.Chart(df).encode(x="date:T")

juice_line = line_base.mark_line(point=True, color="#0B5FFF").encode(y="juice:Q")
anx_line   = line_base.mark_line(point=True, color="#FF5E5B").encode(y="anxiety:Q")
st.altair_chart((juice_line + anx_line).properties(height=250), use_container_width=True)

gq_line = line_base.mark_line(point=True, color="#00A693").encode(y="gq:Q")
st.altair_chart(gq_line.properties(height=200, title="Gumption Quotient"), use_container_width=True)

# --- dGQ/dt PANEL ----------------------------------------------------------

bar_raw = line_base.mark_bar(size=6).encode(
    y=alt.Y("dgqdt:Q", title="d GQ / d t  (per day)"),
    color=alt.condition("datum.dgqdt > 0",
                        alt.value("#22B8CF"),  # teal for up
                        alt.value("#FF5E5B"))  # red for down
)

line_avg = line_base.mark_line(color="black", strokeDash=[4,2]).encode(
    y="dgqdt_7d:Q"
)

st.altair_chart(
    (bar_raw + line_avg)
      .properties(height=250, title="Daily & 7‑day avg change in GQ"),
    use_container_width=True
)

# ---- Raw table (optional) --------------------------------------------------
with st.expander("Raw data"):
    st.dataframe(df_raw, use_container_width=True)
