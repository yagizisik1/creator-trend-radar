import sqlite3
from datetime import datetime

DB_NAME = "trends.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            platform TEXT NOT NULL,
            score INTEGER,
            trend TEXT,
            searched_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_search(topic, platform, score, trend):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO searches (topic, platform, score, trend, searched_at)
        VALUES (?, ?, ?, ?, ?)
    """, (topic, platform, score, trend, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_recent_searches():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM searches ORDER BY searched_at DESC LIMIT 10")
    results = cursor.fetchall()
    conn.close()
    return results