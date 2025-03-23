import numpy as np
import pandas as pd
import cohere
import os
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

def find_similar_events(user_query, top_k=5):
    """
    Find top k events most similar to the user query
    """
    print(f"Finding events similar to query: '{user_query}'")
    
    # Generate embedding for the user query
    try:
        user_embedding = embed_user_query(user_query)
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
    
    # Get top k results
    print(f"Getting top {top_k} results...")
    top_results = []
    for i, similarity in similarities[:top_k]:
        event_data = events_df.iloc[i]
        result = {
            "event_id": event_data.get("event_id", f"Event {i}"),
            "event_name": event_data.get("event name", ""),
            "date": event_data.get("date", ""),
            "similarity_score": similarity,
            "topics": f"{event_data.get('Key topic 1', '')} {event_data.get('Key topic 2', '')} {event_data.get('Key topic 3', '')}".strip(),
            "location": event_data.get("location", ""),
            "summary": event_data.get("event summary", "")
        }
        top_results.append(result)
    
    return top_results

def main():
    try:
        # Example queries
        test_queries = [
            "I'm interested in AI and machine learning events",
            "Looking for blockchain and crypto conferences",
            "Sustainability and green tech workshops near Vancouver",
            "Virtual reality meetups in Toronto"
        ]
        
        # Find similar events for each query
        for query in test_queries:
            print(f"\nQuery: {query}")
            print("-" * 80)
            
            similar_events = find_similar_events(query, top_k=3)
            
            if similar_events:
                for i, event in enumerate(similar_events):
                    print(f"{i+1}. {event['event_name']} ({event['date']})")
                    print(f"   Score: {event['similarity_score']:.4f}")
                    print(f"   Topics: {event['topics']}")
                    print(f"   Location: {event['location']}")
                    print(f"   Summary: {event['summary']}")
                    print()
            else:
                print("No results found. Make sure you've run event_embeddings.py first.")
    
    except Exception as e:
        print(f"Error in main function: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main() 