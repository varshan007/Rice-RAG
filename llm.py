from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import config
import os

def get_llm():
    """
    Returns our connection to the LLM (Llama 3 via Groq).
    Requires GROQ_API_KEY to be set in the .env file.
    """
    return ChatGroq(
        model=config.LLM_MODEL,
        temperature=config.LLM_TEMPERATURE,
        max_tokens=config.LLM_MAX_TOKENS,
        api_key=os.environ.get("GROQ_API_KEY")
    )

def get_rag_prompt():
    """
    This is the strict instruction we give the LLM. 
    Notice how we command it to ONLY use the context.
    """
    template = """
You are an expert agricultural assistant. Answer the question using ONLY the context provided below.
If you don't know the answer or the context doesn't have the information, just say "I don't have enough information to answer this".
DO NOT guess or make up answers.

Context:
{context}

Question:
{question}

Answer:"""
    return PromptTemplate.from_template(template)
