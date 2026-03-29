"""Get motor quote tool for AutoGuard Insurance Agent"""
import json
import logging
import requests
from datetime import datetime, date
from typing import Dict, Optional
from strands import tool
from ..utils import encode_base64, decode_base64, normalize
import insurance_bot.config as config
import os

logger = logging.getLogger(__name__)

@tool
def get_motor_quote(
    registrationNo: str,
    make: str,
    model: str,
    variant: str,
    registrationDate: str,
    fuelType: str,
    registrationCity: str,
    policyStartDate: Optional[str] = None,
    previousPolicyExpireDate: Optional[str] = None,
    previousInsurancePolicy: Optional[str] = None,
    previousNcb: Optional[str] = None,
    transferOfNcb: Optional[str] = None,
    transferOfNcbPercentage: Optional[str] = None,
    breakinInsurance: Optional[str] = None,
    customerType: Optional[str] = None,
    is_electrical: Optional[str] = None,
    is_non_electrical: Optional[str] = None,
    is_preferredGarage: Optional[str] = None,
    is_recommend_preferredGarage: Optional[str] = None,
    payAsYouDrive: Optional[str] = None,
    previousClaimMade: Optional[str] = None
) -> Dict:
    """
    Get a motor insurance quote with various configuration options.

    Args:
        registrationNo: Vehicle registration number
        make: Vehicle make/brand
        model: Vehicle model
        variant: Vehicle variant
        registrationDate: Vehicle registration date (YYYY-MM-DD)
        fuelType: Vehicle fuel type
        registrationCity: City of registration
        policyStartDate: Optional policy start date (YYYY-MM-DD)
        previousPolicyExpireDate: Optional previous policy expiry date (YYYY-MM-DD)
        previousInsurancePolicy: Optional previous insurance policy flag
        previousNcb: Optional previous No Claim Bonus percentage
        transferOfNcb: Optional transfer of NCB flag
        transferOfNcbPercentage: Optional transfer NCB percentage
        breakinInsurance: Optional break-in insurance code
        customerType: Optional customer type (Individual/Corporate)
        is_electrical: Optional electrical accessories flag
        is_non_electrical: Optional non-electrical accessories flag
        is_preferredGarage: Optional preferred garage flag
        is_recommend_preferredGarage: Optional recommended preferred garage flag
        payAsYouDrive: Optional pay-as-you-drive flag
        previousClaimMade: Optional previous claim flag

    Returns:
        Dictionary with quote details and pricing
    """
    # Create params dictionary for the API call
    motor_quote_api_url = os.getenv("MOTOR_QUOTE_API_URL")
    params = {
        **config.vehicle_details,
        "fuelType": fuelType,
        "registrationCity": registrationCity,
        "policyStartDate": policyStartDate,
        "previousPolicyExpireDate": previousPolicyExpireDate,
        "previousInsurancePolicy": previousInsurancePolicy,
        "previousNcb": previousNcb,
        "transferOfNcb": transferOfNcb,
        "transferOfNcbPercentage": transferOfNcbPercentage,
        "breakinInsurance": breakinInsurance,
        "customerType": "Individual",
        "is_electrical": is_electrical,
        "is_non_electrical": is_non_electrical,
        "is_preferredGarage": is_preferredGarage,
        "is_recommend_preferredGarage": is_recommend_preferredGarage,
        "payAsYouDrive": payAsYouDrive,
        "previousClaimMade": previousClaimMade
    }

    required_fields = ['registrationNo', 'make', 'model', 'variant', 'registrationDate', 'fuelType', 'registrationCity']
    for field in required_fields:
        if not params.get(field):
            logger.error(f"Missing required field: {field}")
            return {
                "status": "error",
                "message": f"Missing required field: {field}",
                "response": None
            }

    date_fields = ['policyStartDate', 'previousPolicyExpireDate', 'registrationDate']
    for date_field in date_fields:
        if date_field in params and params[date_field]:
            try:
                datetime.strptime(params[date_field], '%Y-%m-%d')
            except ValueError:
                logger.error(f"Invalid date format for {date_field}: {params[date_field]}")
                return {
                    "status": "error",
                    "message": f"Invalid date format for {date_field}. Use YYYY-MM-DD",
                    "response": None
                }

    request_body = {
        "status": "Plans",
        "registrationNo": params["registrationNo"],
        # "previousInsurancePolicy": normalize(params.get("previousInsurancePolicy"), "01"),
        "previousInsurancePolicy":  "1",
        "policyStartDate": params.get("policyStartDate") if params.get("policyStartDate") else date.today().strftime("%Y-%m-%d"),
        "previousPolicyExpiryDate": params.get("previousPolicyExpireDate") if params.get("previousPolicyExpireDate") else date.today().strftime("%Y-%m-%d"),
        "renewalStatus": "New Policy",
        "previousNcb": str(params.get("previousNcb", "0")),
        "transferOfNcb": normalize(params.get("transferOfNcb"), "YN"),
        "transferOfNcbPercentage": str(params.get("transferOfNcbPercentage", "0")),
        "breakinInsurance": str(params.get("breakinInsurance", "NBK")),
        "cngAddOn": "0",
        "cngValueOfKit": "0",
        "driver_experience": "",
        "driver_age": "",
        "challenge_details": "true",
        "is_preferredGarage": normalize(params.get("is_preferredGarage"), "YN"),
        "preferredGarageDeductibleAmount": "Rs. 5000",
        "customerType": params.get("customerType", "Individual"),
        "is_electrical": normalize(params.get("is_electrical"), "YN"),
        "is_non_electrical": normalize(params.get("is_non_electrical"), "YN"),
        "is_recommend_preferredGarage": normalize(params.get("is_recommend_preferredGarage"), "YN"),
        "recommend_payAsYouDrive": "Y",
        "selectedPlan": "Plans",
        "payAsYouDrive": normalize(params.get("payAsYouDrive"), "YN"),
        "isPA": "1",
        "selectedAddons": config.selected_addons if config.selected_addons else [],
        "make": params["make"],
        "model": params["model"],
        "fuelType": params["fuelType"],
        "variant": params["variant"],
        "registrationDate": params["registrationDate"],
        "registrationCity": params["registrationCity"],
        "previousClaimMade": normalize(params.get("previousClaimMade", "N"), "YN")
    }

    try:
        encoded_body = encode_base64(json.dumps(request_body))
        headers = {
            "Authorization": f"Bearer {config.auth_token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://chatbot-api.uat-example.com",
            "Referer": "https://chatbot-api.uat-example.com/",
            "sec-fetch-mode": "cors",
            "User-Agent": "Mozilla/5.0",
            "src": "AIAGENT"
        }

        logger.info(f"Request payload: {json.dumps(request_body, indent=2)}")
        response = requests.post(
            motor_quote_api_url,
            data=encoded_body,
            # data={"key": encoded_body},
            headers=headers,
            timeout=30
        )

        logger.debug(f"Raw API response status: {response.status_code}")
        logger.debug(f"Raw API response text: {response.text}")

        if response.status_code == 422:
            error_msg = f"Validation Error: {response.text}"
            logger.error(error_msg)
            return {
                "status": "error",
                "message": "Invalid request data. Please check your inputs.",
                "response": error_msg
            }

        response.raise_for_status()

        # Handle base64 decoding
        try:
            decoded_response = decode_base64(response.text)
            logger.debug(f"Decoded response: {decoded_response}")
        except Exception as e:
            logger.error(f"Base64 decode error: {str(e)}")
            return {
                "status": "error",
                "message": "Failed to decode API response",
                "response": response.text
            }

        # Parse JSON
        try:
            if decoded_response.startswith('"') and decoded_response.endswith('"'):
                decoded_response = decoded_response[1:-1].replace('\\"', '"')
            response_data = json.loads(decoded_response)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}. Response: {decoded_response}")
            return {
                "status": "error",
                "message": "Invalid response format from server",
                "response": decoded_response
            }

        if not isinstance(response_data, dict):
            logger.error(f"Unexpected response type: {type(response_data)}")
            return {
                "status": "error",
                "message": "Unexpected response format",
                "response": response_data
            }

        if response_data.get('status') == 'success':
            print (f"===============================QUOTE RESPONSE =======================: {json.dumps(response_data, indent=2)}")
            config.last_quote_response = response_data  
            config.temp_addons_storage = {}
            quotes_data = response_data.get('data', {}).get('data', {}).get('quotes', {})
            
            if not isinstance(quotes_data, dict):
                logger.error(f"Unexpected quotes_data type: {type(quotes_data)}")
                return response_data

            def process_coverage_item(item, is_subcoverage=False):
                """Helper function to process addons/subcoverages"""
                if not isinstance(item, dict) or 'name' not in item:
                    return None
                
                coverage_data = {
                    "is_od_subcoverage": "yes" if is_subcoverage else "no"
                }
                
                # Add all fields except 'isSelected' and 'name'
                for key, value in item.items():
                    if key not in ['isSelected', 'name'] and value is not None:
                        coverage_data[key] = str(value)
                
                return coverage_data

            # Process all modes to collect addons and subcoverages
            for mode in quotes_data.get('modes', []):
                if not isinstance(mode, dict):
                    continue
                
                # Process addons
                for addon in mode.get('addons', []):
                    processed = process_coverage_item(addon)
                    if processed:
                        config.temp_addons_storage[addon['name']] = processed
                
                # Process subcoverages
                for sub in mode.get('subCoverages', []):
                    processed = process_coverage_item(sub, is_subcoverage=True)
                    if processed:
                        config.temp_addons_storage[sub['name']] = processed

            logger.info(f"Processed addons storage: {json.dumps(config.temp_addons_storage, indent=2)}")
            
        logger.debug(f"Motor Quote API Response: {json.dumps(response_data, indent=2)}")
        return response_data

    except requests.exceptions.HTTPError as http_err:
        error_msg = f"HTTP Error {http_err.response.status_code}: {http_err.response.text}"
        logger.error(error_msg)
        return {
            "status": "error",
            "message": "Failed to get motor quote",
            "response": error_msg
        }
    except requests.exceptions.Timeout:
        logger.error("Request timed out")
        return {
            "status": "error",
            "message": "Request timed out. Please try again.",
            "response": None
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Request exception: {str(e)}")
        return {
            "status": "error",
            "message": "Failed to connect to service",
            "response": str(e)
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": "An unexpected error occurred",
            "response": str(e)
        }