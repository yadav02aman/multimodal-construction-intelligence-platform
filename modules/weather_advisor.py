"""
Epic 5: Weather-Aware Advisory & Daily Site Protocols.
Dynamic safety alerts, critical stop-work conditions, and IS 456 / OSHA mitigation protocols.
"""
from typing import Dict, Any, List

WEATHER_PROTOCOLS: Dict[str, Dict[str, Any]] = {
    "High Wind (>45 km/h / Beaufort Scale 6+)": {
        "status_level": "WARNING / CRITICAL SAFETY LEVEL 3",
        "badge_color": "#E74C3C",
        "icon": "🌪️",
        "summary": "Hazardous aerodynamic wind gusts detected. Extreme tipping risk for vertical hoisting and elevated work platforms.",
        "mandatory_action": "MANDATORY SUSPENSION OF CRANE HOISTING & WORK AT HEIGHT (>3M)",
        "protocols": [
            {
                "category": "Tower & Mobile Cranes",
                "mandate": "Immediately cease crane slewing and lifting operations. Release the slewing brake to place crane in free 'weather-vaning' mode to prevent mast buckling.",
                "code": "OSHA 1926.1431 / IS 4573"
            },
            {
                "category": "Scaffolding & Edge Protection",
                "mandate": "Evacuate external suspended cradles and scaffolding decks above 3 meters. Double-check all tie-backs and tie down loose plywood shuttering and corrugated sheet stacks.",
                "code": "IS 3696 Part 1 & 2 / OSHA 1926.451"
            },
            {
                "category": "Roofing & Cladding",
                "mandate": "Prohibit handling of large-surface ACP panels, glass glazing units, and perimeter formwork shutters.",
                "code": "IS 875 (Part 3) Wind Loads"
            }
        ],
        "concrete_advisory": "High wind velocities accelerate surface evaporation from fresh concrete decks, causing severe plastic shrinkage cracking. Apply aliphatic alcohol evaporation retarders and immediate polythene sheeting if placing concrete cannot be deferred."
    },
    "Heavy Rain & Monsoon Storm": {
        "status_level": "CAUTION / ELECTRICAL & TRENCHING RISK",
        "badge_color": "#2980B9",
        "icon": "🌧️",
        "summary": "Precipitation leading to waterlogging, subgrade saturation, mud slips, and increased ground fault electrical risk.",
        "mandatory_action": "LOCKOUT ELECTRICAL DISTRIBUTION BOARDS & DEWATER EXCAVATIONS",
        "protocols": [
            {
                "category": "Deep Excavation & Shoring",
                "mandate": "Inspect foundation trenches and sheet piles for hydrostatic pressure accumulation or slope washouts. Maintain 24/7 sump dewatering pumps with backup diesel generators.",
                "code": "IS 3764 (Safety Code for Excavation)"
            },
            {
                "category": "Electrical Safety",
                "mandate": "De-energize non-essential site DBs. Elevate cables off muddy pooling ground. Verify Residual Current Circuit Breakers (RCCB/GFCI <=30mA) trip testing.",
                "code": "IS 732 / OSHA 1926.404"
            },
            {
                "category": "Concrete Pouring Halt",
                "mandate": "Strictly halt unshielded casting of slabs and beams. Rainwater alters water-cement ratio (W/C), catastrophically diluting compressive strength.",
                "code": "IS 456:2000 Clause 13.1"
            }
        ],
        "concrete_advisory": "Cover recently poured slabs (<8 hours old) with waterproof tarpaulins. Never sprinkle dry cement powder over rain-damaged wet surfaces as it creates weak laitance and surface flaking."
    },
    "Extreme Heat (>40°C / Heat Index High)": {
        "status_level": "ADVISORY / HYDRATION & CONCRETE CURING PROTOCOL",
        "badge_color": "#D35400",
        "icon": "☀️",
        "summary": "High ambient temperature leading to rapid hydration, flash setting of concrete, and heat exhaustion among workers.",
        "mandatory_action": "MANDATORY WET BURLAP CURING & WORKER ROTATION REST PROTOCOL",
        "protocols": [
            {
                "category": "Worker Physiology",
                "mandate": "Implement mandatory 15-minute rest breaks every hour between 11:30 AM and 3:30 PM. Provide shaded rest sheds equipped with chilled electrolyte/ORS water stations.",
                "code": "OSHA Safety and Health Regulations / Factories Act"
            },
            {
                "category": "Concrete Batching & Placement",
                "mandate": "Schedule major structural pours during night shifts or early morning hours (4 AM - 8 AM). Chilled water or crushed ice substitution must be used in the batching plant to maintain fresh concrete temperature below 32°C.",
                "code": "IS 456 Cl 14.2 & ACI 305R (Hot Weather Concreting)"
            },
            {
                "category": "Continuous Wet Curing",
                "mandate": "Initiate ponding or continuous saturated burlap curing as soon as the concrete has hardened sufficiently, maintaining moist cover for minimum 14 days (10 days for OPC).",
                "code": "IS 456:2000 Clause 13.5"
            }
        ],
        "concrete_advisory": "High evaporation triggers rapid slump loss. Never add unmetered water on site to restore workability; use polycarboxylate ether (PCE) based superplasticizers (IS 9103) instead."
    },
    "Dense Fog / Low Visibility (<200m)": {
        "status_level": "ADVISORY / VISUAL TRAFFIC & ILLUMINATION PROTOCOL",
        "badge_color": "#7F8C8D",
        "icon": "🌫️",
        "summary": "Impaired visual range creating severe vehicle collision, blind-spot, and height-fall hazards during transit.",
        "mandatory_action": "ILLUMINATION BOOST TO >150 LUX & DEDICATED MARSHALLING",
        "protocols": [
            {
                "category": "Site Logistics & Heavy Transit",
                "mandate": "Transit mixer and tipper movement restricted to maximum 10 km/h with hazard blinkers active. Dedicated banksmen with luminous batons required for reversing.",
                "code": "IS 13415 / OSHA 1926.601"
            },
            {
                "category": "Task Lighting",
                "mandate": "Power on high-intensity floodlighting towers across active working decks and stairwells to meet minimum 150 lux illumination.",
                "code": "IS 3646 (Code of Practice for Interior & Site Illumination)"
            },
            {
                "category": "Worker PPE",
                "mandate": "Every individual on site must wear EN ISO 20471 / IS 15809 Class 3 high-visibility jackets with 360-degree reflective prismatic tape.",
                "code": "IS 15809:2017"
            }
        ],
        "concrete_advisory": "Cold fog retards concrete setting times. De-shuttering schedules must be adjusted based on field-cured cube compressive strength tests rather than standard calendar days."
    },
    "Normal / Favorable Conditions": {
        "status_level": "OPTIMAL / STANDARD OPERATING CONDITIONS",
        "badge_color": "#27AE60",
        "icon": "🌤️",
        "summary": "Weather parameters are within normal design margins. Maximum productivity shift authorized.",
        "mandatory_action": "EXECUTE SCHEDULED DAILY TARGETS & ROUTINE AUDITS",
        "protocols": [
            {
                "category": "Daily Shift Pre-Start",
                "mandate": "Conduct 10-minute morning toolbox talk (TBT) focusing on task-specific hazards (scaffold tagging, rebar cap inspection).",
                "code": "ISO 45001 / OSHA 1926.21"
            },
            {
                "category": "Routine Plant Inspection",
                "mandate": "Verify wire rope hoist lubrication, tower crane limit switches, and concrete pump pipeline couplings.",
                "code": "IS 13367 (Safe Use of Cranes)"
            },
            {
                "category": "Standard Curing Regimen",
                "mandate": "Maintain regular twice-daily spraying of cured concrete elements in compliance with IS 456.",
                "code": "IS 456 Clause 13.5"
            }
        ],
        "concrete_advisory": "Ambient temperature and relative humidity favor standard mix designs (M25, M30). Maintain standard water-cement ratio (0.45 - 0.50) without extra retarders."
    }
}

def get_weather_protocol(condition_name: str) -> Dict[str, Any]:
    """Retrieve full safety protocol for selected weather scenario."""
    return WEATHER_PROTOCOLS.get(
        condition_name,
        WEATHER_PROTOCOLS["Normal / Favorable Conditions"]
    )
