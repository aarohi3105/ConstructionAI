"""
app.py -- Multimodal Construction Intelligence Platform
Skill Wallet Capstone Project 1 | Platform ID: 6ac4c98d1dcde6d7857c1642

Production-ready Streamlit application with:
  - Tab 1: Site Safety & PPE Audit (OSHA / IS 456)
  - Tab 2: Crack Diagnostics & Structural Integrity (IS 13311 / ACI 224R)
  - Tab 3: Project Planning & Real Estate Valuation in INR
  - Tab 4: Weather-Aware Advisory + Construction AI Chatbot
"""
import streamlit as st

# --- Page Config (must be FIRST Streamlit call) -------------------------
st.set_page_config(
    page_title="Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://aistudio.google.com/app/apikey",
        "About": "Multimodal Construction Intelligence Platform — Capstone Project 1",
    }
)

# --- Module Imports -----------------------------------------------------
from modules.styles import inject_css
from modules.gemini_client import GeminiClient
from modules.tab_ppe import render_ppe_tab
from modules.tab_crack import render_crack_tab
from modules.tab_valuation import render_valuation_tab
from modules.tab_assistant import render_assistant_tab

# --- Inject CSS ---------------------------------------------------------
inject_css()


# ========================================================================
# SIDEBAR
# ========================================================================


def render_sidebar() -> GeminiClient:
    """Render sidebar and initialize GeminiClient."""

    # Read the API key from Streamlit Cloud Secrets.
    # If running locally without secrets, fall back to demo mode.
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", None)
    except Exception:
        api_key = None

    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:1rem 0 1.5rem;">
            <div style="font-size:3rem;">🏗️</div>
            <div style="font-size:1rem;font-weight:800;color:#FF6B35;margin-top:0.25rem;">
                Construction Intelligence
            </div>
            <div style="font-size:0.72rem;color:#8892A4;margin-top:0.15rem;">
                Multimodal AI Platform
            </div>
            <div style="margin-top:0.75rem;">
                <span class="badge">Gemini 1.5</span>
                <span class="badge">IS 456</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # No API key input field is shown.
        st.markdown("### 🏗️ Construction Intelligence")
        if api_key:
            st.success("AI services configured")
        else:
            st.info("Demo mode")

        st.markdown("---")

        # Architecture Overview
        st.markdown("### 🏛️ Architecture Overview")
        arch_items = [
            ("Frontend", "Streamlit + Custom CSS"),
            ("AI Engine", "Google Gemini"),
            ("Vision", "Multimodal Image Analysis"),
            ("Rendering", "Pollinations AI (Flux)"),
            ("Standards", "OSHA 1926 · IS 456 · ACI 224R"),
            ("Deployment", "Streamlit Community Cloud"),
        ]
        for label, value in arch_items:
            st.markdown(f"""
            <div class="arch-item">
                <div class="arch-dot"></div>
                <div>
                    <div style="font-size:0.75rem;font-weight:600;color:#E8EAF0;">{label}</div>
                    <div style="font-size:0.72rem;color:#8892A4;">{value}</div>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")

        # Epics Coverage
        st.markdown("### 📋 Epics Coverage")
        epics = [
            ("Epic 2", "PPE Safety & Crack Diagnostics", "🦺"),
            ("Epic 3", "Planning & Real Estate Valuation", "💰"),
            ("Epic 4", "Multimodal AI & JSON Contracts", "🧠"),
            ("Epic 5", "Chatbot & Weather Advisory", "🌤️"),
            ("Epic 6", "Interface & Deployment", "🚀"),
        ]
        for code, name, icon in epics:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:0.5rem;padding:0.4rem 0;
                        border-bottom:1px solid rgba(255,255,255,0.05);font-size:0.8rem;">
                <span>{icon}</span>
                <div>
                    <span style="color:#FF6B35;font-weight:600;font-size:0.72rem;">{code}</span>
                    <span style="color:#C0C4D0;margin-left:0.4rem;">{name}</span>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("""
        <div style="font-size:0.7rem;color:#8892A4;text-align:center;padding:0.5rem 0;">
            Platform ID: <code>6ac4c98d1dcde6d7857c1642</code><br>
            Python 3.9+ · FastAPI · React Ready<br>
            <strong style="color:#FF6B35;">Skill Wallet Capstone Project 1</strong>
        </div>
        """, unsafe_allow_html=True)

    return GeminiClient(api_key=api_key)

  


# ========================================================================
# HEADER
# ========================================================================

def render_header(client: GeminiClient):
    """Render the main platform header banner."""
    mode_badge = "🔴 Demo Mode" if client.demo_mode else "🟢 AI Connected"
    mode_color = "#F39C12" if client.demo_mode else "#27AE60"

    st.markdown(f"""
    <div class="platform-header">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;
                    flex-wrap:wrap;gap:1rem;">
            <div>
                <div style="margin-bottom:0.75rem;">
                    <span class="badge">🏗️ GenAI</span>
                    <span class="badge">Real Estate</span>
                    <span class="badge">Computer Vision</span>
                </div>
                <h1>Multimodal Construction Intelligence Platform</h1>
                <p>
                    AI-powered site safety auditing &nbsp;·&nbsp; Structural crack diagnostics
                    &nbsp;·&nbsp; Real estate valuation in INR &nbsp;·&nbsp; Weather-aware advisory
                </p>
            </div>
            <div style="text-align:right;flex-shrink:0;">
                <div style="font-size:0.75rem;color:#8892A4;margin-bottom:0.3rem;">System Status</div>
                <span style="font-size:0.85rem;font-weight:600;color:{mode_color};">{mode_badge}</span>
                <div style="font-size:0.7rem;color:#8892A4;margin-top:0.2rem;">Gemini 1.5 Flash</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ========================================================================
# MAIN
# ========================================================================

def main():
    client = render_sidebar()
    render_header(client)

    tab1, tab2, tab3, tab4 = st.tabs([
        "🦺  PPE Safety Audit",
        "🔬  Crack Diagnostics",
        "💰  Valuation & Planning",
        "🌤️  Site Assistant",
    ])

    with tab1:
        render_ppe_tab(client)

    with tab2:
        render_crack_tab(client)

    with tab3:
        render_valuation_tab(client)

    with tab4:
        render_assistant_tab(client)


if __name__ == "__main__":
    main()
