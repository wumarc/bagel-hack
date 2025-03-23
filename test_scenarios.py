"""
Test scenarios for the Networking Event Chatbot.

This script contains example inputs and expected outputs to manually test
the chatbot's functionality.
"""

# Ideal Flow Test Scenario
ideal_flow = [
    {
        "question": "I'd like to help you find the perfect networking event. Could you tell me about your profession and industry?",
        "user_response": "I'm a software engineer specializing in backend development",
        "expected_next_question": "Great! How many years of experience do you have in this field?"
    },
    {
        "question": "Great! How many years of experience do you have in this field?",
        "user_response": "5 years",
        "expected_next_question": "Thanks! What are your main professional interests or areas you're passionate about?"
    },
    {
        "question": "Thanks! What are your main professional interests or areas you're passionate about?",
        "user_response": "Cloud computing, distributed systems, and database optimization",
        "expected_next_question": "What skills are you hoping to develop through networking?"
    },
    {
        "question": "What skills are you hoping to develop through networking?",
        "user_response": "Leadership and project management",
        "expected_next_question": "Now let's talk about what kind of networking event you're looking for. What type of event interests you (conference, workshop, meetup, etc.)?"
    },
    {
        "question": "Now let's talk about what kind of networking event you're looking for. What type of event interests you (conference, workshop, meetup, etc.)?",
        "user_response": "Conference",
        "expected_next_question": "Which industry or sector should the event focus on?"
    },
    {
        "question": "Which industry or sector should the event focus on?",
        "user_response": "Technology",
        "expected_next_question": "Do you have a preferred location for the event?"
    },
    {
        "question": "Do you have a preferred location for the event?",
        "user_response": "San Francisco",
        "expected_next_question": "What format do you prefer (in-person, virtual, hybrid)?"
    },
    {
        "question": "What format do you prefer (in-person, virtual, hybrid)?",
        "user_response": "In-person",
        "expected_next_question": "Finally, what size of event do you prefer (small, medium, large)?"
    },
    {
        "question": "Finally, what size of event do you prefer (small, medium, large)?",
        "user_response": "Large",
        "expected_next_question": "Thank you for providing all the information! Here's a summary of your preferences:"
    }
]

# Expected JSON output for ideal flow
expected_json_output = {
    "professional_profile": {
        "profession": "I'm a software engineer specializing in backend development",
        "years_experience": "5 years",
        "interests": "Cloud computing, distributed systems, and database optimization",
        "skills_to_develop": "Leadership and project management"
    },
    "event_preferences": {
        "type": "Conference",
        "industry": "Technology",
        "location": "San Francisco",
        "format": "In-person",
        "size": "Large"
    },
    "request": "Please recommend networking events that match these preferences."
}

# Irrelevant Input Test Scenario
irrelevant_input_test = [
    {
        "question": "I'd like to help you find the perfect networking event. Could you tell me about your profession and industry?",
        "user_response": "What's the weather like today?",
        "expected_redirection": True
    },
    {
        "question": "Great! How many years of experience do you have in this field?",
        "user_response": "Let's skip this and move on",
        "expected_redirection": True
    }
]

# Edge Case Test Scenario - Vague Answer
vague_answer_test = {
    "question": "I'd like to help you find the perfect networking event. Could you tell me about your profession and industry?",
    "user_response": "I work with computers",
    "should_accept": True
}

# Edge Case Test Scenario - Multiple Info at Once
multiple_info_test = {
    "question": "I'd like to help you find the perfect networking event. Could you tell me about your profession and industry?",
    "user_response": "I'm a marketing manager with 10 years of experience in the technology sector",
    "should_process": True
}

print("Test scenarios ready for manual verification")
print("Run the application with 'streamlit run app.py' and use these sample inputs to test")