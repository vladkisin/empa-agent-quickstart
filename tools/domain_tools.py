from langchain.tools import tool
import logging

logger = logging.getLogger(__name__)

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
    logger.info(f"[TOOL] duckduckgo_search called with query={query}")
    if _ddg is None:
        result = f"(Search unavailable in this environment. Query would be: {query})"
        logger.info(f"[TOOL] duckduckgo_search result: {result}")
        return result
    result = _ddg.run(query)
    logger.info(f"[TOOL] duckduckgo_search result: {result[:200]}...")
    return result

