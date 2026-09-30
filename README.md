# Rice RAG

A Retrieval-Augmented Generation (RAG) system for rice practices and production.

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and add your Groq API key.
3. Place your rice book PDF in `data/pdfs/`.

## Running

1. **Ingest the data** (this will chunk and embed the PDF and video):
   ```bash
   python ingest.py
   ```
2. **Evaluate** (run the test questions):
   ```bash
   python evaluate.py
   ```
3. **Run the UI**:
   ```bash
   streamlit run app.py
   ```
