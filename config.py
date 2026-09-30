"""
Configuration settings for the Rice RAG system.
All tunable numbers live here so they are easy to experiment with.
"""

YOUTUBE_URLS = ["https://www.youtube.com/watch?v=XFLKKizxbHY"]

# --- Chunking Settings ---
CHUNK_SIZE = 800
CHUNK_OVERLAP = 120

# --- Embedding Settings ---
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_STORE_DIR = "chroma_db"

# --- Retrieval Settings ---
TOP_K = 3
MAX_DISTANCE = 0.8  # Lower means closer in cosine distance

# --- LLM Settings ---
LLM_MODEL = "llama3-8b-8192"  # A fast Groq-hosted model
LLM_TEMPERATURE = 0.1
LLM_MAX_TOKENS = 512
