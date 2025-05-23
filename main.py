# main.py
"""
Main application entry point for Hacker News scraper
"""

import time
from config import SCRAPING_CONFIG
from db import create_table, insert_items
from scraper import parse_page


def scrape_all_pages():
    """
    Scrape all pages of Hacker News and save to database
    """
    print("Starting scraping...")
    try:
        create_table()

        page = 1
        total_items = 0

        while True:  # Keep scraping until there are no more pages
            print(f"Scraping page {page}...")
            items = parse_page(page)

            if not items:
                print(f"No items found on page {page}, stopping.")
                break  # Stop when no items are found

            success_count = insert_items(items)
            total_items += success_count

            print(
                f"Scraped page {page} with {success_count}/{len(items)} items successfully inserted.")
            page += 1

            # Be respectful to the server
            time.sleep(SCRAPING_CONFIG['delay_between_pages'])

        print(f"Scraping finished. Total items processed: {total_items}")

    except Exception as e:
        print(f"Error during scraping: {e}")


if __name__ == '__main__':
    scrape_all_pages()
