@echo off
echo Starting Proactive Networking Web Interface...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH. Please install Python and try again.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv\ (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Failed to create virtual environment. Please check your Python installation.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements if needed
if not exist venv\Lib\site-packages\cohere\ (
    echo Installing requirements...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Failed to install requirements. Please check your internet connection.
        pause
        exit /b 1
    )
)

REM Launch the web interface
echo Launching networking assistant...
python web_interface.py

REM If the script returns, wait for user input before closing
pause 