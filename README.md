# Proactive Networking

A conversational agent using Cohere API to help users find the best networking events based on their professional interests and preferences.

## Setup

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Add your Cohere API key to the `.env` file:
```
COHERE_API_KEY=your_api_key_here
```

3. Run the application in one of two ways:

   a. Standard Streamlit interface:
   ```
   streamlit run app.py
   ```

   b. Custom web interface with chat button:
   ```
   python web_interface.py
   ```

## Features

- Collects essential networking preferences:
  - Professional industry
  - Specific interests and topics
  - Experience level
  - Location preferences for events
- Validates and guides the conversation flow
- Generates a structured summary of networking preferences
- Recommends relevant networking events based on user profile
- Allows for additional preferences like event type and size

## Web Interface

The web interface provides:
- A professional landing page with information about the networking service
- A chat button that users can click to interact with the chatbot
- A conversational interface that guides users through providing their networking preferences
- Generated recommendations for networking events based on user profile

## Chatbot Behavior

The chatbot will:
1. Ask about the user's profession or industry
2. Inquire about specific professional interests and topics
3. Ask about years of experience
4. Get location preferences for networking events
5. Offer an opportunity to add any additional event preferences
6. Provide a complete summary of networking criteria
7. Generate personalized event recommendations

## Testing

Run the test script to go through test scenarios:
```
python run_tests.py
```

## Documentation

For more detailed information, refer to the `DOCUMENTATION.md` file. 