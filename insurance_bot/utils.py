"""
Utility functions for AutoGuard Insurance Agent
Handles base64 encoding/decoding and data normalization
"""

import base64
import logging

logger = logging.getLogger(__name__)

def normalize(value, expected):
    """NORMALISATION UTILITIES"""
    if expected == "YN":
        return "Y" if str(value).lower() in ["yes", "y", "true", "1"] else "N"
    if expected == "01":
        return "1" if str(value).lower() in ["yes", "y", "true", "1"] else "0"
    return str(value)

def decode_base64(data):
    """Decodes base64 data with padding handling"""
    try:
        # Add padding if needed
        padding = len(data) % 4
        if padding:
            data += '=' * (4 - padding)
        return base64.b64decode(data).decode('utf-8')
    except Exception as e:
        logger.error(f"Base64 decode error: {str(e)}", exc_info=True)
        raise ValueError("Invalid base64 data")

def encode_base64(data):
    """Encodes data to base64"""
    try:
        if isinstance(data, str):
            data = data.encode('utf-8')
        return base64.b64encode(data).decode('utf-8')
    except Exception as e:
        logger.error(f"Base64 encode error: {str(e)}", exc_info=True)
        raise ValueError("Base64 encoding failed")
