"""
tab_crack.py — Tab 2: Crack Diagnostics & Structural Integrity (Epic 2)
"""
import json
import streamlit as st
from PIL import Image


SEVERITY_COLORS = {
    "Low":      ("#27AE60", "#1a3326"),
    "Medium":   ("#F39C12", "#332b0e"),
    "High":     ("#FF6B35", "#331e12"),
    "Critical": ("#E74C3C", "#2d1010"),
}

RATING_INFO = {
    "SAFE":           ("✅", "#27AE60", "Structure is safe. No immediate action needed."),
    "MINOR_CONCERN":  ("🟡", "#F39C12", "Minor defects. Schedule routine maintenance."),
    "MODERATE_CONCERN":("🟠", "#FF6B35", "Moderate issues. Professional inspection recommended."),
    "MAJOR_CONCERN":  ("🔴", "#E74C3C", "Major structural concern. Immediate engineering review required."),
    "CRITICAL":       ("🚨", "#8E44AD", "Critical failure risk. Evacuate area and engage structural engineer NOW."),
}

DEFECT_ICONS = {
    "Hairline":               "🔍",
    "Settlement":             "⬇️",
    "Structural Shear":       "⚡",
    "Structural Shear Crack": "⚡",
    "Thermal Expansion":      "🌡️",
    "Thermal Expansion Crack":"🌡️",
    "Spalling":               "💥",
    "Corrosion-Induced":      "🔩",
    "Alkali-Silica Reaction": "⚗️",
}


def render_crack_tab(client):
    """Render the Crack Diagnostics tab."""

    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <h2 style="font-size:1.4rem;font-weight:700;margin:0 0 0.3rem;">
            🔬 Crack Diagnostics & Structural Integrity
        </h2>
        <p style="color:#8892A4;font-size:0.88rem;margin:0;">
            Upload concrete/masonry surface photos for AI-powered defect classification,
            severity scoring, and engineering repair recommendations per <strong>IS 13311</strong> / <strong>ACI 224R</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_up, col_img = st.columns([1, 1], gap="large")

    with col_up:
        uploaded = st.file_uploader(
            "Upload Surface / Crack Photo",
            type=["jpg", "jpeg", "png", "webp"],
            help="Upload close-up photos of concrete cracks or surface defects",
            key="crack_upload"
        )
        demo_btn = st.checkbox("▶ Run Demo Analysis (no image required)", value=False, key="crack_demo")

        if uploaded or demo_btn:
            analyze_btn = st.button("🔬 Analyze Structural Defects", key="crack_analyze", use_container_width=True)
        else:
            analyze_btn = False
            st.markdown("""
            <div style="background:#1C2135;border-radius:10px;padding:1.25rem;margin-top:1rem;
                        border:1px dashed rgba(255,107,53,0.2);">
                <p style="color:#8892A4;font-size:0.84rem;margin:0;">
                    📌 <strong>Supported defect types:</strong><br>
                    • Hairline Cracks (cosmetic)<br>
                    • Settlement Cracks (differential foundation movement)<br>
                    • Structural Shear Cracks (load-bearing failure)<br>
                    • Thermal Expansion Cracks<br>
                    • Spalling (surface delamination)<br>
                    • Corrosion-Induced cracking
                </p>
            </div>""", unsafe_allow_html=True)

    with col_img:
        if uploaded:
            img = Image.open(uploaded)
            st.image(img, caption="📸 Surface to Analyze", use_column_width=True)

    if analyze_btn:
        image_bytes = uploaded.getvalue() if uploaded else None
        mime = uploaded.type if uploaded else "image/jpeg"

        with st.spinner("🔬 Performing structural crack analysis…"):
            result = client.analyze_crack(image_bytes)

        _render_crack_results(result)


def _render_crack_results(result: dict):
    st.markdown("---")
    st.markdown("### 🏗️ Diagnostic Results")

    rating = result.get("overall_structural_rating", "MODERATE_CONCERN")
    icon_r, color_r, desc_r = RATING_INFO.get(rating, ("⚠️", "#FF6B35", "Assessment complete."))
    defects = result.get("defects", [])
    action_required = result.get("immediate_action_required", False)

    # Top metric row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Structural Rating</div>
            <div style="font-size:1.1rem;font-weight:700;color:{color_r};margin-top:0.35rem;">
                {icon_r} {rating.replace('_',' ')}
            </div>
            <div class="card-sub">Overall integrity status</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Defects Identified</div>
            <div class="card-value orange">{len(defects)}</div>
            <div class="card-sub">Unique defect types</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        severe = sum(1 for d in defects if d.get("severity") in ("High", "Critical"))
        st.markdown(f"""
        <div class="card">
            <div class="card-title">High/Critical Defects</div>
            <div class="card-value {'red' if severe else 'green'}">{severe}</div>
            <div class="card-sub">Require urgent repair</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        action_color = "red" if action_required else "green"
        action_txt = "YES — Act Now" if action_required else "NO — Monitor"
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Immediate Action</div>
            <div class="card-value {action_color}" style="font-size:1.2rem;">{action_txt}</div>
            <div class="card-sub">Engineering judgement</div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#1C2135;border-left:4px solid {color_r};border-radius:10px;
                padding:1rem 1.25rem;margin:1rem 0 1.5rem;font-size:0.88rem;">
        {icon_r} <strong>Assessment:</strong> {desc_r}
    </div>""", unsafe_allow_html=True)

    # Defect cards
    st.markdown("#### 🔎 Detailed Defect Analysis")

    if not defects:
        st.success("✅ No significant defects detected in this image.")
        return

    for i, defect in enumerate(defects, 1):
        dtype = defect.get("defect_type", "Unknown Defect")
        dicon = DEFECT_ICONS.get(dtype, "🔍")
        sev = defect.get("severity", "Low")
        bc, bg = SEVERITY_COLORS.get(sev, ("#8892A4", "#1C2135"))
        width = defect.get("crack_width_mm", 0)
        length = defect.get("length_estimate_m", 0)
        urgency = defect.get("urgency", "Monitor")
        location = defect.get("location", "Not specified")
        causes = defect.get("root_causes", [])
        repairs = defect.get("recommended_repairs", [])
        risk = defect.get("risk_assessment", "")

        with st.expander(f"{dicon} Defect #{i} — {dtype} | Severity: {sev}", expanded=(i == 1)):
            st.markdown(f"""
            <div class="defect-card">
                <div class="defect-type">{dicon} {dtype}</div>
                <div class="defect-meta">
                    📍 {location} &nbsp;|&nbsp;
                    📏 Width: <strong>{width} mm</strong> &nbsp;|&nbsp;
                    📐 Length: <strong>~{length} m</strong> &nbsp;|&nbsp;
                    <span style="color:{bc};font-weight:700;">{sev} Severity</span>
                </div>
            </div>""", unsafe_allow_html=True)

            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("""<div class="defect-section-title">🕵️ Root Causes</div>""", unsafe_allow_html=True)
                for cause in causes:
                    st.markdown(f"""<div class="defect-item">◦ {cause}</div>""", unsafe_allow_html=True)

                st.markdown(f"""
                <div style="margin-top:0.75rem;background:rgba(0,0,0,0.2);border-radius:8px;
                            padding:0.6rem 0.8rem;font-size:0.82rem;">
                    ⏰ <strong>Urgency:</strong>
                    <span style="color:{bc};font-weight:600;"> {urgency}</span>
                </div>""", unsafe_allow_html=True)

            with col_b:
                st.markdown("""<div class="defect-section-title">🔧 Recommended Repairs</div>""", unsafe_allow_html=True)
                for repair in repairs:
                    st.markdown(f"""<div class="defect-item">→ {repair}</div>""", unsafe_allow_html=True)

                if risk:
                    st.markdown(f"""
                    <div style="margin-top:0.75rem;background:rgba(0,0,0,0.2);border-radius:8px;
                                padding:0.6rem 0.8rem;font-size:0.82rem;color:#C0C4D0;">
                        ⚠️ <strong>Risk:</strong> {risk}
                    </div>""", unsafe_allow_html=True)

    # Summary & standards
    st.markdown("---")
    summary = result.get("summary", "")
    standard = result.get("inspection_standard", "IS 13311 / ACI 224R")
    if summary:
        st.info(f"📋 **{standard} Assessment Summary:** {summary}")

    # Download
    st.download_button(
        label="⬇️ Download Diagnostic Report (JSON)",
        data=json.dumps(result, indent=2),
        file_name="crack_diagnostic_report.json",
        mime="application/json",
        use_container_width=True
    )
