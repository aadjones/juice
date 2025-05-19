# modules/ui/kpi.py
import streamlit as st
from modules.palette import (
    PAL_TEAL, PAL_ORANGE,
    PAL_GREEN, PAL_YELLOW, PAL_RED
)
import pandas as pd

def draw(df, latest):
    k1, k2, k3 = st.columns(3)

    # ── 1) GQ ───────────────────────────────────────────────────────────────
    prev_gq = df.gq.iloc[-2] if len(df) > 1 else latest.gq
    delta_gq = latest.gq - prev_gq if len(df) > 1 else None
    k1.metric(
        label="GQ (Gumption Quotient)",
        value=f"{latest.gq:0.2f}",
        delta=f"{delta_gq:+0.02f}" if delta_gq is not None else "-",
        delta_color="normal",
        help="Juice / Anxiety. Creative efficiency (≥1.5 is healthy)."
    )

    # --- Φf  (Focus Flux) ------------------------------------------------------
    prev_flux = df.focus_flux.iloc[-2] if len(df) > 1 else latest.focus_flux
    delta_flux = latest.focus_flux - prev_flux if len(df) > 1 else None
    
    # Use neutral color for insufficient data
    arrow_col = "#999" if len(df) < 2 else PAL_TEAL
    arrow = "↑" if latest.focus_flux > 0 else "↓" if latest.focus_flux < 0 else ""

    k2.metric(
        label="Φf (Focus Flux)",
        value=f"{arrow}{latest.focus_flux:+.2f}" if not pd.isna(latest.focus_flux) else "0.00",
        delta=f"{delta_flux:+.2f}" if delta_flux is not None else "-",
        delta_color="normal",
        help=(
            "Momentum of motivation.\n"
            "Positive when Juice is rising **and** you still have Surplus Drive."
        )
    )

    # ── 3) Ξσ  (Focus Entropy) ─────────────────────────────────────────────
    sigma_value = latest.sigma if not pd.isna(latest.sigma) else 0
    sigma_colour = (
        PAL_GREEN  if sigma_value < 1.5 else
        PAL_YELLOW if sigma_value < 2.5 else
        PAL_RED
    )
    # Use neutral color for insufficient data
    if len(df) < 2:
        sigma_colour = "#999"
    entropy_html = f"""
    <div title="Rolling σ of Juice. Measures volatility (green < 1.5, yellow 1.5-2.5, red > 2.5)"
         style="padding:0.25rem 0.5rem;background:{sigma_colour};
                border-radius:6px;text-align:center">
        <div style="font-size:0.8rem;color:#fff">Ξσ Focus Entropy</div>
        <div style="font-size:1.4rem;font-weight:bold;color:#fff">
            {latest.sigma:0.2f}
        </div>
    </div>
    """
    k3.markdown(entropy_html, unsafe_allow_html=True)
