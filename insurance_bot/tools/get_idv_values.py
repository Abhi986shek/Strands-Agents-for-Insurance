"""Get IDV values tool for AutoGuard Insurance Agent"""
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
def get_idv_values(
    makeName: str,
    model: str,
    carVariant: str,
    registrationCity: str,
    registrationDate: str,
    registrationNo: str,
    rto: Optional[str] = ""
) -> Dict:
    """
    Retrieves the IDV (Insured Declared Value) range for a vehicle.

    Args:
        makeName: Vehicle make/brand
        model: Vehicle model
        carVariant: Vehicle variant
        registrationCity: City of registration
        registrationDate: Registration date (YYYY-MM-DD)
        registrationNo: Vehicle registration number
        rto: Optional RTO code

    Returns:
        Dictionary with min, max and default IDV values
    """
    print("Fetching IDV values")

    api_url = os.getenv("IDV_API_URL")   

    try:
        request_body = {
            "makeName": makeName,
            "model": model,
            "carVariant": carVariant,
            "registrationCity": registrationCity,
            "rto": rto,
            "registrationDate": registrationDate,
            "registrationNo": registrationNo
        }

        encoded_body = encode_base64(json.dumps(request_body))
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
        logger.info(f"Motor IDV Value API Response (decoded): {decoded_response}")
        return json.loads(decoded_response)

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error calling Motor IDV Value API: {str(http_err)}", exc_info=True)
        return {
            "status": "error",
            "message": f"HTTP Error: {str(http_err)}",
            "response": http_err.response.text if http_err.response else None
        }
    except Exception as e:
        logger.error(f"Error calling Motor IDV Value API: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": f"API Error: {str(e)}",
            "response": None
        }