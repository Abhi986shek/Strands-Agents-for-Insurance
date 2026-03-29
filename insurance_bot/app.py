"""
Main Flask application for AutoGuard Insurance Agent
Entry point that initializes and runs the application
"""
import binascii
import os
import json
import logging
import base64
import uuid
import asyncio
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv
from datetime import date
from typing import Dict, List, Any, Optional, AsyncIterator
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify, Response
from flask_cors import CORS

from .routes import setup_routes

app = Flask(__name__)
# Enable CORS only for specific domains
CORS(app, origins=[
    "https://cp.uat-example.com",
    "https://cp-api.uat-example.com"
])
# Setup routes
setup_routes(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
