# database.py
"""
Database connection and operations for Hacker News scraper
"""

import psycopg2
from config import DB_CONFIG


def connect_db():
    """Create and return a database connection"""
    return psycopg2.connect(
        dbname=DB_CONFIG['dbname'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        sslmode=DB_CONFIG['sslmode']
    )


def create_table():
    """Create the hackernews table if it doesn't exist"""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS hackernews (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        url TEXT,
        points INT,
        author TEXT,
        comments INT,
        post_time TIMESTAMP,
        hn_id INT UNIQUE
    )
    ''')
    conn.commit()
    cur.close()
    conn.close()


def insert_items(items):
    """Insert a list of items into the database"""
    conn = connect_db()
    cur = conn.cursor()

    success_count = 0
    for item in items:
        try:
            cur.execute('''
            INSERT INTO hackernews (hn_id, title, url, points, author, comments, post_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (hn_id) DO UPDATE SET
                points = EXCLUDED.points,
                comments = EXCLUDED.comments,
                post_time = EXCLUDED.post_time
            ''', (
                item['hn_id'], item['title'], item['url'], item['points'],
                item['author'], item['comments'], item['post_time']
            ))
            success_count += 1
        except Exception as e:
            print(f"Error inserting item {item.get('hn_id', 'unknown')}: {e}")

    conn.commit()
    cur.close()
    conn.close()

    return success_count
