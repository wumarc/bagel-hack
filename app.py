import streamlit as st
import cohere
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Cohere client
api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(api_key)

# App title and description
st.title("Networking Event Recommendation Chatbot")
st.markdown("I'll help you find the perfect networking event by understanding your professional profile and preferences.")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_state" not in st.session_state:
    st.session_state.current_state = "initial"

if "user_data" not in st.session_state:
    st.session_state.user_data = {
        "profile": {},
        "event_preferences": {}
    }

if "generated_prompt" not in st.session_state:
    st.session_state.generated_prompt = None

# Define the system prompt for Cohere
def get_system_prompt():
    return """You are a helpful assistant designed to collect information about users for networking event recommendations. 
    
Your goal is to gather the following information in a conversational way:

1. Professional Profile:
   - Profession/industry
   - Years of experience
   - Professional interests
   - Skills they want to develop

2. Event Preferences:
   - Event type (conference, workshop, meetup, etc.)
   - Industry focus
   - Preferred location
   - Format (in-person, virtual, hybrid)
   - Size preference (small, medium, large)

Follow these rules:
- Keep responses concise and friendly
- Ask one question at a time
- If the user provides information not relevant to the task, politely redirect them
- When all required information is collected, summarize it and end the conversation
- Do not make recommendations - your job is only to collect information

Example conversation flow:
User: Hi there!
Assistant: Hello! I'd like to help you find the perfect networking event. Could you tell me about your profession and industry?

User: I'm a software engineer in the healthcare technology sector.
Assistant: Great! How many years of experience do you have in this field?

User: About 5 years.
Assistant: Thanks! What are your main professional interests or areas you're passionate about?

User: I'm mostly interested in AI and machine learning.
Assistant: Excellent! What skills are you hoping to develop through networking?

User: I want to improve my project management skills.
Assistant: I understand. Now let's talk about what kind of networking event you're looking for. What type of event interests you (conference, workshop, meetup, etc.)?

User: I prefer workshops.
Assistant: Workshops are great for hands-on learning. Do you have a preferred location?

If the user asks an unrelated question:
User: What's the weather like today?
Assistant: I'm focused on helping you find networking opportunities. To do that, I need to understand your preferences better. Could we return to discussing your professional background?

CURRENT STATE: {current_state}
CURRENT USER DATA: {user_data}
"""

# Define the states and questions for each state
states = {
    "initial": {
        "question": "I'd like to help you find the perfect networking event. Could you tell me about your profession and industry?",
        "next_state": "years_experience",
        "data_key": ("profile", "profession")
    },
    "years_experience": {
        "question": "Great! How many years of experience do you have in this field?",
        "next_state": "professional_interests",
        "data_key": ("profile", "years_experience")
    },
    "professional_interests": {
        "question": "Thanks! What are your main professional interests or areas you're passionate about?",
        "next_state": "skills_to_develop",
        "data_key": ("profile", "interests")
    },
    "skills_to_develop": {
        "question": "What skills are you hoping to develop through networking?",
        "next_state": "event_type",
        "data_key": ("profile", "skills_to_develop")
    },
    "event_type": {
        "question": "Now let's talk about what kind of networking event you're looking for. What type of event interests you (conference, workshop, meetup, etc.)?",
        "next_state": "industry_focus",
        "data_key": ("event_preferences", "type")
    },
    "industry_focus": {
        "question": "Which industry or sector should the event focus on?",
        "next_state": "location",
        "data_key": ("event_preferences", "industry")
    },
    "location": {
        "question": "Do you have a preferred location for the event?",
        "next_state": "format",
        "data_key": ("event_preferences", "location")
    },
    "format": {
        "question": "What format do you prefer (in-person, virtual, hybrid)?",
        "next_state": "size",
        "data_key": ("event_preferences", "format")
    },
    "size": {
        "question": "Finally, what size of event do you prefer (small, medium, large)?",
        "next_state": "completed",
        "data_key": ("event_preferences", "size")
    },
    "completed": {
        "question": "Thank you for providing all the information! Here's a summary of your preferences:",
        "next_state": None,
        "data_key": None
    }
}

# Function to update user data
def update_user_data(state, user_input):
    if state in states and states[state]["data_key"] is not None:
        main_key, sub_key = states[state]["data_key"]
        st.session_state.user_data[main_key][sub_key] = user_input

# Function to get next state
def get_next_state(current_state):
    if current_state in states:
        return states[current_state]["next_state"]
    return None

# Function to generate prompt for recommendations
def generate_recommendation_prompt():
    user_data = st.session_state.user_data
    prompt = {
        "professional_profile": user_data["profile"],
        "event_preferences": user_data["event_preferences"],
        "request": "Please recommend networking events that match these preferences."
    }
    return json.dumps(prompt, indent=2)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Initial bot message
if not st.session_state.messages:
    initial_question = states["initial"]["question"]
    st.session_state.messages.append({"role": "assistant", "content": initial_question})
    with st.chat_message("assistant"):
        st.markdown(initial_question)

# Handle user input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Update user data based on current state
    if st.session_state.current_state != "completed":
        update_user_data(st.session_state.current_state, prompt)
    
    # Generate response using Cohere
    current_state = st.session_state.current_state
    user_data = st.session_state.user_data
    
    if current_state == "completed":
        # If all information is collected, generate the final prompt
        if st.session_state.generated_prompt is None:
            st.session_state.generated_prompt = generate_recommendation_prompt()
        
        # Display the generated prompt
        response_content = "Here's the structured prompt with your preferences that can be used for recommendations:\n\n```json\n" + st.session_state.generated_prompt + "\n```"
    else:
        # Get response from Cohere
        response = co.chat(
            message=prompt,
            preamble=get_system_prompt().format(current_state=current_state, user_data=user_data),
            conversation_id=None
        )
        
        response_content = response.text
        
        # Move to next state based on predefined flow
        next_state = get_next_state(current_state)
        if next_state:
            st.session_state.current_state = next_state
            
            # If moving to completed state, generate the final prompt
            if next_state == "completed":
                st.session_state.generated_prompt = generate_recommendation_prompt()
                response_content += "\n\nHere's a summary of your preferences:\n\n```json\n" + st.session_state.generated_prompt + "\n```"
            else:
                # Add the next question
                response_content += "\n\n" + states[next_state]["question"]
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_content})
    with st.chat_message("assistant"):
        st.markdown(response_content)

# Display current state and collected data in sidebar for debugging
with st.sidebar:
    st.header("Debugging Information")
    st.subheader("Current State")
    st.write(st.session_state.current_state)
    
    st.subheader("Collected Data")
    st.json(st.session_state.user_data)
    
    if st.session_state.generated_prompt:
        st.subheader("Generated Prompt")
        st.json(json.loads(st.session_state.generated_prompt)) 