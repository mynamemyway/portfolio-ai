# app/core/rag.py

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