import getpass
import os
from langchain_core.tools import tool
from langchain_community.tools import TavilySearchResults

if not os.environ.get("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = getpass.getpass("Tavily API key:\n")

def search_eng():
    tavily_tool = TavilySearchResults(
        max_results=5, 
        include_answer=True,
        include_raw_content=True,
        include_images=True,
    )
    return tavily_tool
