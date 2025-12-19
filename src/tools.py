from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

@tool
def search(input: str) -> str:
    """Use this tool to search for more information based on the user question"""
    print("retrieving information on website...\n\n")
    tool = TavilySearchResults(max_results=2)  # 2 web ที่เกียวข้อง ประหยัด

    results = tool.invoke(input)
    
    src_and_content = []
    for doc in results:
        text = f"Source: {doc['url']}\nContent: {doc['content']}"
        src_and_content.append(text)
        
    return "\n\n".join(src_and_content)