""" 
Utility functions for the Hacker News scraper
"""

import re
from datetime import datetime, timedelta


def parse_relative_time(time_str):
    """
    Convert relative time strings like '2 hours ago', '1 day ago' to datetime objects

    Args:
        time_str (str): Relative time string from Hacker News

    Returns:
        datetime: Parsed datetime object or None if parsing fails
    """
    if not time_str:
        return None

    time_str = time_str.lower().strip()
    now = datetime.now()

    # Handle "just now" or similar
    if 'just now' in time_str or time_str == 'now':
        return now

    # Extract number and unit using regex
    match = re.search(
        r'(\d+)\s*(minute|hour|day|week|month|year)s?\s*ago', time_str)
    if not match:
        # If we can't parse it, return current time
        return now

    number = int(match.group(1))
    unit = match.group(2)

    if unit == 'minute':
        return now - timedelta(minutes=number)
    elif unit == 'hour':
        return now - timedelta(hours=number)
    elif unit == 'day':
        return now - timedelta(days=number)
    elif unit == 'week':
        return now - timedelta(weeks=number)
    elif unit == 'month':
        return now - timedelta(days=number * 30)  # Approximate
    elif unit == 'year':
        return now - timedelta(days=number * 365)  # Approximate

    return now


def normalize_url(url, base_url):
    """
    Normalize URLs to handle relative URLs

    Args:
        url (str): URL to normalize
        base_url (str): Base URL to use for relative URLs

    Returns:
        str: Normalized URL
    """
    if url.startswith('item?'):
        return f'{base_url}/{url}'
    return url
