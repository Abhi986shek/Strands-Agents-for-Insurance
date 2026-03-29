"""
Configuration module for AutoGuard Insurance Agent
Handles environment variables, logging, and global state
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LOGGING CONFIGURATION
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('app.log', maxBytes=1000000, backupCount=5),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# GLOBAL VARIABLES
session_manager = None
selected_plan_name = None
auth_token = None
registrationNo = None
phoneNo = None
quoteId = None
user_profile = {}
selected_addons = []
last_quote_response = None
temp_addons_storage = {}

# Store latest vehicle details from registration API
vehicle_details = {
    "registrationNo": None,
    "make": None,
    "model": None,
    "variant": None,
    "registrationDate": None,
    "fuelType": None,
    "registrationCity": None
}

# Session storage for managing conversations
sessions = {}