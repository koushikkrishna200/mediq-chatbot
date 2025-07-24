import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import EMBEDDING_MODEL_NAME, FAISS_INDEX_PATH


def create_faiss_index(texts, model=None):
    """
    Creates a FAISS index from the provided texts.
    
    :param texts: List of texts (documents) to index.
    :param model: Preloaded SentenceTransformer model (optional).
    """
    if model is None:
        model = SentenceTransformer(EMBEDDING_MODEL_NAME)  # Load model only if not passed
    embeddings = model.encode(texts)
    dimension = embeddings[0].shape[0]
    
    # Initialize FAISS index with L2 distance
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    # Save the index, texts, and model for future retrieval
    with open(FAISS_INDEX_PATH + ".pkl", "wb") as f:
        pickle.dump((index, texts, model), f)

def load_faiss_index():
    """
    Loads the FAISS index, texts, and model from the file.
    
    :return: Tuple containing (index, texts, model)
    """
    try:
        with open(FAISS_INDEX_PATH + ".pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print(f"Error: The index file '{FAISS_INDEX_PATH}.pkl' was not found.")
        return None
    except Exception as e:
        print(f"Error loading the index: {e}")
        return None

def get_top_k_docs(query, k=3):
    """
    Retrieves the top k documents most relevant to the query using the FAISS index.
    
    :param query: The input query to search for relevant documents.
    :param k: The number of top results to return.
    :return: A list of the top k most relevant documents.
    """
    index_data = load_faiss_index()
    if index_data is None:
        return []

    index, texts, model = index_data
    
    # Extract medical entities from the query and augment the query
    entities = extract_medical_entities(query)
    if entities:
        query += " " + " ".join(entities)  # Add extracted entities to the query
    
    # Encode the augmented query
    query_embedding = model.encode([query])
    
    # Perform the search in FAISS index
    D, I = index.search(query_embedding, k)
    
    # Return the top k documents
    return [texts[i] for i in I[0]]
