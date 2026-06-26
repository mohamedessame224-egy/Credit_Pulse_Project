@echo off
title Credit Pulse - منصة استبيانات قطاع الائتمان
color 0A
echo.
echo ============================================================
echo   Credit Pulse - National Bank of Egypt
echo   منصة استبيانات قطاع الائتمان - البنك الاهلي المصري
echo ============================================================
echo.
echo   Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org
    pause
    exit
)
echo.
echo   Installing required packages...
pip install -r requirements.txt --quiet
echo.
echo   Starting Credit Pulse...
echo   Opening browser at http://127.0.0.1:5000
echo.
python run.py
pause
