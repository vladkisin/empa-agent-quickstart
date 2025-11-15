from langchain.tools import tool

try:
    from langchain_community.tools import DuckDuckGoSearchRun
    _ddg = DuckDuckGoSearchRun()
except Exception:
    _ddg = None


@tool
def duckduckgo_search(query: str) -> str:
    """
    Run a simple DuckDuckGo web search and return a short text summary.

    If DuckDuckGo is not available, returns a stub message.
    """
    if _ddg is None:
        return f"(Search unavailable in this environment. Query would be: {query})"
    return _ddg.run(query)

