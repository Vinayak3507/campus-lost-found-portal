"""Purpose:
Store configuration variables.

Examples:
database_url
jwt_secret
token_expiry

---> This file keeps environment-specific settings separate from code."""

import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_NAME = os.getenv("DB_NAME", "campus_lost_found")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "vinayak3507")