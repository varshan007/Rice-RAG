# This script tests our two loaders to see exactly what they produce.

from loaders import load_pdf, load_youtube

def test_pdf():
    print("=== TESTING PDF LOADER ===")
    # 1. Load the entire PDF into a list of Documents (one per page)
    docs = load_pdf("data/pdfs/rice systems.pdf")
    print(f"Total pages loaded: {len(docs)}")
    
    # 2. Loop through the first 3 pages and print the first 200 characters of each
    for i in range(3):
        if i < len(docs):
            meta = docs[i].metadata
            page_num = meta["page"]
            print(f"\n--- Page {page_num} Metadata: {meta} ---")
            print(docs[i].page_content[:200] + "...")

def test_youtube():
    print("\n=== TESTING YOUTUBE LOADER (BLOCK SIZES) ===")
    # We will test 3 different window sizes to see how many words end up in each block
    url = "https://www.youtube.com/watch?v=XFLKKizxbHY"
    
    for window in [20, 60, 120]:
        docs = load_youtube(url, window_seconds=window)
        print(f"\nWindow: {window} seconds -> Total chunks: {len(docs)}")
        
        # Calculate the average number of words per chunk for this window size
        avg_words = sum(len(d.page_content.split()) for d in docs) / len(docs)
        print(f"Average words per chunk: {avg_words:.1f}")
        
        # Print a sample from the first chunk to see what it looks like
        if docs:
            print(f"Sample metadata: {docs[0].metadata}")
            print(f"Sample text snippet: {docs[0].page_content[:150]}...")

if __name__ == "__main__":
    test_pdf()
    test_youtube()
