from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def split_documents(docs: list[Document], chunk_size: int, chunk_overlap: int) -> list[Document]:
    """
    Split a list of Documents into smaller chunks.
    Maintains metadata and adds the starting index of the chunk.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True
    )
    
    return splitter.split_documents(docs)
