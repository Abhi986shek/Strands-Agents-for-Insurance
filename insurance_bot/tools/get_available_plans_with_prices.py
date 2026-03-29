"""Get available plans with prices tool for AutoGuard Insurance Agent"""
import json
from typing import Dict
from strands import tool
import insurance_bot.config as config

@tool
def get_available_plans_with_prices() -> Dict:
    """
    Returns available insurance plans with their calculated prices from the last quote response.
    Price = (totalODPremium + totalTPPremium + totalPApremium) * 1.18

    Returns:
        Dictionary with plan names and calculated prices
    """
    if not config.last_quote_response or config.last_quote_response.get('status') != 'success':
        return {
            "status": "error",
            "message": "No quote data available. Please generate a quote first."
        }

    plans = {}
    premium_breakdown = config.last_quote_response.get('data', {}).get('data', {}).get('premiumBreakdown', {})

    # Map mode names to premium breakdown keys
    mode_mapping = {
        "Launch Mode": "LAUNCH_MODE_RESPONSE",
        "Cruise Mode": "CRUISE_MODE_RESPONSE",
        "Max Mode": "MAX_MODE_RESPONSE",
        "SAOD Mode": "SAOD_RESPONSE",
        "Recommended Mode": "RECOMMEND_RESPONSE"
    }

    for mode_name, breakdown_key in mode_mapping.items():
        if breakdown_key in premium_breakdown:
            premium_data = premium_breakdown[breakdown_key].get('data', {}).get('premiumDetails', {})

            total_od = float(premium_data.get('totalODPremium', 0))
            total_tp = float(premium_data.get('totalTPPremium', 0)) 
            total_pa = float(premium_data.get('totalPApremium', 0))
            
            # Calculate price: (OD + TP + PA) * 1.18
            calculated_price = (total_od + total_tp + total_pa) * 1.18
            
            plans[mode_name] = {
                "price": round(calculated_price, 2),
                "breakdown": {
                    "totalODPremium": total_od,
                    "totalTPPremium": total_tp,
                    "totalPApremium": total_pa
                }
            }

    print (f"===============================AVAILABLE PLANS ========================: {json.dumps(plans, indent=2)}")

    return {
        "status": "success",
        "plans": plans
    }