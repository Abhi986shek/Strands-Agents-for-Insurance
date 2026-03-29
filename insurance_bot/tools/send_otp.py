"""Send OTP tool for AutoGuard Insurance Agent"""
import json
import logging
import requests
from typing import Dict
from strands import tool
# from ..config import API_BASE_URL
from ..utils import encode_base64, decode_base64
import os

logger = logging.getLogger(__name__)


@tool
def send_otp(phone: str) -> Dict:
    """
    Sends an OTP (One-Time Password) to the specified phone number for verification.

    Args:
        phone: The phone number where the OTP should be sent

    Returns:
        Dictionary with the status of the OTP request
    """
    try:
        API_BASE_URL = os.getenv("API_BASE_URL")
        payload = {"phone": phone}
        encoded_body = encode_base64(json.dumps(payload))

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://chatbot-api.uat-example.com",
            "Referer": "https://chatbot-api.uat-example.com/",
            "User-Agent": "Mozilla/5.0",
            "src": "AIAGENT"
        }

        logger.info(f"Sending OTP request for phone: {phone}")

        response = requests.post(
            f"{API_BASE_URL}/getOTP",
            data=encoded_body,
            headers=headers
        )
        response.raise_for_status()

        decoded = decode_base64(response.text)
        result = json.loads(decoded)

        # Check if we need to double-decode as in other API calls
        if isinstance(result, str) and result.startswith('"') and result.endswith('"'):
            result = result[1:-1].replace('\\"', '"')
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                pass
            
        logger.info(f"OTP API response: {result}")
        return result

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error sending OTP: {str(http_err)}", exc_info=True)
        return {
            "status": "error",
            "message": "Failed to send OTP due to HTTP error",
            "details": str(http_err)
        }
    except Exception as e:
        logger.error(f"Unexpected error in send_otp: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": "Failed to send OTP",
            "details": str(e)
        }