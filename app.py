import streamlit as st
from modules.report import build_deck
from modules.storage import load_log, DATA_DIR
from modules.metrics import compute
from modules.units import UNIT_DEFS
from modules.ui import sidebar, kpi, charts, heatmap

st.set_page_config(page_title="Demby Analytics™", layout="wide")

# ----------  responsive CSS  ----------
st.markdown("""
<style>
/* Base font scaling and mobile optimizations */
html { 
    font-size: 14px;
    -webkit-text-size-adjust: 100%;  /* Prevent font scaling in landscape */
}
@media (max-width: 480px) { 
    html { font-size: 16px }
    /* Improve touch targets */
    button, [role="button"] { min-height: 44px; }
    /* Better mobile spacing */
    .stMarkdown { padding: 0.5rem 0; }
    .stButton button { width: 100%; }
}

/* Hide sidebar on narrow screens with backdrop */
@media (max-width: 600px) {
    section[data-testid="stSidebar"] {
        transform: translateX(-330px);
        transition: transform .3s ease;
        z-index: 999;
    }
    body.show-sidebar section[data-testid="stSidebar"] {
        transform: translateX(0);
    }
    /* Add backdrop when sidebar is open */
    body.show-sidebar::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        z-index: 998;
    }
    /* Hide Streamlit's default menu */
    #MainMenu { display: none }
    /* Improve mobile header */
    header[data-testid="stHeader"] { 
        padding: 0.5rem 1rem;
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(10px);
    }
}

/* KPI row responsive with better spacing */
.kpi-row { 
    display: flex; 
    gap: 1rem;
    margin: 1rem 0;
}
@media (max-width: 600px) { 
    .kpi-row { 
        flex-direction: column;
        gap: 0.5rem;
    }
    /* Improve metric cards on mobile */
    .kpi-row .stMetric {
        padding: 0.5rem;
        border-radius: 8px;
        background: #f8f9fa;
    }
}

/* Chart improvements */
.vega-embed { 
    min-height: 240px !important;
}
/* Better touch interactions */
.vega-embed .marks text {
    font-size: 14px !important;
}
@media (max-width: 600px) {
    .vega-embed .marks text {
        font-size: 16px !important;
    }
    /* Improve tooltip visibility on mobile */
    .vega-tooltip {
        font-size: 14px !important;
        padding: 8px !important;
        max-width: 200px !important;
    }
}

/* Mobile-optimized title */
@media (max-width: 600px) {
    h1 {
        font-size: 1.5rem !important;
        margin: 0.5rem 0 !important;
        padding: 0 1rem !important;
    }
}

/* Improve table responsiveness */
.stDataFrame {
    width: 100% !important;
    overflow-x: auto !important;
}
.stDataFrame table {
    min-width: 100% !important;
}

/* Better mobile download button */
@media (max-width: 600px) {
    .stDownloadButton {
        position: sticky;
        bottom: 1rem;
        z-index: 100;
        padding: 0 1rem;
    }
    .stDownloadButton button {
        width: 100%;
        margin: 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
}
</style>
""", unsafe_allow_html=True)

# Add hamburger menu button with improved mobile styling
st.components.v1.html("""
<script>
const btn = document.createElement('button');
btn.innerText = '☰';
btn.style.cssText = `
    position: fixed;
    top: 1rem;
    left: 1rem;
    z-index: 1000;
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 0.75rem;
    cursor: pointer;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    font-size: 1.2rem;
    line-height: 1;
    transition: all 0.2s ease;
`;
btn.onclick = () => {
    document.body.classList.toggle('show-sidebar');
    // Close sidebar when clicking backdrop
    document.body.addEventListener('click', function closeSidebar(e) {
        if (e.target === document.body) {
            document.body.classList.remove('show-sidebar');
            document.body.removeEventListener('click', closeSidebar);
        }
    });
};
if (document.body) {
    document.body.appendChild(btn);
}
// Close sidebar on window resize if open
window.addEventListener('resize', () => {
    if (window.innerWidth > 600) {
        document.body.classList.remove('show-sidebar');
    }
});
</script>
""", height=0)

# ----------  title  ----------
st.markdown(
    "<h1 style='text-align:center; margin:0; padding:1rem;'>"
    "Demby&nbsp;Analytics™<br>"
    "<span style='font-size:0.8em; font-weight:normal;'>"
    "Psychic&nbsp;Physics&nbsp;Dashboard"
    "</span></h1>",
    unsafe_allow_html=True,
)
# --------------------------------

if "nickname" not in st.session_state:
    st.info("Viewing demo data. Choose a nickname in the sidebar to start your own log!")
else:
    st.caption(f"Your data file: {DATA_DIR / (st.session_state.nickname + '.csv')}")


df_raw = load_log()
sidebar.draw(df_raw)           # sidebar first (may rerun)

df = compute(df_raw)

if df.empty:
    st.warning("No data yet. Use the sidebar to log your first entry.")
    st.stop()

latest = df.iloc[-1]
kpi.draw(df, latest)
st.caption(UNIT_DEFS)

chart_path = charts.draw(df)   # main charts
heatmap.draw(df)               # calendar view

# after all charts rendered
pptx_file  = build_deck(df, {"juice_anx": chart_path})

with open(pptx_file, "rb") as f:
    st.download_button(
        "Download Board Deck",
        data=f,
        file_name=pptx_file.name,
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )
