"""
Epic 2: Crack Diagnostics & Structural Integrity Module.
Classification, engineering causes, repair methodologies compliant with IS 456 & ACI 224R.
"""
from typing import Dict, Any, Tuple
from .gemini_client import GeminiPlatformClient

CRACK_SYSTEM_INSTRUCTION = """
You are a Principal Structural Forensic Engineer specializing in Reinforced Cement Concrete (RCC) defect forensics.
Assess concrete crack images according to IS 456:2000 (Plain and Reinforced Concrete - Code of Practice) and ACI 224R (Control of Cracking in Concrete Structures).
Output strictly a valid JSON object matching the requested schema.
"""

CRACK_DIAGNOSTICS_PROMPT = """
Perform a detailed structural integrity inspection of the concrete/masonry defect in this image.
Classify the defect type strictly into one of:
["Hairline Crack", "Settlement Crack", "Structural Shear Crack", "Thermal Expansion Crack", "Spalling & Corrosion Defect"].

Output ONLY this strict JSON structure:
{
  "defect_type": "<Hairline Crack | Settlement Crack | Structural Shear Crack | Thermal Expansion Crack | Spalling & Corrosion Defect>",
  "estimated_crack_width_mm": <number e.g. 0.3 or 2.8>,
  "estimated_depth": "<Surface (<15mm) | Moderate (15-50mm) | Deep / Through-Slab>",
  "structural_risk_score": <integer 0 to 100>,
  "urgency_level": "<Low (Monitor) | Moderate (Remediate in 30 Days) | High (Immediate Action) | Critical / Emergency>",
  "structural_element": "<Beam | Column | Slab | Retaining Wall | Shear Wall | Foundation>",
  "root_causes": [
    "<Primary root cause description>",
    "<Secondary contributing factor>"
  ],
  "is_456_compliance_status": "<Within Permissible Limit (<0.3mm for mild exposure) | Exceeds Permissible Limit | Severe Structural Threat>",
  "recommended_engineering_repairs": [
    {
      "step": 1,
      "method": "<e.g. Surface V-Groove Routing & Cleaning>",
      "materials": "<e.g. Diamond blade grinder, compressed oil-free air>",
      "engineering_rationale": "<Why this step is necessary>"
    },
    {
      "step": 2,
      "method": "<e.g. Low-Viscosity Epoxy Pressure Injection / Polyurethane Grouting>",
      "materials": "<e.g. High-modulus moisture-insensitive epoxy resin (ASTM C881 Type I/IV)>",
      "engineering_rationale": "<Restores shear transfer and seals monolithic core against moisture ingress>"
    },
    {
      "step": 3,
      "method": "<e.g. Structural Carbon Fiber Wrap (CFRP) or Rebar Stitching>",
      "materials": "<e.g. Unidirectional CFRP fabric with epoxy saturant>",
      "engineering_rationale": "<Provides supplementary shear capacity where steel yielding occurred>"
    }
  ],
  "monitoring_protocol": "<Specific instrumentation: tell-tale crack monitor gauge, ultrasonic pulse velocity, or periodic photogrammetry>"
}
"""

DEMO_CRACK_DIAGNOSTICS_RESULT: Dict[str, Any] = {
    "defect_type": "Structural Shear Crack",
    "estimated_crack_width_mm": 2.8,
    "estimated_depth": "Deep / Through-Slab",
    "structural_risk_score": 82,
    "urgency_level": "High (Immediate Action)",
    "structural_element": "RCC Reinforced Beam",
    "root_causes": [
        "Diagonal tension shear stress exceeding concrete tensile capacity (IS 456 Cl 40.1)",
        "Potential yielding or insufficient spacing of secondary shear stirrups under localized dead/live load overload",
        "Micro-void carbonation accelerating rebar oxidation along the crack interface"
    ],
    "is_456_compliance_status": "Exceeds Permissible Limit (Permissible: 0.3mm; Actual: 2.8mm - 9.3x over design envelope)",
    "recommended_engineering_repairs": [
        {
            "step": 1,
            "method": "Structural Shoring & Dead Load Relief",
            "materials": "Adjustable hydraulic props & timber cribbing",
            "engineering_rationale": "Transfer live loads away from the distressed member prior to injection to allow crack closure under compression."
        },
        {
            "step": 2,
            "method": "V-Groove Sealing & Port Installation",
            "materials": "Quick-set epoxy paste surface sealant & conical injection entry ports",
            "engineering_rationale": "Creates a sealed chamber for pressurized deep chemical injection along the 45-degree shear trajectory."
        },
        {
            "step": 3,
            "method": "High-Pressure Low-Viscosity Epoxy Injection",
            "materials": "ASTM C881 Type I, Grade 1 structural epoxy resin (viscosity <200 cPs)",
            "engineering_rationale": "Re-bonds fractured concrete facets, restoring 95%+ of original uncracked compressive and shear capacity."
        },
        {
            "step": 4,
            "method": "Carbon Fiber Reinforced Polymer (CFRP) Strengthening",
            "materials": "Bidirectional 300 gsm carbon fiber fabric with structural epoxy adhesive",
            "engineering_rationale": "External post-tensioning shear jacket to compensate for internal stirrup deficiency."
        }
    ],
    "monitoring_protocol": "Install calibrated mechanical Tell-Tale Crack Gauge (accuracy ±0.1mm) with bi-weekly laser logging for 90 days post-cure."
}

def analyze_crack_diagnostics(client: GeminiPlatformClient, image_bytes: bytes) -> Tuple[Dict[str, Any], bool, str]:
    """
    Run multimodal crack classification and structural diagnosis.
    """
    return client.analyze_multimodal(
        image_bytes=image_bytes,
        prompt=CRACK_DIAGNOSTICS_PROMPT,
        system_instruction=CRACK_SYSTEM_INSTRUCTION,
        fallback_data=DEMO_CRACK_DIAGNOSTICS_RESULT
    )
