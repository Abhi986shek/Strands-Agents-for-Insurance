"""Check vehicle registration tool for AutoGuard Insurance Agent"""
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
def check_vehicle_registration(registrationNo: Optional[str] = None) -> Dict:
    """
    Checks vehicle registration details and eligibility.

    Args:
        registrationNo: Vehicle registration number

    Returns:
        Dictionary with registration status and vehicle details
    """
    print("Checking vehicle registration")

    user_quote_api_url = os.getenv("USER_QUOTE_API_URL")
    api_url = os.getenv("VEHICLE_REGISTRATION_API_URL")
    
    # Use global registration if none provided
    # registration_number = registrationNo if registrationNo and not registrationNo else config.registrationNo
    registration_number = registrationNo 

    try:
        headers = {
            "Authorization": f"Bearer {config.auth_token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://chatbot-api.uat-example.com",
            "Referer": "https://chatbot-api.uat-example.com/",
            "User-Agent": "Mozilla/5.0",
            "src": "AIAGENT"
        }

        quote_response = requests.get(user_quote_api_url, headers=headers)

        # Check if response is valid JSON
        try:
            decoded_response = decode_base64(quote_response.text)  # First decode base64
            
            # Handle possible double-encoded JSON string
            if decoded_response.startswith('"') and decoded_response.endswith('"'):
                decoded_response = decoded_response[1:-1]  # Remove outer quotes
                decoded_response = decoded_response.replace('\\"', '"')  # Unescape quotes
                
            quote_data = json.loads(decoded_response)  # Then parse the decoded JSON
        except ValueError as e:
            # If JSON decode fails, log the raw response
            error_msg = f"Invalid JSON response from userQuoteList API. Status: {quote_response.status_code}. Response: {quote_response.text}"
            logger.error(error_msg)
            return {
                "status": "error",
                "message": "Invalid response from server",
                "response": quote_response.text,
                "allowed": False
            }

        vehicle_type = "4W"

        if vehicle_type == "4W":
            quote_list = quote_data.get("data", {}).get("data", {}).get("quote_data", [])
            for quote in quote_list:
                if quote.get("registration_number") == registration_number:
                    config.selected_addons = quote.get("selected_addons", [])
                    logger.info(f"Selected addons: {config.selected_addons}")
                    break

        request_body = {
            "registrationNo": registration_number,
            "type": "LMV"
        }

        encoded_body = encode_base64(json.dumps(request_body))
        logger.info(f"Vehicle Registration Request: {encoded_body}")

        response = requests.post(api_url, data=encoded_body, headers=headers)
        response.raise_for_status()

        # Handle base64 decoding
        decoded_response = decode_base64(response.text)

        # Handle case where response might be double-encoded JSON string
        if decoded_response.startswith('"') and decoded_response.endswith('"'):
            decoded_response = decoded_response[1:-1]  # Remove outer quotes
            decoded_response = decoded_response.replace('\\"', '"')  # Unescape quotes

        try:
            response_data = json.loads(decoded_response)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in decoded response: {decoded_response}")
            return {
                "status": "error",
                "message": "Invalid response format",
                "response": decoded_response,
                "allowed": False
            }

        # Business rule check
        allow_flag = None
        if isinstance(response_data, dict):
            allow_flag = response_data.get("data", {}).get("data", {}).get("allow")

        if allow_flag == "1":
            logger.info(f"Response data{json.dumps(response_data, indent=2)}")
            vehicle_data = response_data.get("data", {}).get("data", {})
            registration_date = vehicle_data.get("Registration Date")
            if not registration_date:
                from datetime import date
                registration_date = date.today().strftime("%Y-%m-%d")
            config.vehicle_details.update({
                "registrationNo": registration_number,
                "make": vehicle_data.get("make"),
                "model": vehicle_data.get("model"),
                "variant": vehicle_data.get("variant"),
                "registrationDate": registration_date,
                "fuelType": vehicle_data.get("fueltype"),
                "registrationCity": vehicle_data.get("rcRegisteredAt"),
            })
            print("Updated vehicle_details:", config.vehicle_details)

        if allow_flag != "1":
            return {
                "status": "blocked",
                "message": "Vehicle not allowed for processing",
                "details": response_data,
                "allowed": False
            }
            
        return {
            "status": "success",
            "response": response_data,
            "allowed": True
        }

    except requests.exceptions.HTTPError as http_err:
        error_msg = f"HTTP error: {str(http_err)}. Response: {http_err.response.text if http_err.response else 'None'}"
        logger.error(error_msg)
        return {
            "status": "error",
            "message": "Service unavailable. Please try again later.",
            "response": error_msg,
            "allowed": False
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": "An unexpected error occurred",
            "response": str(e),
            "allowed": False
        }