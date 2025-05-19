# modules/ui/kpi.py
import streamlit as st
from modules.palette import (
    PAL_TEAL, PAL_ORANGE,
    PAL_GREEN, PAL_YELLOW, PAL_RED
)

def draw(df, latest):
    k1, k2, k3 = st.columns(3)

    # ── 1) GQ ───────────────────────────────────────────────────────────────
    prev_gq = df.gq.iloc[-2] if len(df) > 1 else latest.gq
    k1.metric(
        label="GQ (Gumption Quotient)",
        value=f"{latest.gq:0.2f}",
        delta=f"{latest.gq - prev_gq:+0.02f}",
        delta_color="normal",
        help="Juice / Anxiety. Creative efficiency (≥1.5 is healthy)."
    )

    # --- Φf  (Focus Flux) ------------------------------------------------------
    prev_flux = df.focus_flux.iloc[-2] if len(df) > 1 else latest.focus_flux

    k2.metric(
        label="Φf (Focus Flux)",
        value=f"{latest.focus_flux:+.2f}",      # <-- no arrow glyph
        delta=f"{latest.focus_flux - prev_flux:+.2f}",
        delta_color="normal",                  # green if ↑, red if ↓
        help=(
            "Momentum of motivation.\n"
            "Positive when Juice is rising **and** you still have Surplus Drive."
        )
    )

    # ── 3) Ξσ  (Focus Entropy) ─────────────────────────────────────────────
    sigma_colour = (
        PAL_GREEN  if latest.sigma < 1.5 else
        PAL_YELLOW if latest.sigma < 2.5 else
        PAL_RED
    )
    entropy_html = f"""
    <div title="Rolling σ of Juice. Measures volatility (green < 1.5, yellow 1.5‑2.5, red > 2.5)"
         style="padding:0.25rem 0.5rem;background:{sigma_colour};
                border-radius:6px;text-align:center">
        <div style="font-size:0.8rem;color:#fff">Ξσ Focus Entropy</div>
        <div style="font-size:1.4rem;font-weight:bold;color:#fff">
            {latest.sigma:0.2f}
        </div>
    </div>
    """
    k3.markdown(entropy_html, unsafe_allow_html=True)
