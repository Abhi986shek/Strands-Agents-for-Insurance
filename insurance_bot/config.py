"""
Configuration module for generic Auto Insurance Agent
Handles environment variables, logging, and global mock state
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

# Store latest vehicle details for current session
vehicle_details = {
    "license_plate": None,
    "make": None,
    "model": None,
    "year": None
}

# Session storage for managing conversations
sessions = {}