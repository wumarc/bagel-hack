# Networking Event Chatbot Documentation

## Overview

This chatbot collects user professional profiles and event preferences to generate a structured JSON prompt that can be used for networking event recommendations.

## Conversation Flow

The chatbot follows a structured conversation flow:

1. **Professional Profile Collection**:
   - Profession/industry
   - Years of experience
   - Professional interests
   - Skills to develop

2. **Event Preferences Collection**:
   - Event type (conference, workshop, meetup, etc.)
   - Industry focus
   - Preferred location
   - Format (in-person, virtual, hybrid)
   - Size preference (small, medium, large)

3. **Prompt Generation**:
   - After collecting all information, the chatbot generates a structured JSON prompt

## Usage

1. Start the application:
   ```
   streamlit run app.py
   ```

2. Interact with the chatbot by answering its questions.

3. After all information is collected, the chatbot will display a structured JSON prompt.

## Testing Scenarios

### Ideal Flow Testing

1. Provide clear answers to each question:
   - Profession: "I'm a software engineer specializing in backend development"
   - Experience: "5 years"
   - Interests: "Cloud computing, distributed systems, and database optimization"
   - Skills: "Leadership and project management"
   - Event type: "Conference"
   - Industry: "Technology"
   - Location: "San Francisco"
   - Format: "In-person"
   - Size: "Large"

2. Verify that the JSON prompt contains all provided information.

### Irrelevant Input Testing

1. Provide an off-topic response:
   - When asked about profession: "What's the weather like today?"
   - The chatbot should politely redirect to the task.

2. Try to skip questions:
   - Respond with: "Let's skip this and move on"
   - The chatbot should politely insist on getting the information.

### Edge Case Testing

1. Provide vague answers:
   - Profession: "I work with computers"
   - The chatbot should still process this response.

2. Provide multiple pieces of information at once:
   - "I'm a marketing manager with 10 years of experience"
   - The chatbot should process this information and may combine steps.

## JSON Output Structure

The final JSON prompt follows this structure:

```json
{
  "professional_profile": {
    "profession": "User's profession",
    "years_experience": "User's experience",
    "interests": "User's interests",
    "skills_to_develop": "Skills user wants to develop"
  },
  "event_preferences": {
    "type": "User's preferred event type",
    "industry": "User's preferred industry focus",
    "location": "User's preferred location",
    "format": "User's preferred format",
    "size": "User's preferred size"
  },
  "request": "Please recommend networking events that match these preferences."
} 