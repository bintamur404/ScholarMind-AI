import os
import sys
from dotenv import load_dotenv

# Load keys for Gemini and LangSmith
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

# Add tools to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.tools.ocr_tool import ocr_tool
from agent.tools.search_tool import web_search_tool
from agent.tools.rag_tool import rag_search_tool

def get_agent_executor():
    """Builds the ScholarMind agent using Google Gemini."""
    
    # Initialize Google Gemini
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

    # Tool list
    tools = [ocr_tool, web_search_tool, rag_search_tool]

    # System prompt defining routing logic
    system_prompt = (
        "You are ScholarMind AI, a Multi-Modal Research Assistant.\n"
        "Your goal is to provide deep, accurate insights using these tools:\n"
        "1. ocr_tool: If a user mentions an image file path, extract text from it.\n"
        "2. rag_search_tool: Search the local vector database of research PDFs. Use this for literature queries.\n"
        "3. web_search_tool: Search the live web for real-time news and general info.\n\n"
        "Be concise, professional, and academic."
    )

    # Compile the LangGraph agent
    agent = create_react_agent(llm, tools, prompt=system_prompt)
    return agent
