# modules/ui/kpi.py
import streamlit as st
from modules.palette import (
    PAL_TEAL, PAL_ORANGE,
    PAL_GREEN, PAL_YELLOW, PAL_RED
)
import pandas as pd

def draw(df, selected_row):
    # Add explanation subtitle for the arrows/deltas
    selected_date = selected_row.date.strftime('%Y-%m-%d')
    st.markdown(
        f"<div style='text-align: center; color: #666; font-size: 0.9rem; margin-bottom: 1rem;'>"
        f"Showing metrics for <strong>{selected_date}</strong> • "
        f"Arrows show day-over-day change from previous day"
        f"</div>", 
        unsafe_allow_html=True
    )
    
    # Wrap KPIs in responsive container
    st.markdown('<div class="kpi-row">', unsafe_allow_html=True)
    
    k1, k2, k3 = st.columns(3)

    # Find the index of the selected row to calculate deltas
    selected_idx = df[df['date'] == selected_row.date].index[0]
    
    # ── 1) GQ ───────────────────────────────────────────────────────────────
    prev_gq = df.gq.iloc[selected_idx-1] if selected_idx > 0 else selected_row.gq
    delta_gq = selected_row.gq - prev_gq if selected_idx > 0 else None
    k1.metric(
        label="GQ (Gumption Quotient)",
        value=f"{selected_row.gq:0.2f}",
        delta=f"{delta_gq:+0.02f}" if delta_gq is not None else "-",
        delta_color="normal",
        help="Juice / Anxiety. Creative efficiency (≥1.5 is healthy)."
    )

    # --- Φf  (Focus Flux) ------------------------------------------------------
    prev_flux = df.focus_flux.iloc[selected_idx-1] if selected_idx > 0 else selected_row.focus_flux
    delta_flux = selected_row.focus_flux - prev_flux if selected_idx > 0 else None
    
    # Use neutral color for insufficient data
    arrow_col = "#999" if selected_idx == 0 else PAL_TEAL
    arrow = "↑" if selected_row.focus_flux > 0 else "↓" if selected_row.focus_flux < 0 else ""

    k2.metric(
        label="Φf (Focus Flux)",
        value=f"{arrow}{selected_row.focus_flux:+.2f}" if not pd.isna(selected_row.focus_flux) else "0.00",
        delta=f"{delta_flux:+.2f}" if delta_flux is not None else "-",
        delta_color="normal",
        help=(
            "Momentum of motivation.\n"
            "Positive when Juice is rising **and** you still have Surplus Drive."
        )
    )

    # ── 3) Ξσ  (Focus Entropy) ─────────────────────────────────────────────
    sigma_value = selected_row.sigma if not pd.isna(selected_row.sigma) else 0
    sigma_colour = (
        PAL_GREEN  if sigma_value < 1.5 else
        PAL_YELLOW if sigma_value < 2.5 else
        PAL_RED
    )
    # Use neutral color for insufficient data
    if len(df) < 2:
        sigma_colour = "#999"
    entropy_html = f"""
    <div title="Rolling 4-day standard deviation of Juice. Measures volatility (green < 1.5, yellow 1.5-2.5, red > 2.5)"
         style="padding:0.25rem 0.5rem;background:{sigma_colour};
                border-radius:6px;text-align:center">
        <div style="font-size:0.8rem;color:#fff">Ξσ Focus Entropy</div>
        <div style="font-size:1.4rem;font-weight:bold;color:#fff">
            {selected_row.sigma:0.2f}
        </div>
    </div>
    """
    k3.markdown(entropy_html, unsafe_allow_html=True)
    
    # Close responsive container
    st.markdown('</div>', unsafe_allow_html=True)
