import os
import sys
from langchain_core.tools import tool

# Ensure DB layer can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from database.sqlite_vector import SQLiteVectorDB

db = SQLiteVectorDB()

@tool
def rag_search_tool(query: str) -> str:
    """
    Consults the local knowledge base of research papers.
    Args:
        query: Research query.
    """
    try:
        results = db.similarity_search(query)
        if not results: return "No matching local documents found."
        
        formatted = "\n\n".join([f"--- Chunk (Dist: {d:.2f}) ---\n{t}" for t, d in results])
        return formatted
    except Exception as e:
        return f"RAG Error: {e}"
