import json
import sys
from prompted_filtering import llm_filter_events

def process_input_file(input_file_path, output_file_path="input_events.json"):
    """
    Process user summaries from an input text file and save the filtered events to a JSON file.
    
    Args:
        input_file_path (str): Path to the input text file containing user summaries
        output_file_path (str): Path to save the output JSON file (default: input_events.json)
    """
    # Read user summaries from input file
    try:
        with open(input_file_path, 'r') as file:
            user_summaries = [line.strip() for line in file if line.strip()]
        
        print(f"Found {len(user_summaries)} user summaries in the input file.")
    except Exception as e:
        print(f"Error reading input file: {str(e)}")
        return
    
    # Process each user summary and collect results
    all_filtered_results = []
    
    for i, user_summary in enumerate(user_summaries):
        print(f"\n\n{'='*100}")
        print(f"Processing user summary {i+1}/{len(user_summaries)}: '{user_summary}'")
        print(f"{'='*100}")
        
        # Filter events using embeddings and LLM
        full_results = llm_filter_events(user_summary, top_n=10)
        
        if full_results:
            print(f"\nResults found for user summary {i+1}")
            
            # Extract only the LLM filtered events and add event IDs
            llm_filtered_events = full_results["llm_filtered_events"]
            
            # Print the first event from top events to debug
            if full_results["embedding_top_events"]:
                first_event = full_results["embedding_top_events"][0]
                print(f"Debug - First event in top events: {first_event['event_name']}")
                print(f"Debug - Event ID: {first_event['event_id']}")
            
            # Add event IDs to the filtered events
            for event in llm_filtered_events:
                # Find matching event in top events to get its ID
                event_name = event["event_title"].split(" - ")[0].strip()  # Extract just the event name part
                print(f"Debug - Looking for event: {event_name}")
                
                found = False
                for top_event in full_results["embedding_top_events"]:
                    if top_event["event_name"] == event_name:
                        event["event_id"] = top_event["event_id"]
                        print(f"Debug - Found match! Event ID: {top_event['event_id']}")
                        found = True
                        break
                
                if not found:
                    print(f"Debug - No match found for {event_name}")
                    # Set a default event ID
                    event["event_id"] = "unknown"
            
            # Create simplified result with only necessary information
            simplified_result = {
                "user_summary": user_summary,
                "summary_index": i + 1,
                "filtered_events": llm_filtered_events
            }
            
            all_filtered_results.append(simplified_result)
        else:
            print(f"No results found for user summary {i+1}.")
    
    # Save all results to the output JSON file
    if all_filtered_results:
        try:
            with open(output_file_path, 'w') as f:
                json.dump(all_filtered_results, f, indent=2)
            print(f"\nAll filtered results saved to {output_file_path}")
        except Exception as e:
            print(f"Error saving output file: {str(e)}")
    else:
        print("\nNo results to save.")

if __name__ == "__main__":
    # Check if input file path is provided as a command-line argument
    if len(sys.argv) > 1:
        input_file_path = sys.argv[1]
        
        # Check if output file path is provided as a command-line argument
        output_file_path = "input_events.json"
        if len(sys.argv) > 2:
            output_file_path = sys.argv[2]
        
        process_input_file(input_file_path, output_file_path)
    else:
        print("Usage: python process_input.py <input_file_path> [output_file_path]")
        print("Default output file name is 'input_events.json'") 