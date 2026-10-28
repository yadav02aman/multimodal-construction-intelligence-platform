"""
Multimodal Construction Intelligence Platform
Turnkey Streamlit Application (Skill Wallet Capstone Project 1)
Platform ID: 6ac4c98d1dcde6d7857c1642
"""
import streamlit as st
import json
import io
from PIL import Image

# Import platform modules
from modules.gemini_client import GeminiPlatformClient
from modules.safety_audit import analyze_site_safety
from modules.crack_diagnostics import analyze_crack_diagnostics
from modules.valuation_engine import calculate_construction_finances, generate_architectural_render_url
from modules.weather_advisor import get_weather_protocol, WEATHER_PROTOCOLS
from modules.chatbot import handle_chat_query
from modules.sample_data import generate_sample_ppe_image, generate_sample_crack_image

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Modern CSS Styling
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Global layout & typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Top banner header */
    .platform-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F2A4A 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 22px 28px;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .platform-title {
        font-size: 26px;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.5px;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .platform-subtitle {
        font-size: 14px;
        color: #94A3B8;
        line-height: 1.5;
    }
    .platform-id-pill {
        display: inline-block;
        background: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.4);
        padding: 3px 10px;
        border-radius: 9999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 600;
        margin-left: 10px;
    }

    /* Metric cards */
    .metric-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 18px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        border-color: #38BDF8;
        transform: translateY(-2px);
    }
    .metric-label {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #94A3B8;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 26px;
        font-weight: 700;
        color: #F1F5F9;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-delta {
        font-size: 12px;
        margin-top: 4px;
        font-weight: 500;
    }

    /* Severity badges */
    .badge-critical {
        background: #DC2626;
        color: white;
        padding: 3px 9px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 11px;
    }
    .badge-high {
        background: #EA580C;
        color: white;
        padding: 3px 9px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 11px;
    }
    .badge-medium {
        background: #D97706;
        color: white;
        padding: 3px 9px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 11px;
    }
    .badge-low {
        background: #059669;
        color: white;
        padding: 3px 9px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 11px;
    }

    /* Status Pill */
    .status-pill-ok {
        background: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 13px;
    }
    .status-pill-warn {
        background: rgba(245, 158, 11, 0.15);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.4);
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 13px;
    }
    .status-pill-danger {
        background: rgba(239, 68, 68, 0.15);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 13px;
    }

    /* Protocol alert banner */
    .protocol-banner {
        border-left: 6px solid #F59E0B;
        background: #1E293B;
        padding: 16px 20px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 20px;
    }

    /* Code block tweaks */
    pre, code {
        font-family: 'JetBrains Mono', monospace !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar Setup & API Management
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🏗️ Construction Platform")
    st.markdown("**Skill Wallet Capstone Project 1**")
    st.markdown('<span class="platform-id-pill">ID: 6ac4c98d1dcde6d7857c1642</span>', unsafe_allow_html=True)
    st.markdown("---")

    st.subheader("🔑 Gemini API Configuration")
    user_api_key = st.text_input(
        "Google Gemini API Key",
        type="password",
        help="Enter your Google AI Studio Gemini API Key. If left empty, the platform runs in Demonstration Mode with domain-accurate simulations.",
        placeholder="AIzaSy..."
    )

    # Initialize client
    gemini_client = GeminiPlatformClient(api_key=user_api_key)

    if gemini_client.is_live():
        st.success("🟢 Live Gemini 1.5/2.5 API Connected", icon="✅")
    else:
        st.info("🟡 Demonstration Mode Active\n(Instant testing without API Key)", icon="ℹ️")

    st.markdown("---")
    st.subheader("📐 Architecture Blueprint")
    with st.expander("System Flow & Microservices", expanded=False):
        st.markdown("""
        **Pipeline Components:**
        1. **Frontend**: Streamlit / React Web App
        2. **API & Logic**: FastAPI REST Controllers + Python Engines
        3. **Multimodal AI**: Gemini 1.5 Flash / Pro + LLaMA Vision
        4. **Visual Synthesis**: Pollinations / Flux Generative 3D
        5. **Standards**: OSHA 1926, IS 456:2000, IS 875, IS 2925
        """)

    st.markdown("---")
    st.caption("Multimodal Construction Intelligence • 2026 Edition")


# ---------------------------------------------------------
# Main Page Header
# ---------------------------------------------------------
st.markdown("""
<div class="platform-header">
    <div class="platform-title">
        <span>🏗️ Multimodal Construction Intelligence Platform</span>
        <span class="platform-id-pill">6ac4c98d1dcde6d7857c1642</span>
    </div>
    <div class="platform-subtitle">
        Intelligent decision-support system analyzing site photos to audit PPE compliance, classify concrete cracks,
        estimate project budgets & real estate valuation in INR, and deliver weather-aware site safety protocols.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Tabs Navigation (Epics 2, 3, 4, 5)
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🦺 Tab 1: Site Safety & PPE Audit (Epic 2)",
    "🔬 Tab 2: Crack Diagnostics & Structural Integrity (Epic 2)",
    "📊 Tab 3: Planning & Real Estate Valuation (Epic 3)",
    "🌤️ Tab 4: Daily Site Assistant & Weather Advisory (Epic 5)"
])

# =========================================================
# TAB 1: SITE SAFETY & PPE AUDIT (EPIC 2)
# =========================================================
with tab1:
    st.markdown("### 🦺 Site Safety & Worker PPE Vision Audit")
    st.markdown(
        "Upload site imagery to perform an automated visual audit of worker Personal Protective Equipment (PPE) "
        "and physical hazards under **OSHA 29 CFR 1926** and Indian Standard **IS 2925 / IS 3521**."
    )

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("#### 📤 Input Site Photography")
        uploaded_ppe_file = st.file_uploader(
            "Upload Construction Site Image (JPG/PNG)",
            type=["jpg", "jpeg", "png"],
            key="ppe_uploader"
        )

        use_sample_ppe = st.button("🖼️ Load Sample Inspection Photo", key="btn_sample_ppe")

        ppe_image_bytes = None
        if use_sample_ppe:
            ppe_image_bytes = generate_sample_ppe_image()
            st.session_state["ppe_current_image"] = ppe_image_bytes
            st.session_state["ppe_is_sample"] = True
        elif uploaded_ppe_file is not None:
            ppe_image_bytes = uploaded_ppe_file.getvalue()
            st.session_state["ppe_current_image"] = ppe_image_bytes
            st.session_state["ppe_is_sample"] = False
        elif "ppe_current_image" in st.session_state:
            ppe_image_bytes = st.session_state["ppe_current_image"]

        if ppe_image_bytes:
            st.image(ppe_image_bytes, caption="Active Site Inspection Target", use_container_width=True)
            analyze_ppe_btn = st.button("🚀 Run AI Safety & PPE Audit", type="primary", use_container_width=True)
        else:
            st.info("👆 Upload an image or click 'Load Sample Inspection Photo' to begin audit.")
            analyze_ppe_btn = False

    with col2:
        st.markdown("#### 📋 Safety Audit Diagnostics")

        if analyze_ppe_btn and ppe_image_bytes:
            with st.spinner("Analyzing site hazards and worker PPE compliance against IS/OSHA standards..."):
                audit_result, is_live, msg = analyze_site_safety(gemini_client, ppe_image_bytes)
                st.session_state["ppe_audit_result"] = audit_result
                st.session_state["ppe_audit_mode"] = msg

        if "ppe_audit_result" in st.session_state:
            res = st.session_state["ppe_audit_result"]
            mode_msg = st.session_state.get("ppe_audit_mode", "")

            # Diagnostics mode banner
            st.caption(f"Engine Status: **{mode_msg}**")

            # Metric Cards Row
            score = res.get("safety_score", 0)
            status = res.get("overall_status", "Unknown")
            workers = res.get("detected_workers_count", 0)

            mcol1, mcol2, mcol3 = st.columns(3)
            with mcol1:
                score_color = "#10B981" if score >= 80 else ("#F59E0B" if score >= 50 else "#EF4444")
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Safety Score</div>
                    <div class="metric-value" style="color: {score_color};">{score}/100</div>
                    <div class="metric-delta">Target: ≥85 (IS 456)</div>
                </div>
                """, unsafe_allow_html=True)

            with mcol2:
                pill_class = "status-pill-ok" if "Compliant" == status else ("status-pill-warn" if "Partially" in status else "status-pill-danger")
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Compliance Status</div>
                    <div style="margin-top: 6px;"><span class="{pill_class}">{status}</span></div>
                    <div class="metric-delta" style="margin-top: 10px;">OSHA 1926.95 Audit</div>
                </div>
                """, unsafe_allow_html=True)

            with mcol3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Workers Detected</div>
                    <div class="metric-value">{workers}</div>
                    <div class="metric-delta">Active in sector</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            # Executive Summary
            if "audit_summary" in res:
                st.markdown(f"**Audit Summary:** {res['audit_summary']}")

            # PPE Checklist
            st.markdown("##### 🦺 PPE Detection Checklist")
            checklist = res.get("ppe_detection", [])
            for item in checklist:
                st_status = item.get("status", "Not Visible")
                icon = "✅" if "Compliant" == st_status else ("⚠️" if "Partially" in st_status else "❌")
                with st.expander(f"{icon} **{item.get('item')}** — {st_status} ({item.get('compliance_rate', 'N/A')})", expanded=True):
                    st.write(f"**Observations:** {item.get('observations', 'N/A')}")

            # Identified Hazards
            st.markdown("##### ⚠️ Identified Site Hazards & Remedial Actions")
            hazards = res.get("identified_site_hazards", [])
            for h in hazards:
                sev = h.get("severity", "Medium")
                badge_class = f"badge-{sev.lower()}" if sev.lower() in ["critical", "high", "medium", "low"] else "badge-medium"
                
                st.markdown(f"""
                <div style="background: #1E293B; border-left: 4px solid {'#EF4444' if sev in ['Critical','High'] else '#F59E0B'}; padding: 12px 16px; border-radius: 4px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                        <strong style="color: #F8FAFC;">{h.get('id', 'HAZ')}: {h.get('hazard_title', 'Hazard')}</strong>
                        <span class="{badge_class}">{sev.upper()}</span>
                    </div>
                    <div style="font-size: 13px; color: #94A3B8; margin-bottom: 6px;">
                        <strong>Location:</strong> {h.get('location_in_image', 'Site')} | <strong>Standard:</strong> <code>{h.get('regulatory_code', 'OSHA')}</code>
                    </div>
                    <div style="font-size: 13px; color: #38BDF8;">
                        <strong>Corrective Action:</strong> {h.get('corrective_remedy', '')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Downloadable JSON Report
            json_report = json.dumps(res, indent=2)
            st.download_button(
                label="📥 Download Structured JSON Safety Report",
                data=json_report,
                file_name="site_safety_audit_report.json",
                mime="application/json",
                use_container_width=True
            )
        else:
            st.info("Run an inspection on the left panel to populate safety metrics and hazard analysis.")


# =========================================================
# TAB 2: CRACK DIAGNOSTICS & STRUCTURAL INTEGRITY (EPIC 2)
# =========================================================
with tab2:
    st.markdown("### 🔬 Concrete Defect & Structural Crack Diagnostics")
    st.markdown(
        "Classify concrete fractures, estimate crack aperture (mm), identify root failure mechanics, and obtain "
        "prescriptive remediation specifications under **IS 456:2000** and **ACI 224R-01**."
    )

    c1, c2 = st.columns([1, 1], gap="large")

    with c1:
        st.markdown("#### 📤 Input Structural Surface Image")
        uploaded_crack_file = st.file_uploader(
            "Upload Concrete / Wall Defect Photo (JPG/PNG)",
            type=["jpg", "jpeg", "png"],
            key="crack_uploader"
        )

        use_sample_crack = st.button("🔍 Load Sample Concrete Shear Crack", key="btn_sample_crack")

        crack_image_bytes = None
        if use_sample_crack:
            crack_image_bytes = generate_sample_crack_image()
            st.session_state["crack_current_image"] = crack_image_bytes
        elif uploaded_crack_file is not None:
            crack_image_bytes = uploaded_crack_file.getvalue()
            st.session_state["crack_current_image"] = crack_image_bytes
        elif "crack_current_image" in st.session_state:
            crack_image_bytes = st.session_state["crack_current_image"]

        if crack_image_bytes:
            st.image(crack_image_bytes, caption="Structural Concrete Surface Target", use_container_width=True)
            analyze_crack_btn = st.button("⚡ Diagnose Structural Integrity", type="primary", use_container_width=True)
        else:
            st.info("👆 Upload a concrete photo or click 'Load Sample Concrete Shear Crack'.")
            analyze_crack_btn = False

    with c2:
        st.markdown("#### 🩺 Structural Diagnostics & Engineering Specification")

        if analyze_crack_btn and crack_image_bytes:
            with st.spinner("Analyzing concrete fracture geometry, shear lines, and IS 456 thresholds..."):
                crack_result, is_live, msg = analyze_crack_diagnostics(gemini_client, crack_image_bytes)
                st.session_state["crack_diag_result"] = crack_result
                st.session_state["crack_diag_mode"] = msg

        if "crack_diag_result" in st.session_state:
            c_res = st.session_state["crack_diag_result"]
            c_mode = st.session_state.get("crack_diag_mode", "")

            st.caption(f"Forensic Engine: **{c_mode}**")

            defect_type = c_res.get("defect_type", "Defect")
            width_mm = c_res.get("estimated_crack_width_mm", 0.0)
            risk = c_res.get("structural_risk_score", 0)
            urgency = c_res.get("urgency_level", "Moderate")

            # Metrics
            mc1, mc2, mc3 = st.columns(3)
            with mc1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Defect Classification</div>
                    <div style="font-size: 16px; font-weight: 700; color: #F59E0B; margin-top: 4px;">{defect_type}</div>
                    <div class="metric-delta">Element: {c_res.get('structural_element', 'RCC Member')}</div>
                </div>
                """, unsafe_allow_html=True)

            with mc2:
                width_color = "#EF4444" if width_mm > 0.3 else "#10B981"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Estimated Width</div>
                    <div class="metric-value" style="color: {width_color};">{width_mm} mm</div>
                    <div class="metric-delta">IS 456 Limit: 0.30 mm</div>
                </div>
                """, unsafe_allow_html=True)

            with mc3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Risk & Urgency</div>
                    <div class="metric-value" style="color: #EA580C;">{risk}/100</div>
                    <div class="metric-delta">{urgency}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            # Compliance banner
            comp_status = c_res.get("is_456_compliance_status", "")
            if "Exceeds" in comp_status or "Threat" in comp_status:
                st.error(f"⚠️ **IS 456 Compliance Alert:** {comp_status}")
            else:
                st.success(f"✅ **IS 456 Compliance:** {comp_status}")

            # Root Causes
            st.markdown("##### 🔬 Root Failure Causes")
            for rc in c_res.get("root_causes", []):
                st.markdown(f"- 🔸 {rc}")

            # Engineering Repairs Roadmap
            st.markdown("##### 🛠️ Prescriptive Engineering Repairs")
            repairs = c_res.get("recommended_engineering_repairs", [])
            for rep in repairs:
                with st.expander(f"Step {rep.get('step')}: **{rep.get('method')}**", expanded=True):
                    st.markdown(f"**Materials / Specifications:** `{rep.get('materials')}`")
                    st.markdown(f"**Rationale:** {rep.get('engineering_rationale')}")

            # Monitoring Protocol
            if "monitoring_protocol" in c_res:
                st.info(f"📡 **Continuous Monitoring Protocol:** {c_res['monitoring_protocol']}")

            # Downloadable Report
            crack_report_json = json.dumps(c_res, indent=2)
            st.download_button(
                label="📥 Download Structural Crack Audit Report (JSON)",
                data=crack_report_json,
                file_name="structural_crack_audit_report.json",
                mime="application/json",
                use_container_width=True
            )
        else:
            st.info("Run crack diagnostics on the left panel to populate engineering specifications.")


# =========================================================
# TAB 3: PLANNING & REAL ESTATE VALUATION (EPIC 3)
# =========================================================
with tab3:
    st.markdown("### 📊 Project Planning, Indian INR Valuation & 3D Synthesis")
    st.markdown(
        "Estimate total project budget, incurred CapEx, finished market valuation in **INR (Lakhs / Crores)**, "
        "material quantities (Steel, Cement, Aggregates), and synthesize conceptual 3D renders via **Pollinations / Flux**."
    )

    vcol1, vcol2 = st.columns([1, 1], gap="large")

    with vcol1:
        st.markdown("#### ⚙️ Project Parameters")

        structure_type = st.selectbox(
            "Structure Classification",
            options=[
                "Residential High-Rise (G+15)",
                "Commercial Complex / Tech Park",
                "Industrial Pre-Engineered Warehouse",
                "Luxury Gated Villa Development",
                "Affordable Housing Society (PMAY)"
            ]
        )

        location_tier = st.selectbox(
            "Location Urban Tier (India)",
            options=[
                "Tier 1 (Mumbai, Delhi-NCR, Bengaluru)",
                "Tier 2 (Pune, Hyderabad, Ahmedabad, Chennai)",
                "Tier 3 (Emerging Urban & Industrial Hubs)"
            ]
        )

        built_up_sqft = st.number_input(
            "Total Built-up Area (Sq. Ft.)",
            min_value=1000,
            max_value=2000000,
            value=45000,
            step=5000
        )

        completion_pct = st.slider(
            "Construction Completion Progress (%)",
            min_value=0,
            max_value=100,
            value=45,
            format="%d%%"
        )

        # Financial Calculations
        finances = calculate_construction_finances(
            structure_type=structure_type,
            location_tier=location_tier,
            built_up_sqft=built_up_sqft,
            completion_percentage=completion_pct
        )

        st.markdown("---")
        st.markdown("#### 🧱 Material Requirements & Milestone Breakdown")

        st.markdown(f"**Current Milestone:** `{finances['milestone']['current']}`")
        st.progress(completion_pct / 100.0)
        st.caption(f"Next Target: {finances['milestone']['next']}")

        mat = finances["materials"]
        m_row1, m_row2 = st.columns(2)
        with m_row1:
            st.markdown(f"""
            - **Cement Required:** {mat['total_cement_bags']:,.0f} bags (50kg)
            - **Cement Consumed:** {mat['cement_consumed_bags']:,.0f} bags
            - **Sand / Coarse Aggregate:** {mat['total_sand_cft']:,.0f} cu.ft
            """)
        with m_row2:
            st.markdown(f"""
            - **TMT Steel Rebar:** {mat['total_steel_tonnes']:.1f} Tonnes
            - **Steel Installed:** {mat['steel_consumed_tonnes']:.1f} Tonnes
            - **Total Labor Estimate:** {mat['total_labor_mandays']:,.0f} person-days
            """)

    with vcol2:
        st.markdown("#### 💰 Financial Ledger & Real Estate Valuation (INR)")

        fc1, fc2 = st.columns(2)
        with fc1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Project Budget</div>
                <div class="metric-value">{finances['total_project_budget_fmt']}</div>
                <div class="metric-delta">@ ₹{finances['cost_per_sqft']:,}/sqft</div>
            </div>
            """, unsafe_allow_html=True)

        with fc2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">CapEx Incurred to Date</div>
                <div class="metric-value" style="color: #F59E0B;">{finances['capex_incurred_fmt']}</div>
                <div class="metric-delta">{completion_pct}% Capital Disbursed</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        fc3, fc4 = st.columns(2)
        with fc3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Current Asset Valuation</div>
                <div class="metric-value" style="color: #10B981;">{finances['current_asset_valuation_fmt']}</div>
                <div class="metric-delta">Risk-Adjusted Value</div>
            </div>
            """, unsafe_allow_html=True)

        with fc4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Completed Market Value</div>
                <div class="metric-value" style="color: #38BDF8;">{finances['completed_market_value_fmt']}</div>
                <div class="metric-delta">Projected Gross Margin: {finances['margin_percentage']:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 🎨 Conceptual 3D Architectural Synthesis")
        st.caption("Auto-generated generative 3D visual preview utilizing Pollinations AI / Flux engine.")

        render_url, render_prompt = generate_architectural_render_url(
            structure_type=structure_type,
            location_tier=location_tier,
            completion_percentage=completion_pct
        )

        with st.expander("📝 View Architectural Synthesis Prompt"):
            st.code(render_prompt, language="text")

        st.image(
            render_url,
            caption=f"Conceptual 3D Rendering: {structure_type} ({completion_pct}% Stage)",
            use_container_width=True
        )


# =========================================================
# TAB 4: DAILY SITE ASSISTANT & WEATHER ADVISORY (EPIC 5)
# =========================================================
with tab4:
    st.markdown("### 🌤️ Daily Site Assistant & Weather-Aware Advisory")
    st.markdown(
        "Real-time hazard mitigation protocols dynamically tailored to weather extremes, plus a dedicated "
        "multi-turn **CivAI Construction Engineering Assistant**."
    )

    wcol1, wcol2 = st.columns([1, 1], gap="large")

    with wcol1:
        st.markdown("#### ⚡ Weather Condition & Safety Protocols")

        selected_weather = st.selectbox(
            "Select Current On-Site Meteorological Condition",
            options=list(WEATHER_PROTOCOLS.keys()),
            index=0
        )

        proto = get_weather_protocol(selected_weather)

        # Weather Banner
        st.markdown(f"""
        <div class="protocol-banner" style="border-left-color: {proto['badge_color']};">
            <div style="font-size: 20px; font-weight: 700; color: #F8FAFC; margin-bottom: 4px;">
                {proto['icon']} {selected_weather}
            </div>
            <div style="font-size: 13px; font-weight: 700; color: {proto['badge_color']}; margin-bottom: 6px;">
                {proto['status_level']}
            </div>
            <div style="font-size: 13px; color: #CBD5E1; margin-bottom: 8px;">
                {proto['summary']}
            </div>
            <div style="background: rgba(0,0,0,0.3); padding: 8px 12px; border-radius: 4px; font-size: 13px; font-weight: 700; color: #FBBF24;">
                🚨 {proto['mandatory_action']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("##### 📜 Mandatory IS & OSHA Compliance Actions")
        for p in proto["protocols"]:
            with st.expander(f"⚠️ {p['category']} (Ref: `{p['code']}`)", expanded=True):
                st.write(p["mandate"])

        st.markdown("##### 💧 Concrete Curing & Placement Advisory")
        st.info(proto["concrete_advisory"], icon="🧱")

    with wcol2:
        st.markdown("#### 🤖 CivAI Multi-Turn Engineering Chatbot")
        st.caption("Trained on IS 456:2000, IS 875, NBC 2016, and OSHA 1926 standards.")

        # Preset query buttons
        st.markdown("💡 *Quick Technical Inquiries:*")
        pq_col1, pq_col2 = st.columns(2)
        with pq_col1:
            if st.button("⏱️ Minimum Curing (IS 456)", use_container_width=True):
                st.session_state["pending_chat_prompt"] = "What is the minimum curing period for OPC vs PPC concrete under IS 456?"
            if st.button("📊 Slump for M25 Pumpable", use_container_width=True):
                st.session_state["pending_chat_prompt"] = "Explain permissible slump values for pumpable concrete mix M25."
        with pq_col2:
            if st.button("🩹 1.2mm Shear Crack Repair", use_container_width=True):
                st.session_state["pending_chat_prompt"] = "How to treat a 1.2mm structural shear crack in an RCC beam?"
            if st.button("🦺 Scaffolding >6ft Rules", use_container_width=True):
                st.session_state["pending_chat_prompt"] = "What are mandatory PPE and fall arrest protocols for scaffolding above 6 feet?"

        # Chat history state
        if "chat_messages" not in st.session_state:
            st.session_state["chat_messages"] = [
                {
                    "role": "assistant",
                    "content": "Hello Engineer! I am CivAI, your Senior Principal Civil Engineer & Safety Consultant. How can I assist you with IS codes, OSHA compliance, mix designs, or structural forensics today?"
                }
            ]

        # Display history
        chat_container = st.container(height=380)
        with chat_container:
            for message in st.session_state["chat_messages"]:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # Chat input
        prompt = st.chat_input("Ask CivAI a structural or safety question...")

        if "pending_chat_prompt" in st.session_state and st.session_state["pending_chat_prompt"]:
            prompt = st.session_state.pop("pending_chat_prompt")

        if prompt:
            # Append user message
            st.session_state["chat_messages"].append({"role": "user", "content": prompt})

            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    with st.spinner("Analyzing civil engineering codes..."):
                        reply, live = handle_chat_query(
                            gemini_client,
                            st.session_state["chat_messages"][:-1],
                            prompt
                        )
                        st.markdown(reply)

            st.session_state["chat_messages"].append({"role": "assistant", "content": reply})
            st.rerun()

        if st.button("🗑️ Clear Chat History"):
            st.session_state["chat_messages"] = [
                {
                    "role": "assistant",
                    "content": "Conversation history cleared. Ready for your next structural engineering or safety inquiry!"
                }
            ]
            st.rerun()
