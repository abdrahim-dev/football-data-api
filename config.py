"""
Configuration module for the Football Data API.
Handles environment variables, API headers, and directory setup.
"""

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# --- API Configuration ---
# Fetch credentials and base URLs from environment variables
BASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")

# Define headers for authentication with the football-data.org API
HEADERS = {"X-Auth-Token": API_KEY}

# --- File System Configuration ---
# Name of the directory where CSV, JSON, and Plots will be saved
OUTPUT_DIR = "output"

# Create the output directory if it doesn't already exist to prevent errors during export
os.makedirs(OUTPUT_DIR, exist_ok=True)
