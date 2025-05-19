import streamlit as st
from modules.storage import append_entry

def draw(df_raw):
    """Render sidebar sliders, return nothing."""
    st.sidebar.header("Daily Log  📈")

    last_j  = int(df_raw.juice.iloc[-1])   if not df_raw.empty else 5
    last_a  = int(df_raw.anxiety.iloc[-1]) if not df_raw.empty else 5

    juice = st.sidebar.slider("Juice (0‑10)", 0, 10, value=last_j)
    anxiety = st.sidebar.slider("Anxiety (0‑10)", 0, 10, value=last_a)

    if st.sidebar.button("Save today"):
        append_entry(int(juice), int(anxiety))
        st.sidebar.success("Entry saved!")
        st.rerun()     # Streamlit ≥1.28
