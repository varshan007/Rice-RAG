# Rice RAG Notes

## Stage 0: Setup and the big picture
- **What it does**: Sets up the folder structure, virtual environment, and core settings.
- **Why this approach**: We separate configuration (`config.py`) from code and secrets (`.env`) to make experimenting easier and prevent leaking keys to GitHub.
- **Okie's Checkpoint Answers**:
  - *What problem does RAG solve that the mini-GPT could not?* RAG gives the model an open-book test (with specific, real information) rather than relying on its internal, potentially hallucinated knowledge.
  - *Why are indexing and querying separate pipelines?* Indexing is slow and only needs to be done once to build the database. Querying must be fast to answer the user's question quickly.
  - *What happens if retrieval grabs corn instead of rice?* The LLM will see the corn paragraphs and, because of our strict prompt, it will either say "I couldn't find this" (good!) or hallucinate (bad!).

