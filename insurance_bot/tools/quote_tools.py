import logging
from typing import Dict, List, Optional
from strands import tool

logger = logging.getLogger(__name__)

@tool
def calculate_premium(
    make: str,
    model: str,
    registration_year: str,
    previous_claims: str = "no"
) -> Dict:
    """Calculate the base premium and fetch available insurance tiers."""
    logger.info(f"Calculating base premium for {make} {model}")
    return {
        "status": "success",
        "plans": [
            {"tier": "Basic Cover", "price": 4500, "description": "Third party + Theft"},
            {"tier": "Standard Protection", "price": 7200, "description": "Comprehensive with standard deductibles"},
            {"tier": "Premium Shield", "price": 12500, "description": "Zero depreciation + Engine start cover"}
        ]
    }

@tool
def fetch_optional_covers(tier: str) -> Dict:
    """Fetch optional add-on covers for a chosen plan tier."""
    logger.info(f"Fetching add-ons for {tier}")
    addons = [
        {"name": "Zero Depreciation", "price": 1500},
        {"name": "Roadside Assistance", "price": 400},
        {"name": "Key Replacement", "price": 250},
        {"name": "Engine Protection", "price": 1200}
    ]
    return {"status": "success", "addons": addons}

@tool
def create_policy_draft(
    tier: str,
    addons: List[str],
    vehicle_value: int
) -> Dict:
    """Draft a policy based on selected tier, add-ons, and vehicle declared value."""
    logger.info(f"Drafting policy for {tier} with addons {addons}")
    return {
        "status": "success",
        "draft_id": "DRAFT-987654321",
        "message": "Policy draft successfully created."
    }
