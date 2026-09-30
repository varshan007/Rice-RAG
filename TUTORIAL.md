# Building a RAG System from Scratch: The Rice RAG Project

This document serves as a complete, step-by-step guide to building the Rice Agriculture RAG (Retrieval-Augmented Generation) system. It documents the architecture, the purpose of each file, and the logical progression we followed to build it from Stage 0 to Stage 5.

---

## 🛠️ Stage 0: Architecture & Setup

Before writing complex logic, a proper RAG system needs a foundation where configuration and secrets are isolated from the main code.

1. **Virtual Environment**: We created a Python virtual environment (`.venv`) to keep all our dependencies (like `langchain`, `chromadb`, and `torch`) isolated from the system Python.
2. **`config.py`**: A centralized file for all "tunable" numbers. Instead of hardcoding chunk sizes or model names deep in our code, we put them here. If we want to switch the LLM from Llama to Qwen, we only change one line in `config.py`.
3. **`.env`**: A secure file for API keys (e.g., `GROQ_API_KEY`). This file is added to `.gitignore` so we never accidentally leak secrets to GitHub.

---

## 📄 Stage 1: Data Extraction (`loaders.py`)

**Goal**: LLMs only understand text. We need to extract clean, readable text from our raw data sources (PDFs and YouTube videos).

* **What we built**: `loaders.py`
* **How it works**: 
  * We used `pypdf` to read the `rice systems.pdf` page by page. We attached "metadata" (like the page number) to each extracted page so we always know the provenance of the information.
  * We used `youtube-transcript-api` to pull auto-generated captions from agricultural YouTube videos. Because captions come in tiny 3-second fragments, we grouped them into logical paragraphs to preserve their meaning.

---

## ✂️ Stage 2: Data Processing (`chunking.py`)

**Goal**: An LLM has a limited "context window" (it can't read an entire 1,000-page book at once). We must slice our extracted text into bite-sized pieces.

* **What we built**: `chunking.py`
* **How it works**: We used Langchain's `RecursiveCharacterTextSplitter`. 
* **The Science**: 
  * **Size (800 chars)**: Small enough to be precise, large enough to contain a full agricultural procedure.
  * **Overlap (120 chars)**: We force chunks to overlap slightly. This ensures that if a crucial sentence (like "Apply fertilizer...") gets cut in half at the end of a chunk, the beginning of the next chunk will contain the full context.

---

## 🧠 Stage 3: The Vector Database (`embeddings.py`, `vectorstore.py`, `ingest.py`)

**Goal**: How do we quickly find the 3 most relevant chunks out of 10,000 when a user asks a question? We convert text into math.

* **What we built**:
  * **`embeddings.py`**: Uses a local HuggingFace model (`all-MiniLM-L6-v2`) to convert every chunk of text into a 384-dimensional mathematical vector. 
  * **`vectorstore.py`**: Initializes a Chroma database to store these vectors. We implemented a **cryptographic hash ID** for each chunk (based on its content and metadata). This prevents the database from storing duplicate copies if we run the ingestion script multiple times.
  * **`ingest.py`**: The master script that ties Stages 1, 2, and 3 together. It loads documents, chunks them, embeds them, and saves them to disk.

---

## 🤖 Stage 4: Retrieval & Generation (`retriever.py`, `llm.py`, `test_rag.py`)

**Goal**: Take a user's question, find the best context, and force an LLM to answer using *only* that context.

* **What we built**:
  * **`retriever.py`**: Tells Chroma to take the user's question, embed it into a vector, and use "Cosine Distance" to find the 3 chunks whose angles are closest to the question's angle.
  * **`llm.py`**: Connects to the Groq API (using the `qwen3.8-27b` model). We set the **Temperature to 0.1** to make the AI strict and factual, preventing creative hallucinations. We also wrote a strict RAG Prompt: *"Answer using ONLY the context below. Do not guess."*
  * **`test_rag.py`**: A testing pipeline that streams 45 evaluation questions through our system. It successfully proved that the AI answers agricultural questions accurately, but strictly refuses to answer irrelevant questions about baking cakes or fixing laptops.

---

## 💻 Stage 5: User Interface (`app.py`)

**Goal**: Build a dashboard so non-programmers can interact with our RAG engine.

* **What we built**: `app.py`
* **How it works**: We used **Streamlit** to wrap our pipeline in a beautiful web chat interface. It maintains chat history in the session state and provides a simple text box for users to interrogate the agricultural knowledge base.

---

## 🚀 How to Run the Project

1. **Activate Environment**: `source .venv/bin/activate`
2. **Add API Key**: Ensure your `.env` file has `GROQ_API_KEY=your_key_here`.
3. **Build the Database**: Run `python3 ingest.py` (You only need to do this once, or whenever you add new PDFs to the `data` folder).
4. **Launch the App**: Run `streamlit run app.py` and open the provided `localhost` link in your browser!
