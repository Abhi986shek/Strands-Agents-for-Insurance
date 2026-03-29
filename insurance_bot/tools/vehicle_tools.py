import logging
from typing import Dict
from strands import tool

logger = logging.getLogger(__name__)

@tool
def fetch_vehicle_details(license_plate: str) -> Dict:
    """Fetch details of a vehicle using its license plate number."""
    logger.info(f"Fetching details for vehicle {license_plate}")
    # Simulating API response for generic car
    return {
        "status": "success",
        "data": {
            "make": "Honda",
            "model": "Civic",
            "variant": "VXi",
            "registration_year": "2021",
            "fuel_type": "Petrol"
        }
    }
