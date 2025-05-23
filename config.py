# config.py
"""
Configuration settings for the Hacker News scraper
Using environment variables for sensitive data
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'booksDb'),
    'user': os.getenv('DB_USER', 'muradibra'),
    'password': os.getenv('DB_PASSWORD'),  # Must be set in environment
    'host': os.getenv('DB_HOST', 'testdb.cvsauiqay7ww.eu-north-1.rds.amazonaws.com'),
    'port': os.getenv('DB_PORT', '5432'),
    'sslmode': os.getenv('DB_SSLMODE', 'require')
}

# Validate required environment variables
required_env_vars = ['DB_PASSWORD']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]

if missing_vars:
    raise ValueError(
        f"Missing required environment variables: {', '.join(missing_vars)}")

# Scraping configuration
SCRAPING_CONFIG = {
    'request_timeout': int(os.getenv('REQUEST_TIMEOUT', '10')),
    'delay_between_pages': int(os.getenv('DELAY_BETWEEN_PAGES', '1')),
    'scrape_interval_minutes': int(os.getenv('SCRAPE_INTERVAL_MINUTES', '5'))
}

# URLs
BASE_URL = os.getenv('BASE_URL', 'https://news.ycombinator.com')
