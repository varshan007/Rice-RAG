from dotenv import load_dotenv
load_dotenv()  # This MUST be called first to load our Groq API key!

from llm import get_llm, get_rag_prompt
from retriever import get_retriever, format_docs
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import json

def build_rag_chain():
    """
    Builds the pipeline: 
    Question -> Retriever -> Format Docs -> Prompt -> LLM -> String Output
    """
    retriever = get_retriever()
    llm = get_llm()
    prompt = get_rag_prompt()
    
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain

def run_evaluation():
    print("Building RAG chain...")
    chain = build_rag_chain()
    
    print("Loading test questions...")
    with open("eval/question.json", "r") as f:
        questions = json.load(f)
        
    print("\n=== EVALUATION ===")
    for idx, item in enumerate(questions):
        question = item["question"]
        print(f"\nQ{idx+1}: {question}")
        
        # Invoke the entire chain!
        answer = chain.invoke(question)
        print(f"A: {answer}")
        
if __name__ == "__main__":
    run_evaluation()
