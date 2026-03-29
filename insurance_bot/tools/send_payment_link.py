import json
import logging
import requests
from typing import Dict, List, Optional
from strands import tool
from ..utils import encode_base64, decode_base64
import insurance_bot.config as config
import os

logger = logging.getLogger(__name__)

@tool
def send_payment_link(
    delivery_methods: List[str],
    email: Optional[str] = None,
    phone: Optional[str] = None
) -> Dict:
    """
    Sends the payment link to the user via selected delivery methods (SMS, WhatsApp, Email).
    Args:
        delivery_methods: List of delivery methods ('sms', 'whatsapp', 'email')
        email: Email address (required if 'email' is in delivery_methods)
        phone: Phone number (uses global if not provided)
    Returns:
        Dictionary with the status of sending payment link
    """
    print("Sending payment link via selected methods")
    
    api_url = os.getenv("SEND_PAYMEN_LINK_URL")
    
    try:
        # Validation
        if not delivery_methods:
            return {
                "status": "error",
                "message": "Please select at least one delivery method"
            }
        
        # Validate delivery methods
        valid_methods = ['sms', 'whatsapp', 'email']
        for method in delivery_methods:
            if method not in valid_methods:
                return {
                    "status": "error",
                    "message": f"Invalid delivery method: {method}. Valid options: {', '.join(valid_methods)}"
                }
        
        # Check if quote ID exists
        if not config.quoteId:
            return {
                "status": "error",
                "message": "No quote ID available. Please generate and save a quote first."
            }
        
        # Get phone number - use global variable
        # phone_number = phone if phone else config.phoneNo
        phone_number = config.phoneNo
        if not phone_number and ('sms' in delivery_methods or 'whatsapp' in delivery_methods):
            return {
                "status": "error", 
                "message": "Phone number not available for SMS/WhatsApp delivery"
            }
        
        # Check email requirement
        if 'email' in delivery_methods and not email:
            return {
                "status": "error",
                "message": "Email address is required when email delivery is selected"
            }
        
        # Build mediums array
        mediums = []
        
        if 'sms' in delivery_methods:
            mediums.append({
                "type": "sms",
                "value": phone_number
            })
        
        if 'whatsapp' in delivery_methods:
            mediums.append({
                "type": "whatsapp", 
                "value": phone_number
            })
        
        if 'email' in delivery_methods:
            mediums.append({
                "type": "email",
                "value": email
            })
        
        # Prepare request body
        request_body = {
            "quoteId": config.quoteId,
            "mediums": mediums
        }
        
        encoded_body = encode_base64(json.dumps(request_body))
        print(f"Send Payment Link Request (raw): {json.dumps(request_body, indent=2)}")
        print(f"Send Payment Link Request (encoded): {encoded_body}")
        print(f"Quote ID being used: {config.quoteId}")
        print(f"Auth token (first 50 chars): {config.auth_token[:50] if config.auth_token else 'None'}")
        
        # headers = {
        #     "Authorization": f"Bearer {config.auth_token}",
        #     "Content-Type": "application/x-www-form-urlencoded",
        #     "src": "WEB"
        # }
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
        print(f"Send Payment Link Response (decoded): {decoded_response}")
        
        # Parse response
        try:
            response_data = json.loads(decoded_response)
            
            # Handle double-encoded JSON if needed
            if isinstance(response_data, str):
                response_data = json.loads(response_data)
                
        except json.JSONDecodeError:
            response_data = {"raw_response": decoded_response}
        
        # Build success message
        method_names = {
            'sms': 'SMS',
            'whatsapp': 'WhatsApp', 
            'email': 'Email'
        }
        
        sent_to = []
        for method in delivery_methods:
            if method in ['sms', 'whatsapp']:
                sent_to.append(f"{method_names[method]} ({phone_number})")
            elif method == 'email':
                sent_to.append(f"{method_names[method]} ({email})")
        
        return {
            "status": "success",
            "message": f"Payment link sent successfully via: {', '.join(sent_to)}",
            "delivery_methods": delivery_methods,
            "sent_to": {
                "phone": phone_number if ('sms' in delivery_methods or 'whatsapp' in delivery_methods) else None,
                "email": email if 'email' in delivery_methods else None
            },
            "response": response_data
        }
        
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error sending payment link: {str(http_err)}", exc_info=True)
        return {
            "status": "error",
            "message": f"Failed to send payment link: HTTP Error {http_err.response.status_code}",
            "response": http_err.response.text if http_err.response else None
        }
    except Exception as e:
        logger.error(f"Error sending payment link: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": f"Failed to send payment link: {str(e)}",
            "response": None
        }