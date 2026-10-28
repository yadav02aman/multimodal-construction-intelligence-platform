"""
Epic 2: Site Safety & PPE Vision Audit Module.
Complies with OSHA 29 CFR 1926 & Indian Standards (IS 2925, IS 3521, IS 456).
"""
from typing import Dict, Any, Tuple
from .gemini_client import GeminiPlatformClient

PPE_SYSTEM_INSTRUCTION = """
You are an OSHA & IS 456 certified Senior Construction Safety Auditor and Civil Inspection AI.
Inspect the provided construction site photo with high precision.
You must output ONLY a valid JSON object matching the exact schema below, with zero additional conversational prose.
"""

PPE_AUDIT_PROMPT = """
Perform an exhaustive multimodal construction safety audit of this site image.
Assess worker compliance under OSHA 1926.95, OSHA 1926.501, IS 2925 (Industrial Helmets), and IS 3521 (Safety Harnesses).

Output ONLY this strict JSON structure:
{
  "safety_score": <integer between 0 and 100>,
  "overall_status": "<Compliant | Partially Compliant | Non-Compliant / Hazardous>",
  "audit_summary": "<2-3 sentence executive audit summary>",
  "detected_workers_count": <integer>,
  "ppe_detection": [
    {
      "item": "Safety Helmets (IS 2925 / OSHA 1926.100)",
      "status": "<Compliant | Partially Compliant | Non-Compliant | Not Visible>",
      "compliance_rate": "<e.g. 50% or 100%>",
      "observations": "<Specific observations regarding helmet usage>"
    },
    {
      "item": "High-Visibility Vests (IS 15809 / OSHA 1926.201)",
      "status": "<Compliant | Partially Compliant | Non-Compliant | Not Visible>",
      "compliance_rate": "<e.g. 75% or 100%>",
      "observations": "<Observations on reflective vest compliance>"
    },
    {
      "item": "Steel-Toe Safety Boots (IS 15298 / OSHA 1926.96)",
      "status": "<Compliant | Partially Compliant | Non-Compliant | Not Visible>",
      "compliance_rate": "<e.g. 100% or 50%>",
      "observations": "<Observations on safety footwear>"
    },
    {
      "item": "Fall Arrest Harness & Lanyard (IS 3521 / OSHA 1926.501)",
      "status": "<Compliant | Partially Compliant | Non-Compliant | Not Applicable>",
      "compliance_rate": "<e.g. 100% or N/A>",
      "observations": "<Observations on tie-off points, guardrails, or fall hazard>"
    }
  ],
  "identified_site_hazards": [
    {
      "id": "HAZ-001",
      "hazard_title": "<Concise hazard name>",
      "category": "<PPE Violation | Fall Risk | Scaffolding Defect | Electrical | Housekeeping>",
      "severity": "<Low | Medium | High | Critical>",
      "location_in_image": "<Description of where hazard is located in the frame>",
      "regulatory_code": "<e.g. OSHA 1926.501(b)(1) / IS 3696 Part 1>",
      "corrective_remedy": "<Actionable engineering and safety correction>"
    }
  ],
  "recommended_stop_work_notice": <true or false>
}
"""

DEMO_SAFETY_AUDIT_RESULT: Dict[str, Any] = {
    "safety_score": 58,
    "overall_status": "Partially Compliant",
    "audit_summary": "Active construction activity identified with 2 workers. Worker 1 demonstrates full PPE adherence with certified hard hat, hi-vis vest, and steel-toe footwear. Worker 2 exhibits critical non-compliance lacking head protection and wearing non-rated open footwear near an unguarded slab edge.",
    "detected_workers_count": 2,
    "ppe_detection": [
        {
            "item": "Safety Helmets (IS 2925 / OSHA 1926.100)",
            "status": "Partially Compliant",
            "compliance_rate": "50%",
            "observations": "1 out of 2 workers equipped with certified yellow hard hat; 1 worker completely unprotected from overhead struck-by hazards."
        },
        {
            "item": "High-Visibility Vests (IS 15809 / OSHA 1926.201)",
            "status": "Partially Compliant",
            "compliance_rate": "50%",
            "observations": "Worker 1 wearing Class 2 high-vis reflective vest. Worker 2 wearing low-contrast dark attire with zero reflective striping."
        },
        {
            "item": "Steel-Toe Safety Boots (IS 15298 / OSHA 1926.96)",
            "status": "Non-Compliant",
            "compliance_rate": "50%",
            "observations": "Worker 2 observed wearing unprotective open footwear/slippers, violating puncture and impact foot protection mandates."
        },
        {
            "item": "Fall Arrest Harness & Lanyard (IS 3521 / OSHA 1926.501)",
            "status": "Non-Compliant",
            "compliance_rate": "0%",
            "observations": "Workers operating adjacent to slab boundary (>2m elevation) without perimeter guardrails or tethered safety harnesses."
        }
    ],
    "identified_site_hazards": [
        {
            "id": "HAZ-001",
            "hazard_title": "Absence of Certified Head Protection (Hard Hat)",
            "category": "PPE Violation",
            "severity": "Critical",
            "location_in_image": "Worker on right side of framing deck",
            "regulatory_code": "IS 2925 / OSHA 1926.100(a)",
            "corrective_remedy": "Immediately issue Type I Class E industrial protective helmet before allowing worker to re-enter the active perimeter."
        },
        {
            "id": "HAZ-002",
            "hazard_title": "Unguarded Slab Edge & Missing Fall Restraint",
            "category": "Fall Risk",
            "severity": "High",
            "location_in_image": "Perimeter boundary of concrete level",
            "regulatory_code": "IS 3696 Part 1 / OSHA 1926.501(b)(1)",
            "corrective_remedy": "Erect standard two-tier guardrail system (top rail 42 inches ± 3 inches, mid-rail, and 4-inch toe-board) or install horizontal lifeline."
        },
        {
            "id": "HAZ-003",
            "hazard_title": "Inappropriate Footwear in Heavy Construction Zone",
            "category": "PPE Violation",
            "severity": "High",
            "location_in_image": "Worker 2 lower extremities",
            "regulatory_code": "IS 15298 / OSHA 1926.96",
            "corrective_remedy": "Mandate steel-toe, puncture-resistant soles with minimum 200J impact rating prior to site access."
        },
        {
            "id": "HAZ-004",
            "hazard_title": "Unsecured Materials near Scaffolding Frame",
            "category": "Housekeeping",
            "severity": "Medium",
            "location_in_image": "Lower staging ground",
            "regulatory_code": "OSHA 1926.250(a)",
            "corrective_remedy": "Stack and band loose shuttering components at designated material laydown areas at least 6 feet from edges."
        }
    ],
    "recommended_stop_work_notice": False
}

def analyze_site_safety(client: GeminiPlatformClient, image_bytes: bytes) -> Tuple[Dict[str, Any], bool, str]:
    """
    Run multimodal safety inspection using Gemini with fallback.
    """
    return client.analyze_multimodal(
        image_bytes=image_bytes,
        prompt=PPE_AUDIT_PROMPT,
        system_instruction=PPE_SYSTEM_INSTRUCTION,
        fallback_data=DEMO_SAFETY_AUDIT_RESULT
    )
