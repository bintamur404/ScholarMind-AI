from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import tool

ddg = DuckDuckGoSearchResults()

@tool
def web_search_tool(query: str) -> str:
    """
    Searches the live web for the latest research data and news.
    Args:
        query: Search string.
    """
    try:
        return ddg.invoke(query)
    except Exception as e:
        return f"Web Search Error: {e}"
