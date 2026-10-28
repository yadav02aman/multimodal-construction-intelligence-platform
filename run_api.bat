@echo off
title Multimodal Construction Platform - FastAPI Backend
cd /d "%~dp0"
echo ============================================================
echo Starting FastAPI Backend (Swagger UI at http://localhost:8000/docs)
echo ============================================================
python -m uvicorn api:app --reload --port 8000
pause
