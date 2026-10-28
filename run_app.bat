@echo off
title Multimodal Construction Intelligence Platform
cd /d "%~dp0"
echo ============================================================
echo Starting Multimodal Construction Intelligence Platform...
echo ============================================================
python -m streamlit run app.py
pause
