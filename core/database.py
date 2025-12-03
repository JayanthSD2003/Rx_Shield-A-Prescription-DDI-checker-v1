import sqlite3
import os

DB_NAME = "rx_shield.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn
import sqlite3
import os

DB_NAME = "rx_shield.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT NOT NULL, 
            image_path TEXT NOT NULL, 
            result_text TEXT NOT NULL, 
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, password_hash):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def get_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def save_analysis(username, image_path, result_text):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO analyses (username, image_path, result_text) VALUES (?, ?, ?)", 
                  (username, image_path, result_text))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving analysis: {e}")
        return False
    finally:
        conn.close()

def get_recent_analysis(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT image_path, result_text FROM analyses WHERE username=? ORDER BY timestamp DESC LIMIT 1", (username,))
        result = cursor.fetchone()
        return result # (image_path, result_text) or None
    except Exception as e:
        print(f"Error getting analysis: {e}")
        return None
    finally:
        conn.close()
