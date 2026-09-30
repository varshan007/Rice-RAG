from loaders import load_pdf
from chunking import split_documents

def run_experiment():
    """
    This test script loads the first 20 pages of the PDF and tries splitting
    them using three different size/overlap combinations to see how many chunks
    we get. It also tests an overlap of 0 to show how abruptly text gets cut.
    """
    print("Loading first 20 non-empty pages of the PDF to experiment...")
    # Load just a subset of pages so the experiment runs fast
    docs = load_pdf("data/pdfs/rice systems.pdf")[:20]
    
    # We will test three different (chunk_size, chunk_overlap) combinations
    settings = [
        (300, 50),
        (800, 120),
        (1500, 200)
    ]
    
    for size, overlap in settings:
        # Split the documents using our settings
        chunks = split_documents(docs, size, overlap)
        print(f"Settings (Size: {size}, Overlap: {overlap}) -> Total Chunks: {len(chunks)}")
    
    print("\n--- ZERO OVERLAP EXPERIMENT ---")
    # Here we set overlap to 0 to demonstrate how it forces unnatural cuts at the boundary
    zero_overlap_chunks = split_documents(docs, 800, 0)
    
    if len(zero_overlap_chunks) > 1:
        print("Looking at the boundary between Chunk 0 and Chunk 1:\n")
        print("End of Chunk 0 (Notice if it abruptly cuts off):")
        print(zero_overlap_chunks[0].page_content[-100:])
        print("\nStart of Chunk 1:")
        print(zero_overlap_chunks[1].page_content[:100])

if __name__ == '__main__':
    run_experiment()
