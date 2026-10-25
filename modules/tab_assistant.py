"""
tab_assistant.py — Tab 4: Daily Site Assistant & Weather-Aware Advisory (Epic 5)
"""
import streamlit as st


# ─── Weather Protocols ────────────────────────────────────────────────────────

WEATHER_PROFILES = {
    "☀️ Normal / Clear": {
        "class": "normal",
        "icon": "☀️",
        "color": "#27AE60",
        "title": "Normal Operations",
        "description": "Standard site protocols are in effect. All operations may proceed with routine safety checks.",
        "alerts": [
            ("info", "ℹ️", "Conduct standard pre-shift safety briefing for all workers."),
            ("info", "ℹ️", "Verify all PPE is in place before commencing ground operations."),
            ("info", "ℹ️", "Ensure potable water supply and first-aid kits are accessible."),
            ("warning", "⚠️", "Monitor UV index — apply sunscreen and enforce scheduled water breaks."),
        ],
        "protocols": [
            "✅ All structural work, concrete pouring, and masonry may proceed.",
            "✅ Crane operations permitted within rated wind speed limits.",
            "✅ Excavation and piling operations normal.",
            "✅ Electrical installations may proceed as scheduled.",
            "✅ All personnel on site — maintain standard 1:25 supervisor ratio.",
        ],
        "concrete_note": "Standard curing protocol (IS 456). Maintain moist curing for minimum 7 days.",
    },
    "🌧️ Heavy Rain": {
        "class": "rain",
        "icon": "🌧️",
        "color": "#2E86AB",
        "title": "Heavy Rain Protocol",
        "description": "Significant rainfall detected. Implement flood prevention, slope stability, and electrical safety measures immediately.",
        "alerts": [
            ("critical", "🚨", "SUSPEND all electrical work and welding operations immediately."),
            ("critical", "🚨", "Halt excavation in soft/expansive soils — risk of collapse."),
            ("warning",  "⚠️", "Secure scaffolding and all loose materials against wind-driven rain."),
            ("warning",  "⚠️", "Install temporary dewatering pumps in excavation pits."),
            ("warning",  "⚠️", "Inspect slopes and embankments for signs of saturation."),
            ("info",     "ℹ️", "Redirect workers to covered areas; maintain headcount logs."),
        ],
        "protocols": [
            "🔴 STOP: All open electrical installations and HV cable laying.",
            "🔴 STOP: Concrete pouring if rain exceeds 2 mm/hr (IS 456 Cl. 13.4).",
            "🟡 MONITOR: Slope stability using piezometers if installed.",
            "🟡 MONITOR: Water ingress into basements and sub-structure zones.",
            "🟢 CONTINUE: Covered formwork, shuttering, and reinforcement works.",
            "🟢 CONTINUE: Indoor finishing works (tiles, plaster, interiors).",
        ],
        "concrete_note": "⛔ Do NOT pour concrete during active rainfall. If pour is in progress, erect poly-sheeting tents. Maintain w/c ratio strictly.",
    },
    "💨 High Wind (>40 km/h)": {
        "class": "wind",
        "icon": "💨",
        "color": "#4A90D9",
        "title": "High Wind Advisory",
        "description": "Wind speeds exceeding safe operational thresholds. Crane and elevated work restrictions apply.",
        "alerts": [
            ("critical", "🚨", "GROUND ALL CRANES immediately — wind exceeds IS 875 operational limits."),
            ("critical", "🚨", "Evacuate workers from scaffolding above 10 m elevation."),
            ("warning",  "⚠️", "Secure or remove all loose materials, form panels, and debris."),
            ("warning",  "⚠️", "Check anchorage of construction hoists and material lifts."),
            ("warning",  "⚠️", "Increase fall protection inspection frequency."),
            ("info",     "ℹ️", "Monitor wind speed with anemometer every 30 minutes."),
        ],
        "protocols": [
            "🔴 STOP: Crane lifts and suspended load operations.",
            "🔴 STOP: Tower crane slewing and telescoping operations.",
            "🔴 STOP: Roof slab pours at height — formwork integrity compromised.",
            "🟡 RESTRICT: Scaffolding work to max 6 m height.",
            "🟡 RESTRICT: Use taglines on all suspended loads.",
            "🟢 CONTINUE: Sub-structure, ground-level, and indoor works.",
        ],
        "concrete_note": "High wind accelerates surface evaporation. Use evaporation retarder spray; cover freshly poured slabs with wet burlap.",
    },
    "🌡️ Extreme Heat (>40°C)": {
        "class": "heat",
        "icon": "🌡️",
        "color": "#E67E22",
        "title": "Extreme Heat Protocol",
        "description": "Ambient temperature exceeds 40°C. Heat stress prevention and concrete curing modifications mandatory.",
        "alerts": [
            ("critical", "🚨", "IMPLEMENT Heat Illness Prevention Plan — mandatory water every 20 mins."),
            ("critical", "🚨", "Restrict heavy physical labour between 12:00–15:00 (peak heat)."),
            ("warning",  "⚠️", "Pre-cool aggregates and mix water with ice — target concrete temp < 32°C."),
            ("warning",  "⚠️", "Deploy shade structures and misting fans on all active work fronts."),
            ("warning",  "⚠️", "Monitor core body temperature of workers handling hot materials."),
            ("info",     "ℹ️", "Appoint Heat Safety Officer for each active work zone."),
        ],
        "protocols": [
            "🔴 RESTRICT: Bituminous/hot-mix paving to early morning (06:00–10:00).",
            "🔴 RESTRICT: Welding outdoors during peak heat hours.",
            "🟡 MODIFY: Reschedule concrete pours to night (20:00–04:00).",
            "🟡 MODIFY: Use ice in mixing water; target slump within 90 min of batching.",
            "🟢 CONTINUE: Air-conditioned or shaded area works.",
            "🟢 CONTINUE: Structural steel erection (early morning only).",
        ],
        "concrete_note": "IS 456 Annex A: Max concrete temp at placement = 32°C. Use fly ash (25–35%) to reduce heat of hydration. Extended moist curing mandatory.",
    },
    "⛈️ Storm / Cyclone Warning": {
        "class": "wind",
        "icon": "⛈️",
        "color": "#8E44AD",
        "title": "STORM EMERGENCY PROTOCOL",
        "description": "Severe storm or cyclone warning active. SITE EVACUATION required. Implement emergency securing procedures.",
        "alerts": [
            ("critical", "🚨", "MANDATORY SITE EVACUATION — all personnel to safe muster point."),
            ("critical", "🚨", "GROUND ALL equipment — shut down tower cranes in free-slew mode."),
            ("critical", "🚨", "CUT electrical power at main isolator. Disconnect temporary supplies."),
            ("critical", "🚨", "BARRICADE site perimeter — prevent unauthorized access."),
            ("warning",  "⚠️", "Conduct headcount at muster point and report to site manager."),
            ("info",     "ℹ️", "Do NOT re-enter until All-Clear issued by authorities."),
        ],
        "protocols": [
            "🔴 STOP: ALL site operations immediately.",
            "🔴 EVACUATE: All personnel — mandatory muster and roll call.",
            "🔴 SECURE: Tower crane in weathervaning (free-slew) mode.",
            "🔴 ISOLATE: All electrical supplies and generator sets.",
            "🔴 SECURE: All scaffolding, formwork, and loose materials.",
            "🟡 DOCUMENT: Take photo/video evidence of site condition pre-storm.",
        ],
        "concrete_note": "⛔ All concrete operations halted. After storm, inspect all poured elements for damage before loading.",
    },
}

# ─── Chatbot helpers ─────────────────────────────────────────────────────────

QUICK_QUESTIONS = [
    "What is the mix design for M30 concrete per IS 10262?",
    "How do I calculate the safe bearing capacity of soil?",
    "What are OSHA requirements for scaffolding at height?",
    "Explain the difference between shear wall and moment frame.",
    "How to estimate reinforcement steel for a 1000 sqft slab?",
    "What is the curing period for RCC as per IS 456?",
    "How to control dust on a construction site?",
    "Explain critical path method (CPM) for project scheduling.",
]


def render_assistant_tab(client):
    """Render the Weather Advisory + Construction Chatbot tab."""

    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <h2 style="font-size:1.4rem;font-weight:700;margin:0 0 0.3rem;">
            🌤️ Daily Site Assistant & Weather-Aware Advisory
        </h2>
        <p style="color:#8892A4;font-size:0.88rem;margin:0;">
            Real-time weather protocols with dynamic safety alerts and an interactive
            construction engineering AI assistant.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Weather Section ──────────────────────────────────────────────────────
    st.markdown("### 🌦️ Site Weather Condition")
    weather = st.selectbox(
        "Select Current Weather Condition",
        list(WEATHER_PROFILES.keys()),
        key="weather_sel"
    )

    profile = WEATHER_PROFILES[weather]
    _render_weather_card(profile)

    st.markdown("---")

    # ── Chatbot Section ──────────────────────────────────────────────────────
    st.markdown("### 🤖 Construction Engineering Assistant")
    st.markdown(f"""
    <p style="color:#8892A4;font-size:0.84rem;margin-bottom:1rem;">
        Ask anything about construction engineering, IS codes, project planning, safety,
        or materials. <span style="color:{"#FF6B35" if client.demo_mode else "#27AE60"};">
        {"⚡ Demo Mode — Connect Gemini API key for real responses" if client.demo_mode else "✅ Gemini AI Connected"}</span>
    </p>
    """, unsafe_allow_html=True)

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": (
                    "👋 Hello! I'm your **Construction Engineering AI Assistant**, powered by Google Gemini.\n\n"
                    "I can help you with:\n"
                    "- 📐 **Structural design** and IS code compliance\n"
                    "- 🏗️ **Project scheduling** and cost estimation\n"
                    "- 🧱 **Material specifications** and mix designs\n"
                    "- ⛑️ **OSHA/IS safety** requirements\n"
                    "- 🌧️ **Weather-specific** construction protocols\n\n"
                    "What would you like to know today?"
                )
            }
        ]

    # Quick questions
    st.markdown("**💡 Quick Questions:**")
    qcols = st.columns(4)
    for i, q in enumerate(QUICK_QUESTIONS):
        with qcols[i % 4]:
            if st.button(q[:40] + "…", key=f"quick_{i}", use_container_width=True):
                st.session_state.pending_message = q

    # Chat display
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            _render_chat_message(msg["role"], msg["content"])

    # Input
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Your Question",
            placeholder="Ask about concrete mix design, structural calculations, IS codes, safety protocols…",
            height=80,
            key="chat_input"
        )
        col_send, col_clear = st.columns([3, 1])
        with col_send:
            send = st.form_submit_button("💬 Send Message", use_container_width=True)
        with col_clear:
            clear = st.form_submit_button("🗑️ Clear Chat", use_container_width=True)

    # Handle pending quick-question
    if "pending_message" in st.session_state:
        pending = st.session_state.pop("pending_message")
        _process_chat(client, pending)
        st.rerun()

    if send and user_input.strip():
        _process_chat(client, user_input.strip())
        st.rerun()

    if clear:
        st.session_state.chat_history = [st.session_state.chat_history[0]]
        st.rerun()


def _process_chat(client, user_message: str):
    history = st.session_state.chat_history
    history.append({"role": "user", "content": user_message})
    # Build message list for API (exclude initial greeting)
    api_msgs = [{"role": m["role"], "content": m["content"]}
                for m in history[1:-1]]
    response = client.chat(api_msgs, user_message)
    history.append({"role": "assistant", "content": response})


def _render_chat_message(role: str, content: str):
    is_user = role == "user"
    avatar = "👤" if is_user else "🤖"
    bubble_cls = "user" if is_user else ""
    align = "flex-end" if is_user else "flex-start"
    avatar_cls = "user" if is_user else "bot"

    st.markdown(f"""
    <div class="chat-msg" style="justify-content:{align};">
        {'<div class="chat-avatar ' + avatar_cls + '">' + avatar + '</div>' if not is_user else ''}
        <div class="chat-bubble {bubble_cls}">{content.replace(chr(10), '<br>')}</div>
        {'<div class="chat-avatar ' + avatar_cls + '">' + avatar + '</div>' if is_user else ''}
    </div>
    """, unsafe_allow_html=True)


def _render_weather_card(profile: dict):
    """Render the weather advisory card with alerts and protocols."""
    card_cls = profile["class"]
    color = profile["color"]

    # Main weather card
    st.markdown(f"""
    <div class="weather-card {card_cls}">
        <div class="weather-icon">{profile['icon']}</div>
        <div class="weather-title" style="color:{color};">{profile['title']}</div>
        <p style="color:#C0C4D0;font-size:0.88rem;margin:0 0 1rem;">{profile['description']}</p>
        <strong style="font-size:0.78rem;text-transform:uppercase;letter-spacing:0.1em;color:#8892A4;">
            ⚠️ Active Alerts
        </strong>
    </div>""", unsafe_allow_html=True)

    for level, icon, text in profile["alerts"]:
        st.markdown(f"""
        <div class="alert-item {level}">
            <span class="alert-icon">{icon}</span>
            <span>{text}</span>
        </div>""", unsafe_allow_html=True)

    col_proto, col_concrete = st.columns([1, 1], gap="large")

    with col_proto:
        st.markdown(f"""
        <div class="card" style="margin-top:1rem;">
            <div class="card-title" style="margin-bottom:0.75rem;">📋 Work Authorization Matrix</div>
            {"".join(f'<div style="font-size:0.83rem;padding:0.3rem 0;border-bottom:1px solid rgba(255,255,255,0.05);">{p}</div>' for p in profile["protocols"])}
        </div>""", unsafe_allow_html=True)

    with col_concrete:
        st.markdown(f"""
        <div class="card" style="margin-top:1rem;border-left:3px solid {color};">
            <div class="card-title" style="margin-bottom:0.5rem;">🧱 Concrete Curing Advisory</div>
            <p style="font-size:0.85rem;color:#C0C4D0;margin:0;">{profile['concrete_note']}</p>
        </div>""", unsafe_allow_html=True)
