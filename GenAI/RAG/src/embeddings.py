# embeddings.py
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-mpnet-base-v2"

def generate_embeddings(chunks):
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode([chunk["chunk"] for chunk in chunks], show_progress_bar=True)
    return embeddings
