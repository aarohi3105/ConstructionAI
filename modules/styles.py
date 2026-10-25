"""
styles.py — Global CSS injection for the Multimodal Construction Intelligence Platform.
"""

GLOBAL_CSS = """
<style>
/* ─── Google Font Import ─────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ─── CSS Variables ─────────────────────────────────────────── */
:root {
    --orange:   #FF6B35;
    --orange-l: #FF8C5A;
    --blue:     #4A90D9;
    --blue-l:   #6BAAE8;
    --green:    #27AE60;
    --green-l:  #2ECC71;
    --red:      #E74C3C;
    --yellow:   #F39C12;
    --purple:   #8E44AD;
    --bg:       #0D0F1A;
    --bg2:      #141728;
    --bg3:      #1C2135;
    --border:   rgba(255,107,53,0.25);
    --text:     #E8EAF0;
    --text-dim: #8892A4;
    --radius:   12px;
    --shadow:   0 8px 32px rgba(0,0,0,0.4);
    --glow:     0 0 20px rgba(255,107,53,0.15);
}

/* ─── Base Overrides ─────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ─── Main Container ─────────────────────────────────────────── */
.block-container {
    padding: 1.5rem 2rem !important;
    max-width: 1400px !important;
}

/* ─── Platform Header ─────────────────────────────────────────── */
.platform-header {
    background: linear-gradient(135deg, #1C2135 0%, #141728 50%, #0D0F1A 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.platform-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--orange), var(--blue), var(--orange));
    animation: shimmer 3s infinite;
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position: 200% center; }
}
.platform-header h1 {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--orange), var(--orange-l));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.25rem 0;
}
.platform-header p {
    color: var(--text-dim);
    font-size: 0.9rem;
    margin: 0;
}
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(255,107,53,0.12);
    border: 1px solid rgba(255,107,53,0.3);
    color: var(--orange);
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-right: 0.5rem;
}

/* ─── Cards ─────────────────────────────────────────────────── */
.card {
    background: var(--bg2);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow);
    transition: border-color 0.25s, box-shadow 0.25s;
}
.card:hover { border-color: var(--border); box-shadow: var(--glow); }
.card-title {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.35rem;
}
.card-value {
    font-size: 2rem;
    font-weight: 800;
    color: var(--text);
    line-height: 1.1;
}
.card-value.orange { color: var(--orange); }
.card-value.green  { color: var(--green-l); }
.card-value.red    { color: var(--red); }
.card-value.blue   { color: var(--blue-l); }
.card-value.yellow { color: var(--yellow); }
.card-sub {
    font-size: 0.78rem;
    color: var(--text-dim);
    margin-top: 0.2rem;
}

/* ─── Status Pill ─────────────────────────────────────────── */
.pill {
    display: inline-block;
    padding: 0.3rem 1rem;
    border-radius: 50px;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.pill-pass    { background: rgba(39,174,96,0.15); border: 1px solid #27AE60; color: #2ECC71; }
.pill-warn    { background: rgba(243,156,18,0.15); border: 1px solid #F39C12; color: #F39C12; }
.pill-fail    { background: rgba(231,76,60,0.15);  border: 1px solid #E74C3C; color: #E74C3C; }
.pill-crit    { background: rgba(142,68,173,0.15); border: 1px solid #8E44AD; color: #CF9FFF; }
.pill-info    { background: rgba(74,144,217,0.15); border: 1px solid #4A90D9; color: #6BAAE8; }

/* ─── Hazard / PPE Row ────────────────────────────────────── */
.ppe-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.6rem 1rem;
    border-radius: 8px;
    margin-bottom: 0.4rem;
    background: var(--bg3);
    border-left: 3px solid transparent;
    transition: 0.2s;
}
.ppe-row.ok   { border-left-color: var(--green); }
.ppe-row.fail { border-left-color: var(--red); }
.ppe-row.na   { border-left-color: var(--text-dim); }
.ppe-label { font-weight: 500; font-size: 0.88rem; }
.ppe-status { font-size: 0.78rem; font-weight: 600; }

/* ─── Hazard card ────────────────────────────────────────── */
.hazard-card {
    background: var(--bg3);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    border-left: 4px solid var(--red);
}
.hazard-card.Low      { border-left-color: var(--green); }
.hazard-card.Medium   { border-left-color: var(--yellow); }
.hazard-card.High     { border-left-color: var(--orange); }
.hazard-card.Critical { border-left-color: var(--red); }
.hazard-title { font-weight: 700; font-size: 0.92rem; margin-bottom: 0.2rem; }
.hazard-remedy { font-size: 0.82rem; color: var(--text-dim); margin-top: 0.3rem; }

/* ─── Crack / Defect card ────────────────────────────────── */
.defect-card {
    background: var(--bg3);
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.75rem;
    border-top: 3px solid var(--orange);
}
.defect-type { font-size: 1.15rem; font-weight: 700; color: var(--orange); }
.defect-meta { font-size: 0.82rem; color: var(--text-dim); margin-top: 0.15rem; }
.defect-section-title {
    font-size: 0.7rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: var(--text-dim); margin: 0.6rem 0 0.2rem;
}
.defect-item { font-size: 0.85rem; padding: 0.2rem 0; }

/* ─── Progress Bar ───────────────────────────────────────── */
.prog-wrap { background: var(--bg3); border-radius: 50px; height: 12px; overflow: hidden; margin: 0.5rem 0; }
.prog-fill  {
    height: 100%;
    border-radius: 50px;
    background: linear-gradient(90deg, var(--orange), var(--orange-l));
    transition: width 0.6s cubic-bezier(0.25, 0.8, 0.25, 1);
}

/* ─── Chatbot ─────────────────────────────────────────────── */
.chat-msg {
    display: flex;
    gap: 0.75rem;
    margin-bottom: 1rem;
    animation: fadeUp 0.3s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.chat-avatar {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; flex-shrink: 0;
}
.chat-avatar.user { background: rgba(255,107,53,0.2); border: 1px solid var(--orange); }
.chat-avatar.bot  { background: rgba(74,144,217,0.2); border: 1px solid var(--blue); }
.chat-bubble {
    background: var(--bg3);
    border-radius: 12px;
    padding: 0.75rem 1rem;
    max-width: 85%;
    font-size: 0.88rem;
    line-height: 1.55;
    border: 1px solid rgba(255,255,255,0.05);
}
.chat-bubble.user { background: rgba(255,107,53,0.08); border-color: rgba(255,107,53,0.2); }

/* ─── Weather Alert Card ──────────────────────────────────── */
.weather-card {
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid rgba(255,255,255,0.08);
}
.weather-card.wind   { background: linear-gradient(135deg, #1a2744 0%, #141728 100%); border-color: #4A90D9; }
.weather-card.rain   { background: linear-gradient(135deg, #142233 0%, #141728 100%); border-color: #2E86AB; }
.weather-card.heat   { background: linear-gradient(135deg, #2d1a0e 0%, #141728 100%); border-color: #E67E22; }
.weather-card.normal { background: linear-gradient(135deg, #142d1a 0%, #141728 100%); border-color: #27AE60; }
.weather-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
.weather-title { font-size: 1.2rem; font-weight: 700; margin-bottom: 0.75rem; }

/* ─── Alert boxes ─────────────────────────────────────────── */
.alert-item {
    display: flex; gap: 0.6rem; align-items: flex-start;
    padding: 0.6rem 0.8rem;
    border-radius: 8px;
    margin-bottom: 0.4rem;
    font-size: 0.85rem;
    background: var(--bg3);
}
.alert-item.critical { border-left: 3px solid var(--red); }
.alert-item.warning  { border-left: 3px solid var(--yellow); }
.alert-item.info     { border-left: 3px solid var(--blue); }
.alert-icon { font-size: 1rem; flex-shrink: 0; }

/* ─── Sidebar ─────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--orange) !important;
    font-size: 0.9rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* ─── Tabs ─────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg2) !important;
    border-radius: var(--radius) !important;
    padding: 0.25rem !important;
    gap: 0.15rem !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-dim) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--orange), #d9512a) !important;
    color: white !important;
}

/* ─── Buttons ─────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--orange), #d9512a) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.25s !important;
    box-shadow: 0 4px 15px rgba(255,107,53,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(255,107,53,0.4) !important;
}

/* ─── Inputs ─────────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--bg3) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 2px rgba(255,107,53,0.2) !important;
}

/* ─── Selectbox ───────────────────────────────────────────── */
.stSelectbox > div > div {
    background: var(--bg3) !important;
    border-color: rgba(255,255,255,0.1) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

/* ─── File Uploader ───────────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: var(--bg3) !important;
    border: 2px dashed rgba(255,107,53,0.3) !important;
    border-radius: 12px !important;
    transition: border-color 0.25s !important;
}
[data-testid="stFileUploader"]:hover { border-color: var(--orange) !important; }

/* ─── Metric override ─────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--bg2) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: var(--radius) !important;
    padding: 1rem !important;
}

/* ─── Divider ─────────────────────────────────────────────── */
hr { border-color: rgba(255,255,255,0.07) !important; }

/* ─── Expander ────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: var(--bg2) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: var(--radius) !important;
}

/* ─── Scrollbar ───────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: rgba(255,107,53,0.4); border-radius: 3px; }

/* ─── Rendering placeholder ───────────────────────────────── */
.render-placeholder {
    background: linear-gradient(135deg, var(--bg3), var(--bg2));
    border: 2px dashed rgba(255,107,53,0.3);
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    color: var(--text-dim);
    font-size: 0.9rem;
}
.render-placeholder .icon { font-size: 3rem; margin-bottom: 0.75rem; }

/* ─── Architecture diagram ───────────────────────────────── */
.arch-item {
    display: flex; gap: 0.75rem; align-items: flex-start;
    padding: 0.6rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.83rem;
}
.arch-item:last-child { border-bottom: none; }
.arch-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--orange); flex-shrink: 0; margin-top: 5px;
}
</style>
"""

def inject_css():
    """Inject global CSS into the Streamlit app."""
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
