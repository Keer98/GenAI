# embeddings.py
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-mpnet-base-v2"


def generate_embeddings(chunks):
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode([chunk["chunk"] for chunk in chunks], show_progress_bar=True)
    return embeddings

def generate_query_embedding(text):
    """Generate embedding for a query text."""
    model = SentenceTransformer(MODEL_NAME)
    embedding = model.encode(text)
    return embedding.tolist()  # Convert numpy array to list

