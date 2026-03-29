import logging
from strands import tool

logger = logging.getLogger(__name__)

@tool
def search_faq(query: str) -> str:
    """Provides answers to frequently asked customer questions about insurance products, company rules, policies."""
    logger.info(f"Querying FAQ mock knowledge base with query: {query}")
    return "Our standard policy covers accidents, theft, and natural disasters. Please contact support via 1-800-INSURE if you need specific claim assistance."
