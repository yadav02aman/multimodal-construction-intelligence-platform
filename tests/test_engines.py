"""
Unit test suite for Multimodal Construction Intelligence Platform.
Tests calculation accuracy, INR formatting, sample generation, and contract schemas.
"""
import io
from PIL import Image

from modules.valuation_engine import (
    calculate_construction_finances,
    format_inr,
    generate_architectural_render_url
)
from modules.weather_advisor import get_weather_protocol, WEATHER_PROTOCOLS
from modules.chatbot import fallback_chat_answer
from modules.safety_audit import DEMO_SAFETY_AUDIT_RESULT
from modules.crack_diagnostics import DEMO_CRACK_DIAGNOSTICS_RESULT
from modules.sample_data import generate_sample_ppe_image, generate_sample_crack_image

def test_inr_formatting():
    assert format_inr(15000000) == "₹ 1.50 Cr"
    assert format_inr(4500000) == "₹ 45.00 L"
    assert format_inr(50000) == "₹ 50,000"

def test_financial_calculations():
    res = calculate_construction_finances(
        structure_type="Residential High-Rise (G+15)",
        location_tier="Tier 1 (Mumbai, Delhi-NCR, Bengaluru)",
        built_up_sqft=10000,
        completion_percentage=50
    )
    # 10,000 sqft * 3100 = 31,000,000 (₹ 3.10 Cr)
    assert res["total_project_budget"] == 31000000.0
    assert res["total_project_budget_fmt"] == "₹ 3.10 Cr"
    # CapEx at 50% = 15,500,000 (₹ 1.55 Cr)
    assert res["capex_incurred"] == 15500000.0
    assert res["materials"]["total_cement_bags"] == 4200.0
    assert res["materials"]["total_steel_tonnes"] == 42.0

def test_render_url_generation():
    url, prompt = generate_architectural_render_url(
        structure_type="Commercial Complex / Tech Park",
        location_tier="Tier 1 (Mumbai, Delhi-NCR, Bengaluru)",
        completion_percentage=60
    )
    assert url.startswith("https://image.pollinations.ai/prompt/")
    assert "Commercial Complex" in prompt

def test_weather_protocols():
    for cond in WEATHER_PROTOCOLS.keys():
        p = get_weather_protocol(cond)
        assert "status_level" in p
        assert "mandatory_action" in p
        assert len(p["protocols"]) > 0

def test_sample_image_generators():
    ppe_bytes = generate_sample_ppe_image()
    assert isinstance(ppe_bytes, bytes)
    img1 = Image.open(io.BytesIO(ppe_bytes))
    assert img1.size == (800, 500)

    crack_bytes = generate_sample_crack_image()
    assert isinstance(crack_bytes, bytes)
    img2 = Image.open(io.BytesIO(crack_bytes))
    assert img2.size == (800, 500)

def test_demo_schemas():
    assert "safety_score" in DEMO_SAFETY_AUDIT_RESULT
    assert "identified_site_hazards" in DEMO_SAFETY_AUDIT_RESULT
    assert "defect_type" in DEMO_CRACK_DIAGNOSTICS_RESULT
    assert "recommended_engineering_repairs" in DEMO_CRACK_DIAGNOSTICS_RESULT

def test_chat_fallbacks():
    ans_curing = fallback_chat_answer("What is the curing period for OPC?")
    assert "IS 456" in ans_curing

    ans_shear = fallback_chat_answer("How to repair a shear crack?")
    assert "Epoxy" in ans_shear or "epoxy" in ans_shear
