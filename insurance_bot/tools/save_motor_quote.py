"""Save motor quote tool for AutoGuard Insurance Agent"""
import json
import logging
import requests
from typing import Dict, Optional, List
from strands import tool
from ..utils import encode_base64, decode_base64, normalize
import insurance_bot.config as config
import os

logger = logging.getLogger(__name__)

@tool
def save_motor_quote(
    selectedPlan: str,
    email: Optional[str] = "",
    owner_name: Optional[str] = "",
    excludeOD: Optional[str] = "0",
    payAsYouDrive: Optional[str] = "N",
    is_preferredGarage: Optional[str] = "N",
    isPA: Optional[str] = "1",
    phone: Optional[str] = "required_phone",
    selectedAddons: Optional[List[str]] = None
) -> Dict:
    """
    Saves a motor insurance quote with the selected options.

    Args:
        selectedPlan: The insurance plan selected by the user
        email: Optional email address
        owner_name: Optional vehicle owner name
        excludeOD: Optional exclude Own Damage cover (0/1)
        payAsYouDrive: Optional pay-as-you-drive option (Y/N)
        is_preferredGarage: Optional preferred garage option (Y/N)
        isPA: Optional personal accident cover (0/1)
        phone: Optional phone number (will use authenticated number if not provided)
        selectedAddons: Optional list of selected add-ons

    Returns:
        Dictionary with saved quote details including quote_id
    """
    print("Saving motor quote")

    api_url = os.getenv("SAVE_QUOTE_URL")   
    try:
        # Initialize with empty list
        final_addons = []

        # Check if selectedAddons exists and process it
        if selectedAddons:
            addons_input = selectedAddons

            # Case 1: Empty list []
            if isinstance(addons_input, list) and not addons_input:
                final_addons = []            
            # Case 2: String representation of list "[addon1, addon2]"
            elif isinstance(addons_input, str):
                try:
                    # Clean and convert to list if not empty
                    if addons_input.strip() not in ["[]", ""]:
                        addons_input = [
                            x.strip().strip("'\"") 
                            for x in addons_input.strip("[]").split(",")
                            if x.strip()
                        ]
                except Exception as e:
                    logger.warning(f"Error parsing addons string: {str(e)}")
                    addons_input = []            
            # Case 3: Actual list of addons ["addon1", "addon2"]
            if isinstance(addons_input, list) and addons_input:
                for addon_name in addons_input:
                    if addon_name in config.temp_addons_storage:
                        addon_obj = {
                            "name": addon_name,
                            "isSelected": "1",
                            **config.temp_addons_storage[addon_name]
                        }
                        final_addons.append(addon_obj)

        # Get phone number from params or use global
        phone_number = phone
        if phone_number == "required_phone":
            phone_number = config.phoneNo  # Fallback to global
            
        # Maintain all original hardcoded values exactly as they were
        request_body = {
            "phone": phone_number,
            "email": email,
            "owner_name": owner_name,
            "excludeOD": normalize(excludeOD, "01"),
            "selectedPlan": selectedPlan,
            "status": "REVIEW_AND_PAY",
            "selectedAddons": final_addons,  
            "payAsYouDrive": normalize(payAsYouDrive, "YN"),
            "is_preferredGarage": normalize(is_preferredGarage, "YN"),
            "isPA": normalize(isPA, "01"),
            "cngAddOn": "0",  
            "cngValueOfKit": None,  
            "preferredGarageDeductibleAmount": "Rs. 5000"  
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
        logger.info(f"Save Motor Quote API Request Body: {json.dumps(request_body, indent=2)}")
        response = requests.post(api_url, data=encoded_body, headers=headers)
        response.raise_for_status()

        # Decode and parse response
        decoded_response = decode_base64(response.text)
        # Parse the response - handle both string and JSON cases
        try:
            response_data = json.loads(decoded_response)
            
            # Check if response_data is a string (double-encoded JSON)
            if isinstance(response_data, str):
                logger.info("Response is double-encoded JSON string, parsing again...")
                response_data = json.loads(response_data)
            
            # logger.info(f"Save Motor Quote API Response (parsed): {json.dumps(response_data, indent=2)}")
        except json.JSONDecodeError:
            response_data = {"raw_response": decoded_response}
            logger.error(f"Failed to parse JSON response: {decoded_response}")

        # Extract quote ID - with detailed debugging
        quote_id = None

        if isinstance(response_data, dict):
            
            # Try direct quote_id first
            if 'quote_id' in response_data:
                quote_id = response_data['quote_id']
                logger.info(f"Found quote_id directly: {quote_id}")
            
            # Try data.data.quote_id path
            elif 'data' in response_data:
                data_section = response_data['data']
                
                if isinstance(data_section, dict) and 'data' in data_section:
                    inner_data = data_section['data']
                    
                    if isinstance(inner_data, dict) and 'quote_id' in inner_data:
                        quote_id = inner_data['quote_id']

        logger.info(f"Final extracted quote_id: {quote_id}")

        # Save quote ID to global variable if found
        if quote_id:
            config.quoteId = str(quote_id)
            logger.info(f"Successfully extracted and saved quote ID: {config.quoteId}")
            return {
                "status": "success",
                "message": "Quote saved successfully",
                "quote_id": config.quoteId,
                "response": response_data
            }
        else:
            logger.error(f"Could not extract quote ID from response structure")
            return {
                "status": "error",
                "message": "API call succeeded but no quote ID was found in response",
                "response": response_data
            }

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error calling Save Motor Quote API: {str(http_err)}", exc_info=True)
        return {
            "status": "error",
            "message": f"HTTP Error: {str(http_err)}",
            "response": http_err.response.text if http_err.response else None
        }
    except Exception as e:
        logger.error(f"Error calling Save Motor Quote API: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": f"API Error: {str(e)}",
            "response": None
        }