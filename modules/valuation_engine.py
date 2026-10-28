"""
Epic 3: Project Planning & Real Estate Valuation Engine.
Financial modeling in INR (Lakhs/Crores), empirical material metrics (Cement, Steel),
and Pollinations AI 3D architectural rendering integration.
"""
from typing import Dict, Any
import urllib.parse

# Indian Construction Cost Benchmarks (INR / sqft built-up area)
STRUCTURE_BENCHMARKS = {
    "Residential High-Rise (G+15)": {
        "Tier 1 (Mumbai, Delhi-NCR, Bengaluru)": {"cost_sqft": 3100, "market_sale_sqft": 11500},
        "Tier 2 (Pune, Hyderabad, Ahmedabad, Chennai)": {"cost_sqft": 2450, "market_sale_sqft": 6800},
        "Tier 3 (Emerging Urban & Industrial Hubs)": {"cost_sqft": 1950, "market_sale_sqft": 4200},
        "steel_kg_sqft": 4.2,
        "cement_bags_sqft": 0.42,
        "sand_cft_sqft": 1.75,
        "labor_mandays_sqft": 0.95
    },
    "Commercial Complex / Tech Park": {
        "Tier 1 (Mumbai, Delhi-NCR, Bengaluru)": {"cost_sqft": 3800, "market_sale_sqft": 15000},
        "Tier 2 (Pune, Hyderabad, Ahmedabad, Chennai)": {"cost_sqft": 3100, "market_sale_sqft": 9200},
        "Tier 3 (Emerging Urban & Industrial Hubs)": {"cost_sqft": 2500, "market_sale_sqft": 5800},
        "steel_kg_sqft": 4.8,
        "cement_bags_sqft": 0.45,
        "sand_cft_sqft": 1.9,
        "labor_mandays_sqft": 1.15
    },
    "Industrial Pre-Engineered Warehouse": {
        "Tier 1 (Mumbai, Delhi-NCR, Bengaluru)": {"cost_sqft": 2100, "market_sale_sqft": 6200},
        "Tier 2 (Pune, Hyderabad, Ahmedabad, Chennai)": {"cost_sqft": 1750, "market_sale_sqft": 4500},
        "Tier 3 (Emerging Urban & Industrial Hubs)": {"cost_sqft": 1400, "market_sale_sqft": 3100},
        "steel_kg_sqft": 6.5, # PEB portal frames
        "cement_bags_sqft": 0.28,
        "sand_cft_sqft": 1.2,
        "labor_mandays_sqft": 0.6
    },
    "Luxury Gated Villa Development": {
        "Tier 1 (Mumbai, Delhi-NCR, Bengaluru)": {"cost_sqft": 4600, "market_sale_sqft": 18500},
        "Tier 2 (Pune, Hyderabad, Ahmedabad, Chennai)": {"cost_sqft": 3600, "market_sale_sqft": 11000},
        "Tier 3 (Emerging Urban & Industrial Hubs)": {"cost_sqft": 2800, "market_sale_sqft": 6900},
        "steel_kg_sqft": 3.8,
        "cement_bags_sqft": 0.40,
        "sand_cft_sqft": 1.8,
        "labor_mandays_sqft": 1.3
    },
    "Affordable Housing Society (PMAY)": {
        "Tier 1 (Mumbai, Delhi-NCR, Bengaluru)": {"cost_sqft": 2200, "market_sale_sqft": 5800},
        "Tier 2 (Pune, Hyderabad, Ahmedabad, Chennai)": {"cost_sqft": 1750, "market_sale_sqft": 3900},
        "Tier 3 (Emerging Urban & Industrial Hubs)": {"cost_sqft": 1450, "market_sale_sqft": 2800},
        "steel_kg_sqft": 3.6,
        "cement_bags_sqft": 0.38,
        "sand_cft_sqft": 1.6,
        "labor_mandays_sqft": 0.85
    }
}

def format_inr(amount: float) -> str:
    """Format numeric values into standard Indian Lakhs / Crores string."""
    if amount >= 10000000: # 1 Crore = 10,000,000
        crores = amount / 10000000
        return f"₹ {crores:.2f} Cr"
    elif amount >= 100000: # 1 Lakh = 100,000
        lakhs = amount / 100000
        return f"₹ {lakhs:.2f} L"
    else:
        return f"₹ {amount:,.0f}"

def format_full_inr(amount: float) -> str:
    """Format full rupee value with commas."""
    return f"₹ {amount:,.0f}"

def calculate_construction_finances(
    structure_type: str,
    location_tier: str,
    built_up_sqft: float,
    completion_percentage: float
) -> Dict[str, Any]:
    """
    Calculate project budget, CapEx incurred, current asset valuation,
    and material requirements according to Indian civil standards.
    """
    profile = STRUCTURE_BENCHMARKS.get(
        structure_type,
        STRUCTURE_BENCHMARKS["Residential High-Rise (G+15)"]
    )
    tier_rates = profile.get(location_tier, profile["Tier 1 (Mumbai, Delhi-NCR, Bengaluru)"])

    cost_per_sqft = tier_rates["cost_sqft"]
    market_sale_sqft = tier_rates["market_sale_sqft"]

    # Total Project Construction Cost (CapEx Budget)
    total_project_budget = built_up_sqft * cost_per_sqft

    # Capital Expenditure Incurred to Date
    completion_ratio = max(0.0, min(100.0, completion_percentage)) / 100.0
    capex_incurred = total_project_budget * completion_ratio

    # Current Market Asset Valuation:
    # A partially constructed property holds land + built value minus completion risk discount.
    # At 0%, land/approvals hold ~35% of completed market value.
    # At 100%, commands 100% of finished market rate.
    valuation_factor = 0.35 + (0.65 * completion_ratio)
    completed_market_value = built_up_sqft * market_sale_sqft
    current_asset_valuation = completed_market_value * valuation_factor

    # Projected Gross Development Value (GDV) / Profit Margin
    potential_gross_margin = completed_market_value - total_project_budget
    margin_percentage = (potential_gross_margin / completed_market_value) * 100.0 if completed_market_value > 0 else 0

    # Material Estimations (Total project requirements)
    total_steel_kg = built_up_sqft * profile["steel_kg_sqft"]
    total_steel_tonnes = total_steel_kg / 1000.0
    steel_consumed_tonnes = total_steel_tonnes * completion_ratio

    total_cement_bags = built_up_sqft * profile["cement_bags_sqft"]
    cement_consumed_bags = total_cement_bags * completion_ratio

    total_sand_cft = built_up_sqft * profile["sand_cft_sqft"]
    total_labor_mandays = built_up_sqft * profile["labor_mandays_sqft"]

    # Milestone categorization
    if completion_percentage < 25:
        current_milestone = "Foundation, Excavation & Substructure"
        next_milestone = "RCC Superstructure Framing"
        milestone_color = "#3498DB"
    elif completion_percentage < 60:
        current_milestone = "RCC Superstructure Framing & Slabs"
        next_milestone = "Masonry, Partitioning & MEP Services"
        milestone_color = "#F39C12"
    elif completion_percentage < 85:
        current_milestone = "Brickwork, Plastering, Electrical & Plumbing"
        next_milestone = "Architectural Finishing, Glazing & Landscaping"
        milestone_color = "#9B59B6"
    elif completion_percentage < 100:
        current_milestone = "Final Finishes, Fixtures & Snag Resolution"
        next_milestone = "Occupancy Certificate (OC) & Handover"
        milestone_color = "#2ECC71"
    else:
        current_milestone = "Project Handed Over & Occupancy Certified (100%)"
        next_milestone = "Post-Occupancy Facility Management"
        milestone_color = "#1ABC9C"

    return {
        "structure_type": structure_type,
        "location_tier": location_tier,
        "built_up_sqft": built_up_sqft,
        "completion_percentage": completion_percentage,
        "cost_per_sqft": cost_per_sqft,
        "market_sale_sqft": market_sale_sqft,
        "total_project_budget": total_project_budget,
        "total_project_budget_fmt": format_inr(total_project_budget),
        "capex_incurred": capex_incurred,
        "capex_incurred_fmt": format_inr(capex_incurred),
        "current_asset_valuation": current_asset_valuation,
        "current_asset_valuation_fmt": format_inr(current_asset_valuation),
        "completed_market_value": completed_market_value,
        "completed_market_value_fmt": format_inr(completed_market_value),
        "potential_gross_margin": potential_gross_margin,
        "potential_gross_margin_fmt": format_inr(potential_gross_margin),
        "margin_percentage": margin_percentage,
        "materials": {
            "total_steel_tonnes": total_steel_tonnes,
            "steel_consumed_tonnes": steel_consumed_tonnes,
            "total_cement_bags": total_cement_bags,
            "cement_consumed_bags": cement_consumed_bags,
            "total_sand_cft": total_sand_cft,
            "total_labor_mandays": total_labor_mandays
        },
        "milestone": {
            "current": current_milestone,
            "next": next_milestone,
            "color": milestone_color
        }
    }

def generate_architectural_render_url(
    structure_type: str,
    location_tier: str,
    completion_percentage: float
) -> Tuple[str, str]:
    """
    Generate dynamic prompt and Pollinations AI rendering URL.
    Returns: (image_url, generated_prompt)
    """
    phase_descriptions = {
        (0, 25): "under active construction, foundation pit, mobile cranes, reinforced concrete rebar cage columns, deep excavation",
        (25, 60): "halfway constructed, active tower crane, exposed cast concrete floors and structural pillars, safety netting, blue sky daylight",
        (60, 85): "late construction stage, curtain wall glass facade partially installed, exterior scaffolding, modern architecture",
        (85, 101): "fully completed, magnificent modern architectural masterpiece, reflective glass facade, lush landscaping, dramatic architectural lighting"
    }

    phase_text = "active construction site"
    for (low, high), desc in phase_descriptions.items():
        if low <= completion_percentage < high:
            phase_text = desc
            break
        elif completion_percentage >= 100:
            phase_text = phase_descriptions[(85, 101)]

    clean_tier = location_tier.split("(")[0].strip()

    prompt = (
        f"3D architectural visualization of a luxurious {structure_type} in {clean_tier} India, "
        f"{phase_text}, ultra photorealistic, architectural digest award winning design, "
        f"octane render, 8k resolution, cinematic golden hour lighting, civil engineering perspective"
    )

    encoded_prompt = urllib.parse.quote(prompt)
    # Pollinations AI direct image endpoint with seed for deterministic crisp renders
    seed = int(completion_percentage * 17) + 42
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=600&seed={seed}&nologo=true"

    return url, prompt
