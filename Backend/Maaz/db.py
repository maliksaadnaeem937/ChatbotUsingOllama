import sqlite3
from datetime import datetime

DB_NAME = "chat_history.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Conversations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            title TEXT,
            created_at TEXT
        )
    """)

    # Messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT,
            role TEXT,
            content TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def create_conversation(conversation_id, title):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO conversations (id, title, created_at)
        VALUES (?, ?, ?)
    """, (conversation_id, title, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def get_conversations():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title FROM conversations
        ORDER BY created_at DESC
    """)

    data = cursor.fetchall()
    conn.close()
    return data


def save_message(conversation_id, role, content):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO messages (conversation_id, role, content, created_at)
        VALUES (?, ?, ?, ?)
    """, (conversation_id, role, content, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def get_messages(conversation_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, content FROM messages
        WHERE conversation_id = ?
        ORDER BY created_at ASC
    """, (conversation_id,))

    data = cursor.fetchall()
    conn.close()
    return data
