import os
import shutil
import argparse
from loaders import load_pdf, load_youtube
from chunking import split_documents
from embeddings import get_embeddings
from vectorstore import get_vectorstore, make_id
import config

def main(reset=False):
    if reset and os.path.exists(config.VECTOR_STORE_DIR):
        print("Resetting vector store...")
        shutil.rmtree(config.VECTOR_STORE_DIR)
        
    print("Loading documents...")
    all_docs = []
    
    # 1. Load PDF
    pdf_path = "data/pdfs/rice systems.pdf"
    if os.path.exists(pdf_path):
        all_docs.extend(load_pdf(pdf_path))
    else:
        print(f"Warning: {pdf_path} not found.")
        
    # 2. Load YouTube
    for url in config.YOUTUBE_URLS:
        all_docs.extend(load_youtube(url, window_seconds=60))
        
    print(f"Loaded {len(all_docs)} pages/transcripts.")
    
    # 3. Chunk
    chunks = split_documents(all_docs, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    print(f"Created {len(chunks)} chunks.")
    
    # 4. Embed & Store
    print("Initializing embedding model and vector store...")
    embeddings = get_embeddings()
    store = get_vectorstore(embeddings)
    
    print("Adding chunks to vector store (this will take a minute)...")
    # De-duplicate chunks using our deterministic ID
    unique_chunks = {make_id(chunk): chunk for chunk in chunks}
    ids = list(unique_chunks.keys())
    documents = list(unique_chunks.values())
    
    # Add in batches to avoid memory overload
    batch_size = 64
    for i in range(0, len(documents), batch_size):
        store.add_documents(
            documents=documents[i:i+batch_size],
            ids=ids[i:i+batch_size]
        )
        print(f"Processed batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1}")
        
    print("Ingestion complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Delete the vector store before ingesting")
    args = parser.parse_args()
    main(args.reset)
