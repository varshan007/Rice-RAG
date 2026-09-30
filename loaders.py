import re
from pypdf import PdfReader
from langchain_core.documents import Document
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi

def clean_text(text: str) -> str:
    """Clean PDF text by fixing hyphenated words and collapsing spaces."""
    # Re-join words split by end-of-line hyphens (e.g., 'agri-\nculture' -> 'agriculture')
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
    # Collapse multiple spaces and blank lines into a single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def load_pdf(path: str) -> list[Document]:
    """Load a PDF page by page into LangChain Documents with 1-based page numbers."""
    reader = PdfReader(path)
    documents = []
    
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            cleaned_text = clean_text(text)
            if cleaned_text:
                metadata = {
                    "source": path,
                    "type": "pdf",
                    "page": i + 1  # 1-based indexing for humans
                }
                documents.append(Document(page_content=cleaned_text, metadata=metadata))
                
    return documents

def extract_video_id(url: str) -> str:
    """Extract the YouTube video ID from standard or shortened URLs."""
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
    raise ValueError(f"Could not extract video ID from {url}")

def load_youtube(url: str, window_seconds: int = 60) -> list[Document]:
    """
    Fetch YouTube captions and group them into time-blocks.
    Returns Documents with a clickable timestamp URL.
    """
    video_id = extract_video_id(url)
    transcript = YouTubeTranscriptApi().fetch(video_id)
    
    documents = []
    current_text = []
    current_start = 0.0
    
    for item in transcript:
        text = item.text.replace('\n', ' ').strip()
        if text.startswith('[') and text.endswith(']'):
            continue  # Skip markers like [Music] or [Applause]
            
        if not current_text:
            current_start = item.start
            
        current_text.append(text)
        
        # If this caption pushes us past the window size, save the block
        if item.start + item.duration - current_start >= window_seconds:
            block_text = " ".join(current_text)
            metadata = {
                "source": video_id,
                "type": "video",
                "start_seconds": int(current_start),
                # This URL automatically opens the video at the exact start second!
                "url": f"https://youtube.com/watch?v={video_id}&t={int(current_start)}s"
            }
            documents.append(Document(page_content=block_text, metadata=metadata))
            current_text = []  # Reset for the next block
            
    # Add any leftover text at the end of the video
    if current_text:
        block_text = " ".join(current_text)
        metadata = {
            "source": video_id,
            "type": "video",
            "start_seconds": int(current_start),
            "url": f"https://youtube.com/watch?v={video_id}&t={int(current_start)}s"
        }
        documents.append(Document(page_content=block_text, metadata=metadata))
        
    return documents
