"""
FastAPI Backend Microservice.
Implements the architecture in Image 2:
- /api/v1/safety-audit (POST multipart image)
- /api/v1/crack-diagnostics (POST multipart image)
- /api/v1/valuation (POST project data)
- /api/v1/weather-advisory (GET weather protocols)
- /api/v1/chat (POST multi-turn assistant query)
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from modules.gemini_client import GeminiPlatformClient
from modules.safety_audit import analyze_site_safety
from modules.crack_diagnostics import analyze_crack_diagnostics
from modules.valuation_engine import calculate_construction_finances, generate_architectural_render_url
from modules.weather_advisor import get_weather_protocol, WEATHER_PROTOCOLS
from modules.chatbot import handle_chat_query

app = FastAPI(
    title="Multimodal Construction Intelligence Platform API",
    description="Decoupled FastAPI backend for PPE audits, concrete crack diagnostics, INR valuation, and weather advisory.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Schemas
class ValuationRequest(BaseModel):
    structure_type: str = Field(
        default="Residential High-Rise (G+15)",
        description="Type of construction structure"
    )
    location_tier: str = Field(
        default="Tier 1 (Mumbai, Delhi-NCR, Bengaluru)",
        description="Urban tier in India"
    )
    built_up_sqft: float = Field(
        default=45000,
        gt=0,
        description="Total built-up area in square feet"
    )
    completion_percentage: float = Field(
        default=45.0,
        ge=0,
        le=100,
        description="Current stage completion percentage"
    )

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    query: str
    history: Optional[List[ChatMessage]] = []
    gemini_api_key: Optional[str] = None

@app.get("/")
def root():
    return {
        "platform": "Multimodal Construction Intelligence Platform",
        "platform_id": "6ac4c98d1dcde6d7857c1642",
        "status": "operational",
        "docs": "/docs"
    }

@app.post("/api/v1/safety-audit")
async def safety_audit_endpoint(
    file: UploadFile = File(...),
    gemini_api_key: Optional[str] = Form(None)
):
    """Analyze site photo for worker PPE compliance and OSHA/IS hazards."""
    image_bytes = await file.read()
    client = GeminiPlatformClient(api_key=gemini_api_key)
    result, is_live, msg = analyze_site_safety(client, image_bytes)
    return {
        "is_live_gemini": is_live,
        "engine_message": msg,
        "audit_data": result
    }

@app.post("/api/v1/crack-diagnostics")
async def crack_diagnostics_endpoint(
    file: UploadFile = File(...),
    gemini_api_key: Optional[str] = Form(None)
):
    """Classify concrete defect and recommend engineering repair protocols."""
    image_bytes = await file.read()
    client = GeminiPlatformClient(api_key=gemini_api_key)
    result, is_live, msg = analyze_crack_diagnostics(client, image_bytes)
    return {
        "is_live_gemini": is_live,
        "engine_message": msg,
        "diagnostic_data": result
    }

@app.post("/api/v1/valuation")
def project_valuation_endpoint(req: ValuationRequest):
    """Calculate project budget, CapEx, INR valuation, material metrics, and 3D render URL."""
    finances = calculate_construction_finances(
        structure_type=req.structure_type,
        location_tier=req.location_tier,
        built_up_sqft=req.built_up_sqft,
        completion_percentage=req.completion_percentage
    )
    render_url, render_prompt = generate_architectural_render_url(
        structure_type=req.structure_type,
        location_tier=req.location_tier,
        completion_percentage=req.completion_percentage
    )
    return {
        "financial_ledger": finances,
        "architectural_3d_render": {
            "image_url": render_url,
            "prompt": render_prompt
        }
    }

@app.get("/api/v1/weather-advisories")
def weather_conditions_list():
    """List available weather condition scenarios and protocols."""
    return {
        "available_conditions": list(WEATHER_PROTOCOLS.keys()),
        "protocols": WEATHER_PROTOCOLS
    }

@app.get("/api/v1/weather-advisories/{condition_name}")
def weather_protocol_detail(condition_name: str):
    """Get active safety protocols for a specific weather condition."""
    if condition_name not in WEATHER_PROTOCOLS:
        raise HTTPException(status_code=404, detail="Weather condition not found")
    return get_weather_protocol(condition_name)

@app.post("/api/v1/chat")
def chat_assistant_endpoint(req: ChatRequest):
    """Multi-turn construction engineering assistant query."""
    client = GeminiPlatformClient(api_key=req.gemini_api_key)
    history_dicts = [{"role": m.role, "content": m.content} for m in req.history]
    reply, is_live = handle_chat_query(client, history_dicts, req.query)
    return {
        "is_live_gemini": is_live,
        "reply": reply
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
