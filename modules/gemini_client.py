"""
gemini_client.py — Wrapper for Google Gemini API calls with demo-mode fallback.
"""
import json
import base64
import re
from io import BytesIO
from typing import Optional

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


# ─── Demo Payloads ────────────────────────────────────────────────────────────

DEMO_PPE_RESULT = {
    "safety_score": 62,
    "overall_status": "NEEDS_IMPROVEMENT",
    "ppe_detection": {
        "hard_hat": {"status": "Detected", "compliance": True,  "workers_compliant": 4, "workers_total": 5},
        "high_vis_vest": {"status": "Partial",  "compliance": False, "workers_compliant": 3, "workers_total": 5},
        "steel_toe_boots": {"status": "Not Verified", "compliance": False, "workers_compliant": 0, "workers_total": 5},
        "safety_harness": {"status": "Not Required", "compliance": True,  "workers_compliant": 0, "workers_total": 0},
        "safety_gloves": {"status": "Detected", "compliance": True,  "workers_compliant": 2, "workers_total": 2},
        "eye_protection": {"status": "Not Detected", "compliance": False, "workers_compliant": 0, "workers_total": 5}
    },
    "site_hazards": [
        {
            "hazard": "Inadequate High-Visibility Vests",
            "severity": "High",
            "description": "2 out of 5 workers lack high-visibility vests, increasing risk during low-light operations.",
            "remedy": "Immediately issue IS 3521 compliant vests; implement gear checklist at entry gate."
        },
        {
            "hazard": "Unprotected Excavation Zone",
            "severity": "Critical",
            "description": "Open excavation pit detected without perimeter barriers or safety netting.",
            "remedy": "Install OSHA 1926.502 compliant fall protection barriers; add warning signage."
        },
        {
            "hazard": "Electrical Cable Exposure",
            "severity": "Medium",
            "description": "Uninsulated power cables observed on the ground in high-traffic zone.",
            "remedy": "Route cables overhead or through conduit; perform immediate electrical inspection."
        },
        {
            "hazard": "Missing Eye Protection",
            "severity": "Medium",
            "description": "Workers performing grinding operations without safety glasses.",
            "remedy": "Enforce ANSI Z87.1 eye protection; conduct toolbox talk on PPE requirements."
        }
    ],
    "osha_standards_referenced": ["1926.100", "1926.102", "1926.501", "1926.416"],
    "is_standards_referenced": ["IS 456:2000", "IS 3521", "IS 15684"],
    "audit_summary": "The site demonstrates partial PPE compliance. While hard hats and gloves are well-adopted, high-vis vests and eye protection require immediate corrective action. Two critical/high hazards demand urgent attention before operations resume."
}

DEMO_CRACK_RESULT = {
    "defects": [
        {
            "defect_type": "Structural Shear Crack",
            "crack_width_mm": 2.8,
            "length_estimate_m": 0.65,
            "severity": "High",
            "urgency": "Immediate — Within 7 Days",
            "location": "Column-beam junction, East elevation",
            "root_causes": [
                "Differential foundation settlement",
                "Overloading beyond design capacity",
                "Inadequate shear reinforcement (IS 456 non-compliance)"
            ],
            "recommended_repairs": [
                "Epoxy injection grouting (low-viscosity resin, 0.2–0.4 MPa)",
                "Carbon fibre reinforcement polymer (CFRP) wrapping",
                "Structural assessment by licensed civil engineer (mandatory)"
            ],
            "risk_assessment": "High risk of progressive failure if untreated. Affects load-bearing integrity."
        },
        {
            "defect_type": "Thermal Expansion Crack",
            "crack_width_mm": 0.4,
            "length_estimate_m": 1.2,
            "severity": "Low",
            "urgency": "Routine — Within 90 Days",
            "location": "External facade, South wall",
            "root_causes": [
                "Diurnal thermal cycling",
                "Inadequate expansion joint spacing",
                "Low cement-aggregate ratio"
            ],
            "recommended_repairs": [
                "Polyurethane sealant application",
                "Install additional expansion joints per IS 3201",
                "Surface elastomeric coating"
            ],
            "risk_assessment": "Cosmetic/minor structural concern. Monitor for widening over 6 months."
        }
    ],
    "overall_structural_rating": "MODERATE_CONCERN",
    "inspection_standard": "IS 13311 / ACI 224R",
    "immediate_action_required": True,
    "summary": "Two defects identified. One structural shear crack requires immediate professional intervention. The thermal crack is cosmetic but should be addressed in routine maintenance."
}

DEMO_VALUATION = {
    "project_budget_lakhs": 312.5,
    "capex_incurred_lakhs": 187.4,
    "market_valuation_lakhs": 425.0,
    "steel_requirement_mt": 48.6,
    "cement_requirement_bags": 18240,
    "cost_per_sqft_inr": 2500,
    "break_even_sqft_rate": 3200,
    "recommended_sale_rate_inr": 4150,
    "roi_percent": 36.0,
    "milestone_status": "Structure Complete — Finishing Ongoing"
}


# ─── Gemini Client ─────────────────────────────────────────────────────────────

class GeminiClient:
    """Wraps Gemini API calls with a graceful demo-mode fallback."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.demo_mode = not (api_key and GENAI_AVAILABLE)
        self.model = None

        if not self.demo_mode:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel("gemini-1.5-flash")
            except Exception:
                self.demo_mode = True

    def _image_to_part(self, image_bytes: bytes, mime_type: str = "image/jpeg"):
        """Convert image bytes to a Gemini-compatible Part."""
        if not GENAI_AVAILABLE:
            return None
        return {"mime_type": mime_type, "data": base64.b64encode(image_bytes).decode()}

    def _extract_json(self, text: str) -> dict:
        """Extract the first JSON object from model output."""
        # Try to find JSON block between ```json ... ```
        match = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        # Try raw JSON
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            return json.loads(match.group(0))
        raise ValueError("No JSON object found in model response.")

    def _call(self, prompt: str, image_bytes: Optional[bytes] = None,
              mime_type: str = "image/jpeg") -> str:
        """Generic Gemini call, returns raw text."""
        parts = [prompt]
        if image_bytes:
            parts = [self._image_to_part(image_bytes, mime_type), prompt]
        response = self.model.generate_content(parts)
        return response.text

    # ── Tab 1: PPE Safety Audit ───────────────────────────────────────────────

    def analyze_ppe(self, image_bytes: Optional[bytes] = None) -> dict:
        if self.demo_mode:
            return DEMO_PPE_RESULT

        prompt = """You are an expert OSHA and IS 456 certified construction safety auditor.
Analyze this construction site image for PPE compliance and safety hazards.

Return ONLY valid JSON with this exact structure:
{
  "safety_score": <integer 0-100>,
  "overall_status": "<COMPLIANT|NEEDS_IMPROVEMENT|NON_COMPLIANT|CRITICAL>",
  "ppe_detection": {
    "hard_hat": {"status": "<Detected|Not Detected|Partial>", "compliance": <bool>, "workers_compliant": <int>, "workers_total": <int>},
    "high_vis_vest": {"status": "<Detected|Not Detected|Partial>", "compliance": <bool>, "workers_compliant": <int>, "workers_total": <int>},
    "steel_toe_boots": {"status": "<Detected|Not Detected|Not Verified|Partial>", "compliance": <bool>, "workers_compliant": <int>, "workers_total": <int>},
    "safety_harness": {"status": "<Detected|Not Detected|Not Required|Partial>", "compliance": <bool>, "workers_compliant": <int>, "workers_total": <int>},
    "safety_gloves": {"status": "<Detected|Not Detected|Partial>", "compliance": <bool>, "workers_compliant": <int>, "workers_total": <int>},
    "eye_protection": {"status": "<Detected|Not Detected|Partial>", "compliance": <bool>, "workers_compliant": <int>, "workers_total": <int>}
  },
  "site_hazards": [
    {
      "hazard": "<hazard name>",
      "severity": "<Low|Medium|High|Critical>",
      "description": "<detailed description>",
      "remedy": "<corrective action>"
    }
  ],
  "osha_standards_referenced": ["<standard codes>"],
  "is_standards_referenced": ["<IS codes>"],
  "audit_summary": "<comprehensive 2-3 sentence summary>"
}"""
        try:
            raw = self._call(prompt, image_bytes)
            return self._extract_json(raw)
        except Exception as e:
            return {**DEMO_PPE_RESULT, "_note": f"Fallback to demo: {str(e)}"}

    # ── Tab 2: Crack Diagnostics ──────────────────────────────────────────────

    def analyze_crack(self, image_bytes: Optional[bytes] = None) -> dict:
        if self.demo_mode:
            return DEMO_CRACK_RESULT

        prompt = """You are a licensed structural engineer specializing in concrete diagnostics per IS 13311 and ACI 224R standards.
Analyze the provided image of a concrete/masonry surface for cracks and defects.

Return ONLY valid JSON:
{
  "defects": [
    {
      "defect_type": "<Hairline|Settlement|Structural Shear|Thermal Expansion|Spalling|Corrosion-Induced|Alkali-Silica Reaction>",
      "crack_width_mm": <float>,
      "length_estimate_m": <float>,
      "severity": "<Low|Medium|High|Critical>",
      "urgency": "<Immediate — Within 7 Days|Short-term — Within 30 Days|Routine — Within 90 Days|Monitor>",
      "location": "<location description>",
      "root_causes": ["<cause 1>", "<cause 2>"],
      "recommended_repairs": ["<repair method 1>", "<repair method 2>"],
      "risk_assessment": "<risk description>"
    }
  ],
  "overall_structural_rating": "<SAFE|MINOR_CONCERN|MODERATE_CONCERN|MAJOR_CONCERN|CRITICAL>",
  "inspection_standard": "IS 13311 / ACI 224R",
  "immediate_action_required": <bool>,
  "summary": "<2-3 sentence overall assessment>"
}"""
        try:
            raw = self._call(prompt, image_bytes)
            return self._extract_json(raw)
        except Exception as e:
            return {**DEMO_CRACK_RESULT, "_note": f"Fallback to demo: {str(e)}"}

    # ── Tab 4: Chatbot ────────────────────────────────────────────────────────

    def chat(self, messages: list, user_message: str) -> str:
        if self.demo_mode:
            return (
                "🤖 **Demo Mode Active** — Connect your Gemini API key in the sidebar for real AI responses.\n\n"
                "In production, I would answer construction engineering queries including:\n"
                "- Structural load calculations and safety factors\n"
                "- IS 456 / OSHA compliance guidance\n"
                "- Material quantity estimation\n"
                "- Site scheduling and critical path analysis\n"
                "- Concrete mix design per IS 10262\n\n"
                f"Your query was: *\"{user_message}\"*"
            )

        system_prompt = """You are an expert construction engineering assistant with deep knowledge of:
- IS 456:2000, IS 875, IS 1893 structural codes
- OSHA 1926 construction safety standards
- Indian construction cost estimation and real estate valuation
- Concrete technology, structural design, and project management
- Geotechnical engineering and foundation design

Provide precise, practical, and actionable responses. Use bullet points for clarity.
Format your responses in markdown. Keep responses concise but comprehensive."""

        history = [{"role": "user", "parts": [system_prompt]},
                   {"role": "model", "parts": ["Understood. I'm ready to assist with construction engineering queries."]}]

        for msg in messages[-10:]:  # last 10 messages for context
            history.append({"role": msg["role"], "parts": [msg["content"]]})

        try:
            chat_session = self.model.start_chat(history=history)
            response = chat_session.send_message(user_message)
            return response.text
        except Exception as e:
            return f"⚠️ Error generating response: {str(e)}"

    # ── Architectural Rendering Prompt Generator ──────────────────────────────

    def generate_render_prompt(self, structure_type: str, sqft: float,
                               location: str, style: str = "modern") -> str:
        """Generate a Pollinations-compatible architectural rendering prompt."""
        return (
            f"Photorealistic architectural 3D rendering of a {structure_type.lower()}, "
            f"{sqft:.0f} sq ft built-up area, {style} Indian architecture style, "
            f"{location} urban context, golden hour lighting, aerial perspective, "
            f"professional architectural visualization, 8K detail, glass facade, "
            f"landscaped surroundings, ultra-realistic materials"
        )
