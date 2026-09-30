# Rice RAG Notes

## Stage 0: Setup and the big picture
- **What it does**: Sets up the folder structure, virtual environment, and core settings.
- **Why this approach**: We separate configuration (`config.py`) from code and secrets (`.env`) to make experimenting easier and prevent leaking keys to GitHub.
- **Checkpoint Answers**:
  - *What problem does RAG solve that the mini-GPT could not?* RAG gives the model an open-book test (with specific, real information) rather than relying on its internal, potentially hallucinated knowledge.
  - *Why are indexing and querying separate pipelines?* Indexing is slow and only needs to be done once to build the database. Querying must be fast to answer the user's question quickly.
  - *What happens if retrieval grabs corn instead of rice?* The LLM will see the corn paragraphs and, because of our strict prompt, it will either say "I couldn't find this" (good!) or hallucinate (bad!).

## Stage 1: Data loading
- **What it does**: Loads the PDF page by page (cleaning hyphenated words), and fetches YouTube captions (grouping them into 60-second blocks).
- **Why this approach**: 
  - *PDF*: 1-based page numbers are used so human readers can easily look up citations. Cleaned text prevents bad embeddings.
  - *YouTube*: Grouping captions into blocks provides enough context for the model, whereas single sentence fragments do not contain enough meaning for a good match.
- **Alternatives**: LangChain's `PyPDFLoader` is an alternative but uses 0-based page numbering.
- **Experiment Results**: 
  - 20-second window: 99 chunks, ~46 words/chunk
  - 60-second window: 38 chunks, ~121 words/chunk
  - 120-second window: 20 chunks, ~230 words/chunk
- **Checkpoint Answers**:
  - *What is a Document?* It gives us knowledge + provenance.
  - *Why store page numbers now, not later?* Metadata preserves where that knowledge came from right at the start.
  - *Why group caption lines?* Caption grouping preserves the meaning of spoken content before we embed it.

## Stage 2: Chunking
- **What it does**: Splits large Document objects into smaller chunks using `RecursiveCharacterTextSplitter`.
- **Why this approach**: 
  - Uses double newlines, single newlines, spaces, and then characters to avoid cutting sentences in half.
  - Adds `start_index` to the metadata to track the exact original location.
  - Carries all original document metadata forward to every chunk.
- **Experiment Results**: 
  - (300, 50) -> 103 chunks (too many, scattered)
  - (800, 120) -> 41 chunks (sweet spot)
  - (1500, 200) -> 26 chunks (too few, very long)
  - Setting overlap to 0 caused the text to awkwardly cut at boundaries, losing context.
- **Checkpoint Answers**:
  - *Why characters and not tokens here?* Because at this indexing stage, we don't necessarily know which LLM (and which tokenizer) we will use for querying.
  - *What does overlap fix and what does it cost?* Overlap preserves continuity across chunks, but it costs us database size since some text is stored twice.
  - *Which setting did you choose?* 800/120 is the practical middle ground: enough context to preserve agricultural procedures, enough overlap to protect boundaries, while avoiding the larger chunks and database overhead of 1500/200.

## Stage 3: Embeddings & Vector Store
- **What it does**: Converts chunks of text into 384-dimensional mathematical vectors and stores them in a Chroma database.
- **Why this approach**:
  - We use `HuggingFaceEmbeddings` locally because it is free, fast, and secure (data doesn't leave our computer).
  - We normalise vectors so cosine similarity acts purely on the angle (meaning) rather than length.
  - We create a unique hash (ID) for each chunk to prevent duplicating data if `ingest.py` is run twice.
- **Checkpoint Answers**:
  - *Why are embeddings normalised?* It ensures vectors all have a length of 1, meaning Cosine Distance operates purely on the angle (the semantic meaning) between them, ignoring the raw magnitude.
  - *Why do we deduplicate chunks before storing?* To make ingestion repeatable without allowing the knowledge base to grow with duplicate copies of the same content.
  - *What happens if you re-run indexing without deduplication?* We will consume roughly 5× the storage and indexing resources, and the LLM will just read 5 identical copies of the same paragraph during retrieval!

## Stage 4: Querying & Generation
- **What it does**: Takes a user's question, embeds it, retrieves the top 3 most similar chunks from Chroma, and forces the LLM to read them before answering.
- **Why this approach**:
  - The strict prompt (`DO NOT guess or make up answers`) prevents hallucinations.
  - The temperature is set to `0.1` so the LLM acts as a strict librarian rather than a creative storyteller.
- **Experiment Results**: 
  - The LLM successfully answered questions about Rice when it found the text (e.g. Q4, Q6).
  - It successfully refused to answer questions about Wheat, Cake, or France because they were not in the context!
- **Checkpoint Answers**:
  - *What happens if retrieval returns Corn instead of Rice at Temperature 0.9?* A highly creative temperature will cause the LLM to make unsupported extrapolations (hallucinate), effectively ignoring the failure of the retrieval.

## Conclusion
The strict RAG prompt works exactly as intended! If a user asks a highly specific question (e.g., about planting in "Trichy, TamilNadu"), the LLM will refuse to hallucinate an answer using its internal knowledge if that specific region is not covered in the retrieved PDF chunks. This proves our AI is grounded in the factual documents we provided.
