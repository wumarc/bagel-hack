import numpy as np
import pandas as pd
import cohere
import os
import json
import re
import traceback
from dotenv import load_dotenv
from event_embeddings import embed_user_query

# Load environment variables
print("Loading environment variables...")
load_dotenv()

# Initialize Cohere client
print("Initializing Cohere client...")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY environment variable not set. Please set it in a .env file.")
else:
    print(f"COHERE_API_KEY found with length: {len(COHERE_API_KEY)}")

co = cohere.Client(COHERE_API_KEY)

def cosine_similarity(embedding1, embedding2):
    """
    Calculate cosine similarity between two embeddings
    """
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

def get_top_similar_events(user_summary, top_n=10):
    """
    Find top N events most similar to the user summary based on embeddings
    """
    print(f"Finding events similar to user summary: '{user_summary}'")
    
    # Generate embedding for the user summary
    try:
        user_embedding = embed_user_query(user_summary)
        print(f"Generated user embedding with shape: {user_embedding.shape}")
    except Exception as e:
        print(f"Error generating user embedding: {str(e)}")
        traceback.print_exc()
        return None
    
    # Load event embeddings and events data
    try:
        print("Loading event embeddings and processed events data...")
        event_embeddings = np.load("event_embeddings.npy")
        print(f"Loaded event embeddings with shape: {event_embeddings.shape}")
        
        events_df = pd.read_csv("processed_events.csv")
        print(f"Loaded processed events data with {len(events_df)} rows")
    except FileNotFoundError as e:
        print(f"Error: {str(e)}. Run event_embeddings.py first.")
        return None
    except Exception as e:
        print(f"Error loading embeddings or events data: {str(e)}")
        traceback.print_exc()
        return None
    
    # Calculate similarity scores
    print("Calculating similarity scores...")
    similarities = []
    for i, event_embedding in enumerate(event_embeddings):
        similarity = cosine_similarity(user_embedding, event_embedding)
        similarities.append((i, similarity))
    
    # Sort by similarity (highest first)
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Get top N results
    print(f"Getting top {top_n} results...")
    top_results = []
    for i, similarity in similarities[:top_n]:
        event_data = events_df.iloc[i]
        result = {
            "event_id": event_data.get("event_id", f"Event {i}"),
            "event_name": event_data.get("event name", ""),
            "date": event_data.get("date", ""),
            "similarity_score": float(similarity),
            "topics": f"{event_data.get('Key topic 1', '')} {event_data.get('Key topic 2', '')} {event_data.get('Key topic 3', '')}".strip(),
            "location": event_data.get("location", ""),
            "summary": event_data.get("event summary", ""),
            "event_text": event_data.get("event_text", "")
        }
        top_results.append(result)
    
    return top_results

def create_prompt(user_summary, top_events):
    """
    Create a prompt for Cohere to refine the top N matches
    """
    prompt = f"""User preferences:
{user_summary}

Event options:
"""
    
    for i, event in enumerate(top_events):
        prompt += f"{i+1}. {event['event_name']} - {event['date']} - {event['location']}\n"
        prompt += f"   Summary: {event['summary']}\n"
        prompt += f"   Topics: {event['topics']}\n\n"
    
    prompt += """Based on the user's preferences, select and rank the top 3 most relevant events for networking. 
For each selected event, provide:
- A brief reason why it's a good fit
- A relevance score (1 to 100)

Format your response as follows:
Event #X: [Event Name]
Reason: [Brief explanation of why this event is relevant]
Relevance Score: [Score between 1-100]

Please ensure your response is structured exactly as specified above."""
    
    return prompt

def parse_llm_output(output_text):
    """
    Parse the LLM output into a structured format
    """
    print("Parsing LLM output...")
    
    results = []
    
    # Extract each event section using regex
    pattern = r"Event #\d+: (.*?)\nReason: (.*?)\nRelevance Score: (\d+)"
    matches = re.findall(pattern, output_text, re.DOTALL)
    
    for match in matches:
        event_name = match[0].strip()
        reason = match[1].strip()
        score = int(match[2].strip())
        
        results.append({
            "event_title": event_name,
            "reason": reason,
            "relevance_score": score
        })
    
    return results

def llm_filter_events(user_summary, top_n=10):
    """
    Main function to filter events using embeddings and LLM
    """
    try:
        # Step 1: Get top N similar events based on embeddings
        top_events = get_top_similar_events(user_summary, top_n)
        if not top_events:
            return None
        
        # Step 2: Create prompt for Cohere
        prompt = create_prompt(user_summary, top_events)
        print("\nPrompt for Cohere:")
        print("-" * 80)
        print(prompt)
        print("-" * 80)
        
        # Step 3: Call Cohere's generate API with a valid model
        print("\nCalling Cohere's generate API...")
        try:
            response = co.generate(
                prompt=prompt,
                max_tokens=800,
                temperature=0.3,
                k=0,
                p=0.75
            )
            
            # Get the generated text
            output_text = response.generations[0].text
            print("\nCohere's response:")
            print("-" * 80)
            print(output_text)
            print("-" * 80)
            
        except Exception as e:
            print(f"Error in Cohere generate API call: {str(e)}")
            traceback.print_exc()
            # Mock response for testing
            output_text = f"""Event #1: {top_events[0]['event_name']} 
Reason: This event matches the user's interests.
Relevance Score: 95

Event #2: {top_events[1]['event_name']}
Reason: This event is also relevant to the user's interests.
Relevance Score: 85

Event #3: {top_events[2]['event_name']}
Reason: This event provides good networking opportunities.
Relevance Score: 75"""
            print("\nUsing mock response for testing:")
            print("-" * 80)
            print(output_text)
            print("-" * 80)
        
        # Step 4: Parse the LLM output
        parsed_results = parse_llm_output(output_text)
        
        # Step 5: Return the structured results
        return {
            "user_summary": user_summary,
            "embedding_top_events": top_events,
            "llm_filtered_events": parsed_results,
            "llm_raw_output": output_text
        }
    
    except Exception as e:
        print(f"Error in llm_filter_events: {str(e)}")
        traceback.print_exc()
        return None

def main():
    try:
        # Process individual user summary for example.json
        custom_user_summary = "I'm a healthcare professional interested in AI and data analytics applications in medicine, looking for conferences where I can learn about the latest innovations."
        print(f"\n\n{'='*100}")
        print(f"Processing custom user summary: '{custom_user_summary}'")
        print(f"{'='*100}")
        
        # Filter events for the custom user
        custom_results = llm_filter_events(custom_user_summary, top_n=10)
        
        if custom_results:
            print("\nFinal Results for custom user:")
            print("-" * 80)
            
            for j, event in enumerate(custom_results["llm_filtered_events"]):
                print(f"Rank {j+1}: {event['event_title']}")
                print(f"  Reason: {event['reason']}")
                print(f"  Relevance Score: {event['relevance_score']}")
                print()
            
            # Save custom results to example.json
            filename = "example.json"
            with open(filename, "w") as f:
                json.dump(custom_results, f, indent=2)
            print(f"Custom results saved to {filename}")
        else:
            print("No results found for custom user.")
        
        # Example user summaries
        test_summaries = [
            "I'm a tech professional interested in AI and machine learning. I want to network with others in this field.",
            "I work in finance and blockchain technology. Looking for events to expand my network in crypto and financial tech.",
            "I'm a sustainability advocate looking for green tech events to connect with like-minded professionals.",
            "I'm a VR/AR developer based in Toronto looking for local networking events in my field."
        ]
        
        # Process each user summary
        for i, user_summary in enumerate(test_summaries):
            print(f"\n\n{'='*100}")
            print(f"Processing user summary: '{user_summary}'")
            print(f"{'='*100}")
            
            # Filter events using embeddings and LLM
            results = llm_filter_events(user_summary, top_n=10)
            
            if results:
                print("\nFinal Results:")
                print("-" * 80)
                
                for j, event in enumerate(results["llm_filtered_events"]):
                    print(f"Rank {j+1}: {event['event_title']}")
                    print(f"  Reason: {event['reason']}")
                    print(f"  Relevance Score: {event['relevance_score']}")
                    print()
                
                # Save results to JSON file
                filename = f"filtered_events_{i+1}.json"
                with open(filename, "w") as f:
                    json.dump(results, f, indent=2)
                print(f"Results saved to {filename}")
            else:
                print("No results found.")
    
    except Exception as e:
        print(f"Error in main function: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main() 