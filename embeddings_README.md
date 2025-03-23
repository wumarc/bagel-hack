# Event and User Embeddings Preparation

This project prepares and stores embeddings for events and user inputs using the Cohere embedding API.

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root and add your Cohere API key:
   ```
   COHERE_API_KEY=your_cohere_api_key_here
   ```
   You can get a Cohere API key by signing up at [cohere.com](https://cohere.com/)

## Files

- `event_embeddings.py`: Main script to process event data and generate embeddings
- `similarity_search.py`: Utility to demonstrate similarity search using the generated embeddings
- `.env`: Contains your Cohere API key
- `synthetic_event_data_2024.csv` and `synthetic_event_data_2025.csv`: Input event data files

## Usage

### 1. Generate Event Embeddings

Run the `event_embeddings.py` script to process the event data and generate embeddings:

```
python event_embeddings.py
```

This will:
- Load and preprocess events from the CSV files
- Generate embeddings for all events using Cohere's API
- Save the embeddings to `event_embeddings.npy`
- Save the processed events data to `processed_events.csv`
- Generate an example user query embedding

### 2. Run Similarity Search

After generating the embeddings, you can use the `similarity_search.py` script to find events similar to user queries:

```
python similarity_search.py
```

This demonstrates how to:
- Generate embeddings for user queries
- Calculate cosine similarity between embeddings
- Find and display the most relevant events for each query

## Customization

- To use your own event data, modify the CSV file paths in `event_embeddings.py`
- To change the embedding model or parameters, modify the relevant parameters in the `generate_embeddings` function
- To add your own queries, edit the `test_queries` list in `similarity_search.py`

## Output

The script generates the following output files:
- `event_embeddings.npy`: NumPy array containing event embeddings
- `processed_events.csv`: Processed event data with text representations
- `user_embedding_example.npy`: Example user query embedding

## Advanced Usage

You can import functions from these scripts to integrate the embedding functionality into other applications:

```python
from event_embeddings import embed_user_query
from similarity_search import find_similar_events

# Generate user query embedding
query = "I'm interested in AI and machine learning events"
results = find_similar_events(query, top_k=5)

# Process results
for event in results:
    print(f"{event['event_name']} - {event['similarity_score']:.4f}")
``` 