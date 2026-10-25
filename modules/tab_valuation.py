"""
tab_valuation.py — Tab 3: Project Planning & Real Estate Valuation (Epic 3)
"""
import math
import urllib.parse
import streamlit as st
import requests
from io import BytesIO
from PIL import Image


# ─── Rates & Multipliers ───────────────────────────────────────────────────────

STRUCTURE_RATES = {
    "Residential Apartment":  {"base_inr_sqft": 1800, "steel_kg_sqft": 4.5, "cement_bags_sqft": 0.45},
    "Commercial Office":      {"base_inr_sqft": 2400, "steel_kg_sqft": 5.2, "cement_bags_sqft": 0.55},
    "Industrial Warehouse":   {"base_inr_sqft": 1200, "steel_kg_sqft": 3.8, "cement_bags_sqft": 0.35},
    "Luxury Villa":           {"base_inr_sqft": 3200, "steel_kg_sqft": 5.8, "cement_bags_sqft": 0.60},
    "Mixed-Use Development":  {"base_inr_sqft": 2100, "steel_kg_sqft": 5.0, "cement_bags_sqft": 0.50},
    "IT/Tech Park":           {"base_inr_sqft": 2800, "steel_kg_sqft": 5.5, "cement_bags_sqft": 0.58},
    "Hospital/Healthcare":    {"base_inr_sqft": 3500, "steel_kg_sqft": 6.0, "cement_bags_sqft": 0.65},
}

TIER_MULTIPLIERS = {
    "Tier 1 — Metro (Mumbai, Delhi, Bengaluru, Chennai, Hyderabad, Kolkata)": 1.35,
    "Tier 2 — Large Cities (Pune, Ahmedabad, Jaipur, Lucknow, Chandigarh)":   1.10,
    "Tier 3 — Smaller Cities & Towns":                                         0.85,
}

MARKET_PREMIUM = {
    "Tier 1 — Metro (Mumbai, Delhi, Bengaluru, Chennai, Hyderabad, Kolkata)": 1.65,
    "Tier 2 — Large Cities (Pune, Ahmedabad, Jaipur, Lucknow, Chandigarh)":   1.30,
    "Tier 3 — Smaller Cities & Towns":                                         1.10,
}

MILESTONES = [
    (10,  "Foundation Complete"),
    (25,  "Basement / Plinth Level"),
    (45,  "Structural Framing"),
    (60,  "Slab & Roofing"),
    (75,  "MEP & Façade Work"),
    (90,  "Finishing & Interiors"),
    (100, "Project Handover"),
]

STYLES = ["Modern Indian", "Contemporary", "Colonial Revival", "Minimalist", "Smart Green Building"]


def _format_inr(value_lakhs: float) -> str:
    if value_lakhs >= 100:
        return f"₹ {value_lakhs/100:.2f} Cr"
    return f"₹ {value_lakhs:.2f} L"


def _get_milestone(pct: int) -> str:
    for threshold, label in reversed(MILESTONES):
        if pct >= threshold:
            return label
    return "Pre-Construction"


def _fetch_pollinations_image(prompt: str, width: int = 800, height: int = 500) -> bytes | None:
    """Fetch an architectural rendering from Pollinations.ai."""
    try:
        encoded = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&nologo=true"
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            return resp.content
        return None
    except Exception:
        return None


def render_valuation_tab(client):
    """Render the Planning & Real Estate Valuation tab."""

    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <h2 style="font-size:1.4rem;font-weight:700;margin:0 0 0.3rem;">
            🏗️ Project Planning & Real Estate Valuation
        </h2>
        <p style="color:#8892A4;font-size:0.88rem;margin:0;">
            Dynamic cost estimation, capital expenditure tracking, and real estate asset valuation
            in INR — with conceptual 3D architectural rendering via Pollinations AI.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Inputs ──────────────────────────────────────────────────────────────
    with st.container():
        st.markdown("#### ⚙️ Project Parameters")
        c1, c2 = st.columns(2, gap="large")
        with c1:
            structure_type = st.selectbox(
                "Structure Type", list(STRUCTURE_RATES.keys()),
                help="Select the primary construction category", key="val_struct"
            )
            sqft = st.number_input(
                "Built-Up Area (sq ft)", min_value=500, max_value=500_000,
                value=2500, step=100, key="val_sqft"
            )
            location_tier = st.selectbox(
                "Location Tier", list(TIER_MULTIPLIERS.keys()),
                help="Indian city tier affects cost and market valuation", key="val_tier"
            )

        with c2:
            completion_pct = st.slider(
                "Completion Percentage (%)", 0, 100, 45, 5,
                help="Drag to current project completion stage", key="val_comp"
            )
            arch_style = st.selectbox("Architectural Style (for 3D render)", STYLES, key="val_style")
            project_name = st.text_input(
                "Project Name", value="Horizon Residences, Phase II",
                help="Used in report and rendering prompt", key="val_name"
            )

    calc_btn = st.button("📊 Calculate & Generate Report", key="val_calc", use_container_width=True)

    if calc_btn:
        _render_valuation_results(
            client, structure_type, sqft, location_tier,
            completion_pct, arch_style, project_name
        )


def _render_valuation_results(client, structure_type, sqft, location_tier,
                               completion_pct, arch_style, project_name):
    st.markdown("---")
    st.markdown("### 📈 Financial & Valuation Dashboard")

    rates = STRUCTURE_RATES[structure_type]
    tier_mult = TIER_MULTIPLIERS[location_tier]
    market_mult = MARKET_PREMIUM[location_tier]

    # Calculations
    base_rate_sqft = rates["base_inr_sqft"] * tier_mult
    total_budget_inr = base_rate_sqft * sqft
    capex_incurred_inr = total_budget_inr * (completion_pct / 100)
    remaining_inr = total_budget_inr - capex_incurred_inr
    market_val_inr = total_budget_inr * market_mult
    current_asset_val = market_val_inr * (completion_pct / 100)
    roi_pct = ((market_val_inr - total_budget_inr) / total_budget_inr) * 100

    # Material requirements
    steel_kg = rates["steel_kg_sqft"] * sqft
    steel_mt = steel_kg / 1000
    cement_bags = int(rates["cement_bags_sqft"] * sqft)

    # Milestone
    milestone = _get_milestone(completion_pct)

    # Convert to lakhs
    total_l = total_budget_inr / 100_000
    capex_l = capex_incurred_inr / 100_000
    remain_l = remaining_inr / 100_000
    market_l = market_val_inr / 100_000
    curr_asset_l = current_asset_val / 100_000

    # ── Financial Cards ──────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("Total Project Budget", _format_inr(total_l), "orange", f"@ ₹{base_rate_sqft:,.0f}/sqft"),
        ("CapEx Incurred", _format_inr(capex_l), "blue", f"{completion_pct}% complete"),
        ("Market Asset Value", _format_inr(market_l), "green", "On completion (estimated)"),
        ("Projected ROI", f"{roi_pct:.1f}%", "yellow" if roi_pct > 20 else "red", "Return on investment"),
    ]
    for col, (title, val, color, sub) in zip([c1, c2, c3, c4], cards):
        with col:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">{title}</div>
                <div class="card-value {color}">{val}</div>
                <div class="card-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    # ── Progress & Milestone ─────────────────────────────────────────────────
    st.markdown(f"""
    <div style="margin:1rem 0;">
        <div style="display:flex;justify-content:space-between;font-size:0.8rem;color:#8892A4;margin-bottom:0.3rem;">
            <span>🏗️ Construction Progress — <strong style="color:#E8EAF0;">{milestone}</strong></span>
            <span>{completion_pct}%</span>
        </div>
        <div class="prog-wrap" style="height:16px;">
            <div class="prog-fill" style="width:{completion_pct}%;"></div>
        </div>
        <div style="display:flex;justify-content:space-between;margin-top:0.5rem;">
            {"".join(f'<span style="font-size:0.7rem;color:{"#FF6B35" if completion_pct >= t else "#8892A4"};">{"●" if completion_pct >= t else "○"} {lbl}</span>' for t, lbl in MILESTONES)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Secondary Metrics ────────────────────────────────────────────────────
    st.markdown("#### 📦 Material Requirements & Cost Breakdown")
    m1, m2, m3, m4, m5 = st.columns(5)
    metrics = [
        ("Steel Requirement", f"{steel_mt:.1f} MT", f"{steel_kg:,.0f} kg total"),
        ("Cement Requirement", f"{cement_bags:,} Bags", f"50 kg bags (Portland)"),
        ("Remaining CapEx", _format_inr(remain_l), f"To complete {100-completion_pct}%"),
        ("Current Asset Value", _format_inr(curr_asset_l), "Work-in-progress value"),
        ("Cost per sq ft", f"₹{base_rate_sqft:,.0f}", f"All-in rate ({location_tier[:6]})"),
    ]
    for col, (label, val, sub) in zip([m1, m2, m3, m4, m5], metrics):
        with col:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">{label}</div>
                <div class="card-value" style="font-size:1.35rem;">{val}</div>
                <div class="card-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    # ── Financial Summary Table ──────────────────────────────────────────────
    with st.expander("💰 Detailed Financial Breakdown"):
        st.markdown(f"""
| Parameter | Value |
|-----------|-------|
| Project Name | {project_name} |
| Structure Type | {structure_type} |
| Built-Up Area | {sqft:,} sq ft |
| Base Construction Rate | ₹ {rates['base_inr_sqft']:,}/sqft |
| Location Multiplier | {tier_mult}× |
| Effective Rate | ₹ {base_rate_sqft:,.0f}/sqft |
| **Total Project Budget** | **{_format_inr(total_l)}** |
| **CapEx Incurred ({completion_pct}%)** | **{_format_inr(capex_l)}** |
| **Remaining Expenditure** | **{_format_inr(remain_l)}** |
| **Estimated Market Value** | **{_format_inr(market_l)}** |
| **Projected ROI** | **{roi_pct:.1f}%** |
| Steel Requirement | {steel_mt:.2f} MT ({steel_kg:,.0f} kg) |
| Cement Requirement | {cement_bags:,} bags (50 kg) |
| Current Milestone | {milestone} |
        """)

    # ── 3D Architectural Rendering ───────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 🎨 Conceptual 3D Architectural Rendering")
    st.markdown(f"""
    <p style="color:#8892A4;font-size:0.84rem;margin-bottom:1rem;">
        AI-generated conceptual visualization via <strong>Pollinations AI (Flux)</strong> —
        prompt crafted for <em>{project_name}</em>.
    </p>
    """, unsafe_allow_html=True)

    render_prompt = client.generate_render_prompt(structure_type, sqft,
                                                   location_tier.split("—")[0].strip(),
                                                   arch_style)

    with st.expander("🔤 View Rendering Prompt"):
        st.code(render_prompt, language=None)

    gen_render = st.button("🖼️ Generate Architectural Rendering", key="gen_render")

    if gen_render:
        with st.spinner("🎨 Generating 3D render via Pollinations AI (Flux)…"):
            img_bytes = _fetch_pollinations_image(render_prompt)

        if img_bytes:
            img = Image.open(BytesIO(img_bytes))
            st.image(img, caption=f"🏛️ Conceptual Rendering — {project_name}", use_column_width=True)
            st.download_button(
                "⬇️ Download Rendering",
                data=img_bytes,
                file_name=f"{project_name.replace(' ','_')}_render.jpg",
                mime="image/jpeg"
            )
        else:
            st.markdown(f"""
            <div class="render-placeholder">
                <div class="icon">🏛️</div>
                <strong>{project_name}</strong><br>
                <span>{structure_type} · {sqft:,} sq ft · {arch_style} Style</span><br><br>
                <small>Rendering service temporarily unavailable.<br>
                Copy the prompt above and paste it into Pollinations.ai or Midjourney.</small>
            </div>""", unsafe_allow_html=True)
