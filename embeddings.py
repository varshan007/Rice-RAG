from langchain_huggingface import HuggingFaceEmbeddings
import config

def get_embeddings():
    """
    Returns the HuggingFace embedding model.
    We normalize embeddings so cosine distance calculations work perfectly.
    """
    return HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL,
        encode_kwargs={'normalize_embeddings': True}
    )
