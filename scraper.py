# scraper.py
"""
Web scraping logic for Hacker News
"""

import requests
from bs4 import BeautifulSoup
from config import BASE_URL, SCRAPING_CONFIG
from utils import parse_relative_time, normalize_url


def parse_page(page_num):
    """
    Parse a single page of Hacker News

    Args:
        page_num (int): Page number to scrape

    Returns:
        list: List of parsed items
    """
    url = f'{BASE_URL}/?p={page_num}'
    try:
        res = requests.get(url, timeout=SCRAPING_CONFIG['request_timeout'])
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching page {page_num}: {e}")
        return []

    soup = BeautifulSoup(res.text, 'html.parser')

    items = []
    rows = soup.select('tr.athing')

    if not rows:
        print(f"No items found on page {page_num}")
        return []

    for row in rows:
        try:
            item = parse_single_item(row)
            if item:
                items.append(item)
        except Exception as e:
            print(f"Error parsing item: {e}")
            continue

    return items


def parse_single_item(row):
    """
    Parse a single item row from Hacker News

    Args:
        row: BeautifulSoup element representing a story row

    Returns:
        dict: Parsed item data or None if parsing fails
    """
    hn_id = int(row['id'])

    # Try multiple selectors for the title link (HN structure changes over time)
    title_link = (row.select_one('a.titlelink') or
                  row.select_one('a.storylink') or
                  row.select_one('span.titleline a'))

    if not title_link:
        print(f"Could not find title link for item {hn_id}")
        return None

    title = title_link.text.strip()
    url = normalize_url(title_link.get('href', ''), BASE_URL)

    # Get the subtext row (contains points, author, comments, time)
    subtext = row.find_next_sibling('tr')
    if subtext:
        subtext_td = subtext.select_one('td.subtext')
        if subtext_td:
            points = parse_points(subtext_td)
            author = parse_author(subtext_td)
            comments = parse_comments(subtext_td)
            post_time = parse_post_time(subtext_td)
        else:
            points, author, comments, post_time = 0, '', 0, None
    else:
        points, author, comments, post_time = 0, '', 0, None

    return {
        'hn_id': hn_id,
        'title': title,
        'url': url,
        'points': points,
        'author': author,
        'comments': comments,
        'post_time': post_time
    }


def parse_points(subtext_td):
    """Extract points from subtext"""
    points_elem = subtext_td.select_one('.score')
    if points_elem:
        try:
            return int(points_elem.text.split()[0])
        except (ValueError, IndexError):
            return 0
    return 0


def parse_author(subtext_td):
    """Extract author from subtext"""
    author_elem = subtext_td.select_one('a.hnuser')
    return author_elem.text.strip() if author_elem else ''


def parse_comments(subtext_td):
    """Extract comment count from subtext"""
    comment_links = subtext_td.select('a')
    for link in comment_links:
        if 'comment' in link.text:
            try:
                return int(link.text.split()[0])
            except (ValueError, IndexError):
                return 0
    return 0


def parse_post_time(subtext_td):
    """Extract and parse post time from subtext"""
    age_elem = subtext_td.select_one('span.age')
    if age_elem:
        time_str = age_elem.text.strip()
        return parse_relative_time(time_str)
    return None
