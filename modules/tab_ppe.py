"""
tab_ppe.py — Tab 1: Site Safety & PPE Audit (Epic 2)
"""
import json
import streamlit as st
from PIL import Image
from io import BytesIO


# ─── PPE metadata ─────────────────────────────────────────────────────────────

PPE_META = {
    "hard_hat":       {"label": "Hard Hat / Safety Helmet", "icon": "⛑️",  "standard": "IS 2925"},
    "high_vis_vest":  {"label": "High-Visibility Vest",     "icon": "🦺",  "standard": "IS 15809"},
    "steel_toe_boots":{"label": "Steel-Toe Safety Boots",   "icon": "👢",  "standard": "IS 5557"},
    "safety_harness": {"label": "Safety Harness",           "icon": "🪢",  "standard": "IS 3521"},
    "safety_gloves":  {"label": "Safety Gloves",            "icon": "🧤",  "standard": "IS 6994"},
    "eye_protection": {"label": "Eye Protection / Goggles", "icon": "🥽",  "standard": "IS 5983"},
}

SEVERITY_COLOR = {
    "Low":      "#27AE60",
    "Medium":   "#F39C12",
    "High":     "#FF6B35",
    "Critical": "#E74C3C",
}

STATUS_PILL = {
    "COMPLIANT":        ("pill-pass", "✅ COMPLIANT"),
    "NEEDS_IMPROVEMENT":("pill-warn", "⚠️ NEEDS IMPROVEMENT"),
    "NON_COMPLIANT":    ("pill-fail", "❌ NON-COMPLIANT"),
    "CRITICAL":         ("pill-crit", "🚨 CRITICAL"),
}


def _score_color(score: int) -> str:
    if score >= 80: return "green"
    if score >= 60: return "yellow"
    return "red"


def render_ppe_tab(client):
    """Render the PPE Safety Audit tab."""

    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <h2 style="font-size:1.4rem;font-weight:700;margin:0 0 0.3rem;">
            🦺 Site Safety & PPE Audit
        </h2>
        <p style="color:#8892A4;font-size:0.88rem;margin:0;">
            Upload a construction site photo for AI-powered PPE compliance analysis under
            <strong>OSHA 1926</strong> and <strong>IS 456</strong> standards.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_upload, col_preview = st.columns([1, 1], gap="large")

    with col_upload:
        uploaded = st.file_uploader(
            "Upload Site Photo",
            type=["jpg", "jpeg", "png", "webp"],
            help="JPG / PNG / WEBP — max 50 MB",
            key="ppe_upload"
        )
        demo_btn = st.checkbox("▶ Run Demo Analysis (no image required)", value=False, key="ppe_demo")

        if uploaded or demo_btn:
            analyze_btn = st.button("🔍 Run Safety Audit", key="ppe_analyze", use_container_width=True)
        else:
            analyze_btn = False
            st.markdown("""
            <div style="background:#1C2135;border-radius:10px;padding:1.25rem;margin-top:1rem;
                        border:1px dashed rgba(255,107,53,0.2);">
                <p style="color:#8892A4;font-size:0.84rem;margin:0;">
                    📌 <strong>How to use:</strong><br>
                    1. Upload a JPG/PNG of your construction site<br>
                    2. Click <em>Run Safety Audit</em><br>
                    3. View PPE compliance, hazards, and download JSON report
                </p>
            </div>""", unsafe_allow_html=True)

    with col_preview:
        if uploaded:
            img = Image.open(uploaded)
            st.image(img, caption="📸 Uploaded Site Photo", use_column_width=True)

    if analyze_btn:
        image_bytes = None
        mime = "image/jpeg"
        if uploaded:
            image_bytes = uploaded.getvalue()
            mime = uploaded.type or "image/jpeg"

        with st.spinner("🔍 Analyzing PPE compliance with Gemini AI…"):
            result = client.analyze_ppe(image_bytes)

        _render_ppe_results(result)


def _render_ppe_results(result: dict):
    st.markdown("---")
    st.markdown("### 📊 Audit Results")

    score = result.get("safety_score", 0)
    status_key = result.get("overall_status", "NON_COMPLIANT")
    pill_cls, pill_text = STATUS_PILL.get(status_key, ("pill-fail", status_key))
    sc = _score_color(score)

    # Top metrics row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Safety Score</div>
            <div class="card-value {sc}">{score}<span style="font-size:1rem;"> /100</span></div>
            <div class="card-sub">Overall compliance rating</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        ppe_data = result.get("ppe_detection", {})
        compliant = sum(1 for v in ppe_data.values() if v.get("compliance"))
        total = len(ppe_data)
        st.markdown(f"""
        <div class="card">
            <div class="card-title">PPE Items Compliant</div>
            <div class="card-value blue">{compliant}<span style="font-size:1rem;"> /{total}</span></div>
            <div class="card-sub">Equipment categories</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        hazards = result.get("site_hazards", [])
        critical = sum(1 for h in hazards if h.get("severity") in ("Critical", "High"))
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Critical/High Hazards</div>
            <div class="card-value {'red' if critical else 'green'}">{critical}</div>
            <div class="card-sub">Require immediate action</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Overall Status</div>
            <div style="margin-top:0.5rem;">
                <span class="pill {pill_cls}">{pill_text}</span>
            </div>
            <div class="card-sub" style="margin-top:0.5rem;">{status_key.replace("_"," ").title()}</div>
        </div>""", unsafe_allow_html=True)

    # Progress bar
    st.markdown(f"""
    <div style="margin:0.5rem 0 1.5rem;">
        <div style="display:flex;justify-content:space-between;font-size:0.78rem;color:#8892A4;margin-bottom:0.3rem;">
            <span>Compliance Progress</span><span>{score}%</span>
        </div>
        <div class="prog-wrap"><div class="prog-fill" style="width:{score}%;"></div></div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_r = st.columns([1, 1], gap="large")

    # PPE Checklist
    with col_l:
        st.markdown("#### 🛡️ PPE Compliance Checklist")
        for key, meta in PPE_META.items():
            item = ppe_data.get(key, {})
            ok = item.get("compliance", False)
            status_txt = item.get("status", "Unknown")
            workers = ""
            if item.get("workers_total", 0) > 0:
                workers = f" · {item['workers_compliant']}/{item['workers_total']} workers"
            row_cls = "ok" if ok else ("na" if status_txt in ("Not Required", "Not Verified") else "fail")
            icon = "✅" if ok else ("⚪" if row_cls == "na" else "❌")
            color = "#27AE60" if ok else ("#8892A4" if row_cls == "na" else "#E74C3C")
            st.markdown(f"""
            <div class="ppe-row {row_cls}">
                <span class="ppe-label">{meta['icon']} {meta['label']}</span>
                <span class="ppe-status" style="color:{color};">{icon} {status_txt}{workers}</span>
            </div>""", unsafe_allow_html=True)

    # Hazards
    with col_r:
        st.markdown("#### ⚠️ Identified Site Hazards")
        if not hazards:
            st.success("✅ No significant hazards identified.")
        for h in hazards:
            sev = h.get("severity", "Low")
            bc = SEVERITY_COLOR.get(sev, "#8892A4")
            st.markdown(f"""
            <div class="hazard-card {sev}">
                <div class="hazard-title">
                    {h.get('hazard','Unknown Hazard')}
                    <span style="font-size:0.75rem;font-weight:600;color:{bc};
                                 background:rgba(0,0,0,0.3);padding:0.15rem 0.5rem;
                                 border-radius:4px;margin-left:0.5rem;">{sev}</span>
                </div>
                <div style="font-size:0.82rem;color:#C0C4D0;margin-top:0.2rem;">
                    {h.get('description','')}
                </div>
                <div class="hazard-remedy">
                    🔧 <strong>Remedy:</strong> {h.get('remedy','')}
                </div>
            </div>""", unsafe_allow_html=True)

    # Standards & Summary
    st.markdown("---")
    with st.expander("📋 Standards Referenced & Audit Summary"):
        osha = result.get("osha_standards_referenced", [])
        is_std = result.get("is_standards_referenced", [])
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**OSHA Standards:**")
            for s in osha:
                st.markdown(f"- `{s}`")
        with col2:
            st.markdown("**IS Standards (BIS):**")
            for s in is_std:
                st.markdown(f"- `{s}`")
        summary = result.get("audit_summary", "")
        if summary:
            st.info(f"📝 **Summary:** {summary}")

    # Download
    st.download_button(
        label="⬇️ Download Audit Report (JSON)",
        data=json.dumps(result, indent=2),
        file_name="ppe_audit_report.json",
        mime="application/json",
        use_container_width=True
    )
