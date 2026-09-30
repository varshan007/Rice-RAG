import config
from vectorstore import get_vectorstore
from embeddings import get_embeddings

def get_retriever():
    """
    Gets the Chroma vector store and turns it into a 'retriever'.
    The retriever will return the top K chunks using Cosine Distance.
    """
    embeddings = get_embeddings()
    store = get_vectorstore(embeddings)
    
    # search_type="similarity" is standard cosine similarity
    return store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": config.TOP_K
        }
    )

def format_docs(docs):
    """
    Takes the retrieved Document objects and joins their text together
    with blank lines so we can paste it into the LLM's prompt.
    """
    return "\n\n".join(doc.page_content for doc in docs)
