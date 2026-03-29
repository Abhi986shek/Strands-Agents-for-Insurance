"""Get available addons for selected plan tool for AutoGuard Insurance Agent"""
import json
from typing import Dict
from strands import tool
import insurance_bot.config as config

@tool
def get_available_addons_for_selected_plan(plan_name: str) -> Dict:
    """
    Returns available add-ons with prices for the specified plan only.

    Args:
        plan_name: The selected plan name (e.g., "Recommended Mode", "Max Mode", etc.)

    Returns:
        Dictionary with addon names and prices for the selected plan
    """
    if not config.last_quote_response or config.last_quote_response.get('status') != 'success':
        return {
            "status": "error",
            "message": "No quote data available. Please generate a quote first."
        }

    # Store the selected plan globally
    config.selected_plan_name = plan_name

    addons = {}
    modes = config.last_quote_response.get('data', {}).get('data', {}).get('quotes', {}).get('modes', [])

    # Find the selected plan mode
    selected_mode = None
    for mode in modes:
        if isinstance(mode, dict) and mode.get('name') == plan_name:
            selected_mode = mode
            break

    if not selected_mode:
        return {
            "status": "error",
            "message": f"Plan '{plan_name}' not found in quote response"
        }

    # Extract addons from the selected mode only
    for addon in selected_mode.get('addons', []):
        if isinstance(addon, dict) and 'name' in addon:
            addons[addon['name']] = {
                "price": float(addon.get('totalPremium', 0)),
                "salesProductTemplateId": addon.get('salesProductTemplateId', ''),
                "details": {k: v for k, v in addon.items() if k not in ['name', 'isSelected', 'totalPremium']}
            }

    # Extract subcoverages from the selected mode only
    for sub in selected_mode.get('subCoverages', []):
        if isinstance(sub, dict) and 'name' in sub:
            addons[sub['name']] = {
                "price": float(sub.get('totalPremium', 0)),
                "salesProductTemplateId": sub.get('salesProductTemplateId', ''),
                "is_subcoverage": True,
                "details": {k: v for k, v in sub.items() if k not in ['name', 'isSelected', 'totalPremium']}
            }

    print (f"===============================AVAILABLE ADDONS UNDER {plan_name}========================: {json.dumps(addons, indent=2)}")
    
    return {
        "status": "success",
        "addons": addons,
        "selected_plan": plan_name
    }