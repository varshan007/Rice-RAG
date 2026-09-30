from langchain_chroma import Chroma
from langchain_core.documents import Document
import hashlib
import config

def get_vectorstore(embeddings):
    """
    Returns a connection to our Chroma vector database.
    We explicitly tell it to use cosine distance (hnsw:space).
    """
    return Chroma(
        collection_name="rice_rag",
        embedding_function=embeddings,
        persist_directory=config.VECTOR_STORE_DIR,
        collection_metadata={"hnsw:space": "cosine"}
    )

def make_id(doc: Document) -> str:
    """
    Create a unique, deterministic ID for a document chunk.
    This prevents duplicate chunks if we run ingestion twice.
    """
    unique_string = f"{doc.metadata.get('source')}_{doc.metadata.get('page', '')}_{doc.metadata.get('start_seconds', '')}_{doc.page_content[:50]}"
    return hashlib.sha1(unique_string.encode('utf-8')).hexdigest()
