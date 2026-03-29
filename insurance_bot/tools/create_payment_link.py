"""Create payment link tool for AutoGuard Insurance Agent"""
import json
import logging
import requests
from typing import Dict, Optional
from strands import tool
from ..utils import encode_base64, decode_base64
import insurance_bot.config as config
import os 

logger = logging.getLogger(__name__)

@tool
def create_payment_link(quoteId: Optional[str] = None) -> Dict:
    """
    Generates a payment link for the insurance quote.

    Args:
        quoteId: Quote ID for which to generate payment link (uses stored ID if None)

    Returns:
        Dictionary with payment link URL and status
    """
    print("Generating payment link")
    api_url = os.getenv("CREATE_PAYMEN_LINK_URL")

    print(f"Using quote ID: {config.quoteId}")
    try:
        print("Inside try function")
        # Use provided quoteId or fall back to global
        quote_id_to_use = config.quoteId
        if not quote_id_to_use:
            return {
                "status": "error",
                "message": "No quote ID available. Please save a quote first."
            }

        request_body = {
            "quoteId": quote_id_to_use
        }

        encoded_body = encode_base64(json.dumps(request_body))
        print(f"Create Payment Link API Request (encoded): {encoded_body}")

        headers = {
            "Authorization": f"Bearer {config.auth_token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://chatbot-api.uat-example.com",
            "Referer": "https://chatbot-api.uat-example.com/",
            "User-Agent": "Mozilla/5.0",
            "src": "AIAGENT"
        }

        response = requests.post(api_url, data=encoded_body, headers=headers)
        response.raise_for_status()

        decoded_response = decode_base64(response.text)
        print(f"Create Payment Link API Response (decoded): {decoded_response}")
        return json.loads(decoded_response)

    except requests.exceptions.HTTPError as http_err:
        print("Inside HTTP error")
        logger.error(f"HTTP error calling Create Payment Link API: {str(http_err)}", exc_info=True)
        return {
            "status": "error",
            "message": f"HTTP Error: {str(http_err)}",
            "response": http_err.response.text if http_err.response else None
        }
    except Exception as e:
        logger.error(f"Error calling Create Payment Link API: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": f"API Error: {str(e)}",
            "response": None
        }