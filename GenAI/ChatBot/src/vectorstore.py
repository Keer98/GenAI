from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
import warnings

warnings.filterwarnings("ignore")

def create_vectorstore(texts, urls, model_name="all-mpnet-base-v2"):
    """Creates a FAISS vectorstore."""
    embedding_function = SentenceTransformerEmbeddings(model_name=model_name)
    metadata = [{"url": url} for url in urls]
    vectorstore = FAISS.from_texts(texts=texts, embedding=embedding_function, metadatas=metadata)
    vectorstore.save_local("faiss_index")
    return vectorstore

def load_vectorstore(folder_path="faiss_index", model_name="all-mpnet-base-v2"):
    """Loads a FAISS vectorstore."""
    embedding_function = SentenceTransformerEmbeddings(model_name=model_name)
    return FAISS.load_local(folder_path=folder_path, embeddings=embedding_function,allow_dangerous_deserialization=True)
