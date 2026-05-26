@echo off
title CivicPulse v2.0 - Telangana Civic Management
color 0A
echo.
echo  ===================================================
echo   CivicPulse v2.0 - Starting...
echo  ===================================================
echo.
echo  Installing dependencies...
pip install -r requirements.txt -q
echo  Done.
echo.
echo  Starting server at http://localhost:5000
echo  Browser will open automatically...
echo.
python app.py
pause
