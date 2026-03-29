import logging
from typing import Dict
from strands import tool

logger = logging.getLogger(__name__)

@tool
def send_verification_code(phone_number: str) -> Dict:
    """Send a verification code to a user's phone number."""
    logger.info(f"Sending verification code to {phone_number}")
    return {"status": "success", "message": f"Verification code sent to {phone_number}"}

@tool
def verify_user_code(phone_number: str, code: str) -> Dict:
    """Verify a 6-digit code sent to the user."""
    logger.info(f"Verifying code {code} for {phone_number}")
    if code and len(code) == 6:
        return {"status": "success", "token": "generic_session_token_12345"}
    return {"status": "error", "message": "Invalid code provided"}
