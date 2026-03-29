import logging
from typing import Dict, List
from strands import tool

logger = logging.getLogger(__name__)

@tool
def process_checkout(
    draft_id: str,
    delivery_methods: List[str],
    contact_info: str
) -> Dict:
    """Generate a payment link and send it via specified delivery methods (sms, email)."""
    logger.info(f"Generating payment link for draft {draft_id}")
    checkout_url = f"https://checkout.example.com/pay/{draft_id}"
    
    return {
        "status": "success",
        "url": checkout_url,
        "message": f"Payment link {checkout_url} sent via {', '.join(delivery_methods)} to {contact_info}."
    }
