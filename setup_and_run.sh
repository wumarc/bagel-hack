#!/bin/bash

# Networking Event Chatbot Setup and Run Script

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Create and activate virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment based on OS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Check if .env file exists and has Cohere API key
if [ ! -f .env ] || ! grep -q "COHERE_API_KEY" .env; then
    echo "Cohere API key not found."
    echo "Please enter your Cohere API key:"
    read api_key
    echo "COHERE_API_KEY=$api_key" > .env
    echo "API key saved to .env file."
fi

# Run the application
echo "Starting the application..."
python -m streamlit run app.py 