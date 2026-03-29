"""Verify OTP tool for AutoGuard Insurance Agent"""
import json
import logging
import requests
from typing import Dict, Optional
from strands import tool
# from ..config import API_BASE_URL
from ..utils import encode_base64, decode_base64
import insurance_bot.config as config
import os

logger = logging.getLogger(__name__)

@tool
def verify_otp(phone: str, otp: str, registration_number: Optional[str] = None) -> Dict:
    """
    Verifies OTP, stores auth token and user profile details for future API calls.
    Args:
        phone: User's phone number
        otp: One-time password received by the user
        registration_number: Optional vehicle registration number
    Returns:
        Dictionary with verification status and message
    """
    try:
        API_BASE_URL = os.getenv("API_BASE_URL")
        # Validate input
        if not phone or not otp:
            raise ValueError("Both phone and OTP are required")

        # Prepare API call
        payload = json.dumps({
            "phone": phone,
            "otp": otp,
            "isLogin": 1,
            "isWhatsappNotification": 1,
            "type": "4W"
        })
        encoded_body = encode_base64(payload)

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://chatbot-api.uat-example.com",
            "Referer": "https://chatbot-api.uat-example.com/",
            "User-Agent": "Mozilla/5.0",
            "src": "AIAGENT"
        }

        response = requests.post(
            f"{API_BASE_URL}/verifyOTP",
            data=encoded_body,
            headers=headers
        )
        response.raise_for_status()

        # First decode the base64 response
        decoded_response = decode_base64(response.text)

        # Handle the double-encoded JSON string
        if decoded_response.startswith('"') and decoded_response.endswith('"'):
            decoded_response = decoded_response[1:-1]  # Remove outer quotes
            decoded_response = decoded_response.replace('\\"', '"')  # Unescape quotes

        # Parse the JSON response
        try:
            api_response = json.loads(decoded_response)
        except json.JSONDecodeError as e:
            return {
                "status": "error",
                "message": "Invalid response format from server",
                "response": decoded_response
            }

        if api_response.get('status') != 'success':
            return {
                "status": "error",
                "message": api_response.get('message', 'OTP verification failed'),
                "response": api_response
            }

        # Extract token and user details
        data_section = api_response.get('data', {}).get('data', {})
        token = data_section.get('token')
        user_details = data_section.get('userDetails', {})
        is_first_login = data_section.get('isFirstLogin', True)

        print(f"TOKEN IS : {token}")
        print(f"USER DETAILS : {json.dumps(user_details, indent=2)}")

        if not token:
            raise ValueError("Token not found in response")

        # Store globally
        config.auth_token = token
        config.registrationNo = registration_number
        config.phoneNo = phone
        config.user_profile = {
            "isFirstLogin": is_first_login,
            "email": user_details.get("email", ""),
            "fname": user_details.get("fname", ""),
            "lname": user_details.get("lname", "")
        }

        return {
            "status": "success",
            "message": "OTP verified successfully",
            "token": token  # Include token in response for debugging
        }

    except requests.exceptions.HTTPError as http_err:
        error_msg = f"HTTP {http_err.response.status_code}" if http_err.response else "HTTP Error"
        logger.error(f"Verify OTP failed: {error_msg}", exc_info=True)
        return {
            "status": "error",
            "message": error_msg,
            "response": http_err.response.text if http_err.response else None
        }

    except Exception as e:
        logger.error(f"Verify OTP exception: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": f"Verification failed: {str(e)}",
            "response": None
        }