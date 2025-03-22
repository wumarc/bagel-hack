"""
Helper script to run the Streamlit application and guide through test scenarios.
"""

import subprocess
import os
import time
import sys
import webbrowser

def print_separator():
    print("\n" + "=" * 80 + "\n")

def print_test_instructions(test_name, steps):
    print_separator()
    print(f"TEST SCENARIO: {test_name}")
    print_separator()
    
    for i, step in enumerate(steps, 1):
        print(f"Step {i}: {step}")
    
    print_separator()
    input("Press Enter to continue...")

def main():
    # Check if Cohere API key is set
    if "COHERE_API_KEY" not in os.environ and not os.path.exists(".env"):
        print("WARNING: Cohere API key not found!")
        api_key = input("Please enter your Cohere API key to continue: ")
        
        with open(".env", "w") as f:
            f.write(f"COHERE_API_KEY={api_key}")
        
        print("API key saved to .env file.")
    
    # Instructions for running the tests
    print_separator()
    print("NETWORKING EVENT CHATBOT TEST SUITE")
    print_separator()
    print("This script will guide you through testing the chatbot with different scenarios.")
    print("The Streamlit application will open in your browser.")
    print_separator()
    
    # Ideal Flow Test Instructions
    ideal_flow_steps = [
        "When asked about your profession, enter: 'I'm a software engineer specializing in backend development'",
        "When asked about years of experience, enter: '5 years'",
        "When asked about interests, enter: 'Cloud computing, distributed systems, and database optimization'",
        "When asked about skills, enter: 'Leadership and project management'",
        "When asked about event type, enter: 'Conference'",
        "When asked about industry, enter: 'Technology'",
        "When asked about location, enter: 'San Francisco'",
        "When asked about format, enter: 'In-person'",
        "When asked about size, enter: 'Large'",
        "Verify that the JSON output contains all the information you provided"
    ]
    
    print_test_instructions("Ideal Flow Test", ideal_flow_steps)
    
    # Irrelevant Input Test Instructions
    irrelevant_input_steps = [
        "Refresh the page to restart the conversation",
        "When asked about your profession, enter: 'What's the weather like today?'",
        "Verify that the chatbot politely redirects you to the task",
        "Provide a valid profession answer to continue",
        "When asked about years of experience, enter: 'Let's skip this and move on'",
        "Verify that the chatbot insists on getting this information"
    ]
    
    print_test_instructions("Irrelevant Input Test", irrelevant_input_steps)
    
    # Vague Answer Test Instructions
    vague_answer_steps = [
        "Refresh the page to restart the conversation",
        "When asked about your profession, enter: 'I work with computers'",
        "Verify that the chatbot accepts this vague answer and continues",
        "Complete the rest of the conversation with valid answers"
    ]
    
    print_test_instructions("Vague Answer Test", vague_answer_steps)
    
    # Multiple Info Test Instructions
    multiple_info_steps = [
        "Refresh the page to restart the conversation",
        "When asked about your profession, enter: 'I'm a marketing manager with 10 years of experience in the technology sector'",
        "Verify how the chatbot handles multiple pieces of information at once",
        "Complete the rest of the conversation with valid answers"
    ]
    
    print_test_instructions("Multiple Info Test", multiple_info_steps)
    
    # Start the Streamlit application
    print_separator()
    print("Starting the Streamlit application...")
    print("After testing, press Ctrl+C in this terminal to exit.")
    print_separator()
    
    # Open the browser automatically
    time.sleep(2)
    webbrowser.open("http://localhost:8501")
    
    # Run the Streamlit application
    try:
        subprocess.run(["streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\nTest session ended.")
    except Exception as e:
        print(f"\nError starting Streamlit: {e}")
        print("Make sure you have installed all requirements with 'pip install -r requirements.txt'")

if __name__ == "__main__":
    main() 