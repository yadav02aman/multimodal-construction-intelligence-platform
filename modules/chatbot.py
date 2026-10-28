"""
Epic 5: Civil Engineering & Construction Site Assistant Chatbot.
Domain-expert conversational agent versed in IS Codes, OSHA, structural forensics,
mix design (M20-M50), and site safety protocols.
"""
from typing import List, Dict, Tuple
from .gemini_client import GeminiPlatformClient

CIVIL_CHATBOT_SYSTEM_PROMPT = """
You are "CivAI", a Senior Principal Structural Engineer and Site Safety Director with 25+ years of experience across:
- Indian Standards: IS 456:2000 (Plain and Reinforced Concrete), IS 875 (Parts 1-5 Design Loads), IS 1893 (Earthquake Resistant Design), IS 3696 / IS 3764 (Site Safety), NBC 2016.
- Global Safety: OSHA 29 CFR 1926 (Safety and Health Regulations for Construction).
- Field Execution: RMC batching, slump tests, concrete curing, crack repair (epoxy, polyurethane, CFRP), formwork removal intervals, and real estate valuation.

Guidelines:
1. Always give precise, technically rigorous, and actionable civil engineering answers.
2. Cite the exact IS code clause or OSHA section where appropriate.
3. Be professional, direct, and structured (use bullet points, step-by-step methodologies, and cautionary notes).
4. If asked about dangerous structural cracking or site hazards, always emphasize safety first and physical non-destructive testing (NDT).
"""

KNOWLEDGE_BASE_FALLBACKS = [
    {
        "keywords": ["curing", "cure", "opc", "ppc", "days", "period"],
        "response": (
            "### IS 456:2000 Concrete Curing Standards (Clause 13.5)\n\n"
            "- **Ordinary Portland Cement (OPC):** Minimum **7 days** under normal ambient conditions; minimum **10 days** when exposed to hot, dry weather conditions.\n"
            "- **Mineral Admixture / Blended Cements (PPC, PSC, GGBS, Fly Ash):** Minimum **10 days** under normal conditions; minimum **14 days** under hot/arid weather.\n\n"
            "**Key Best Practices:**\n"
            "1. Curing must commence as soon as the concrete has hardened sufficiently to resist surface indentation.\n"
            "2. Ponding is mandatory for horizontal slabs; continuous wet hessian/burlap wrapping for vertical columns and beams.\n"
            "3. Premature cessation of curing causes plastic and drying shrinkage micro-cracking and robs the concrete of up to 40% of its target 28-day compressive strength."
        )
    },
    {
        "keywords": ["shear crack", "crack", "beam", "repair", "epoxy", "width"],
        "response": (
            "### Remediation Protocol for Structural Shear Cracks in RCC Beams\n\n"
            "A diagonal shear crack (typically running at ~45° near support zones) indicates diagonal tension exceeding concrete tensile strength.\n\n"
            "**Step-by-Step Remediation Plan:**\n"
            "1. **Load Relief:** Install adjustable Acrow hydraulic props underneath the beam to relieve live and superimposed dead loads.\n"
            "2. **Surface Preparation:** Chip a V-groove (15mm × 15mm) along the crack trajectory; clean with dry, oil-free compressed air.\n"
            "3. **Port Fixing:** Bond injection ports at intervals equal to the member depth (e.g., 200–300mm apart) using epoxy adhesive.\n"
            "4. **Low-Viscosity Epoxy Pressure Injection:** Inject ASTM C881 Type I Grade 1 epoxy (viscosity <200 cPs) beginning at the lowest port until resin flows from the adjacent port.\n"
            "5. **Structural Jacketing / CFRP Wrap:** If shear deficiency is confirmed by structural review, apply bidirectional Carbon Fiber Reinforced Polymer (CFRP) wrap to provide external transverse shear reinforcement (per ACI 440.2R)."
        )
    },
    {
        "keywords": ["slump", "workability", "m25", "pumpable", "mix"],
        "response": (
            "### Permissible Slump Values under IS 456:2000 (Table 2)\n\n"
            "- **Lightly Reinforced Sections (Slabs, Beams, Columns with wide spacing):** 25 mm - 75 mm (Low to Medium workability).\n"
            "- **Heavily Reinforced Sections (Piles, Deep Beams, Retaining Walls):** 75 mm - 125 mm (High workability).\n"
            "- **Pumpable Concrete (M20 / M25 / M30 through 100mm-125mm delivery pipes):**\n"
            "  - Optimal Slump at discharge: **100 mm to 140 mm**.\n"
            "  - Admixture requirement: Polycarboxylate Ether (PCE) based superplasticizer (IS 9103) is mandatory to retain slump for 90 minutes without water bleeding or aggregate segregation.\n"
            "- **Self-Compacting Concrete (SCC):** Slump flow of **600 mm to 750 mm** measured with standard inverted slump cone."
        )
    },
    {
        "keywords": ["scaffolding", "ppe", "height", "fall", "harness", "6 feet"],
        "response": (
            "### Scaffolding & Fall Protection Mandates (IS 3696 & OSHA 1926.501)\n\n"
            "Under OSHA Subpart M & IS 3696 Part 1:\n"
            "1. **Trigger Height:** Fall protection is mandatory for any open edge or platform at or above **1.8 meters (6 feet)** in general construction.\n"
            "2. **Full Body Harness (IS 3521 / ANSI Z359):**\n"
            "   - Must feature shock-absorbing lanyards anchored to a certified tie-off point capable of withstanding 5,000 lbs (22.2 kN) per worker.\n"
            "   - Single-strap waist belts are strictly prohibited for fall arrest.\n"
            "3. **Scaffolding Requirements:**\n"
            "   - Top-rail installed at 42 inches (±3 inches) above the walking surface.\n"
            "   - Mid-rail installed midway at ~21 inches.\n"
            "   - Mandatory 4-inch (100mm) toe-boards to prevent tools from falling onto workers below.\n"
            "   - Green/Yellow/Red Scaff-tag system inspected daily by a designated Competent Person."
        )
    },
    {
        "keywords": ["deshuttering", "formwork", "removal", "striking"],
        "response": (
            "### Formwork Removal (Striking Time) as per IS 456:2000 (Clause 11.3)\n\n"
            "For OPC concrete under normal temperature (>16°C):\n"
            "1. **Vertical formwork to columns, walls, beams:** 16 to 24 hours.\n"
            "2. **Soffit formwork to slabs (props left under):** 3 days.\n"
            "3. **Soffit formwork to beams (props left under):** 7 days.\n"
            "4. **Props to slabs:**\n"
            "   - Spanning up to 4.5m: 7 days.\n"
            "   - Spanning over 4.5m: 14 days.\n"
            "5. **Props to beams and arches:**\n"
            "   - Spanning up to 6m: 14 days.\n"
            "   - Spanning over 6m: 21 days.\n\n"
            "*Note: For PPC or fly-ash blended concrete, prop retention periods should be extended or validated against cube crush tests.*"
        )
    }
]

def fallback_chat_answer(query: str) -> str:
    """Generate intelligent offline fallback answers for civil engineering queries."""
    q_lower = query.lower()
    for item in KNOWLEDGE_BASE_FALLBACKS:
        if any(kw in q_lower for kw in item["keywords"]):
            return item["response"]

    return (
        f"### Civil Engineering Advisory for: \"{query}\"\n\n"
        "According to **IS 456:2000** and standard Indian civil engineering guidelines:\n\n"
        "1. **Safety & Quality Verification:** Ensure all field practices align with certified structural drawings and approved method statements (MS).\n"
        "2. **Material Testing:** Validate 7-day and 28-day cube compressive strength tests, rebars tensile strength (IS 1786), and aggregate grading (IS 383).\n"
        "3. **Regulatory Oversight:** Ensure mandatory compliance with OSHA 1926 standards for temporary structures and the National Building Code (NBC 2016).\n\n"
        "*(Note: You can connect a live Google Gemini API key in the sidebar to engage in deep conversational reasoning on project-specific blueprints and dynamic site challenges.)*"
    )

def handle_chat_query(client: GeminiPlatformClient, history: List[Dict[str, str]], query: str) -> Tuple[str, bool]:
    """
    Process multi-turn chat message using live Gemini or smart offline engineering fallback.
    """
    return client.chat_response(
        history=history,
        user_message=query,
        system_prompt=CIVIL_CHATBOT_SYSTEM_PROMPT,
        fallback_responder=fallback_chat_answer
    )
