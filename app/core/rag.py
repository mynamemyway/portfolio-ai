# app/core/rag.py

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_mistralai.embeddings import MistralAIEmbeddings

from app.config import settings

from pathlib import Path

# --- Constants ---

# Define the root directory of the project.
# Path(__file__) is the path to the current file (app/core/rag.py).
# .parent.parent.parent navigates up three levels to the project root.
ROOT_DIR = Path(__file__).parent.parent.parent

# Directory for the knowledge base source documents.
KNOWLEDGE_BASE_DIR = ROOT_DIR / "knowledge_base"

# Directory where the local ChromaDB vector store will be persisted.
CHROMA_PERSIST_DIR = ROOT_DIR / "chroma_db"

# --- Model Names ---

# Primary embedding model for production (API-based).
MISTRAL_EMBEDDING_MODEL = "mistral-embed"

# Alternative embedding model for local development (requires heavy dependencies).
HF_EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


# --- Embedding Model Initialization ---

def get_embedding_model():
    """
    Initializes and returns the embedding model based on the chosen strategy.

    Primary (Production): MistralAIEmbeddings via API. This is lightweight and
    suitable for serverless environments like Render.

    Alternative (Local): HuggingFaceEmbeddings. Requires installing
    sentence-transformers and its heavy dependencies (e.g., torch).
    """
    # Primary option for production using Mistral's API
    embeddings = MistralAIEmbeddings(
        model=MISTRAL_EMBEDDING_MODEL, mistral_api_key=settings.MISTRAL_API_KEY
    )

    # --- Alternative for local development (commented out) ---
    # embeddings = HuggingFaceEmbeddings(
    #     model_name=HF_EMBEDDING_MODEL_NAME,
    #     model_kwargs={"device": "cpu"},  # Explicitly use CPU
    # )

    return embeddings


# --- Vector Store Initialization ---

def get_vector_store() -> Chroma:
    """
    Initializes and returns the Chroma vector store.

    It uses the embedding model created by get_embedding_model and sets up
    a persistent directory to save the database on disk.
    """
    embeddings = get_embedding_model()
    vector_store = Chroma(
        persist_directory=str(CHROMA_PERSIST_DIR), embedding_function=embeddings
    )
    return vector_store