@echo off
:: Networking Event Chatbot Setup and Run Script for Windows

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b 1
)

:: Create and activate virtual environment
echo Creating virtual environment...
python -m venv venv

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install requirements
echo Installing requirements...
pip install -r requirements.txt

:: Check if .env file exists and has Cohere API key
set NEED_API_KEY=0
if not exist .env (
    set NEED_API_KEY=1
) else (
    findstr /m "COHERE_API_KEY" .env >nul
    if %errorlevel% neq 0 (
        set NEED_API_KEY=1
    )
)

if %NEED_API_KEY% equ 1 (
    echo Cohere API key not found.
    echo Please enter your Cohere API key:
    set /p api_key=
    echo COHERE_API_KEY=%api_key%> .env
    echo API key saved to .env file.
)

:: Run the application
echo Starting the application...
python -m streamlit run app.py

pause 