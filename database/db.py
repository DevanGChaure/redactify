import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "redactify.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def insert_document(original_filename, stored_filename):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO documents (original_filename, stored_filename) VALUES (?, ?)",
        (original_filename, stored_filename),
    )
    conn.commit()
    doc_id = cur.lastrowid
    conn.close()
    return doc_id


def get_all_documents():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM documents ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_document(doc_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM documents WHERE id = ?", (doc_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_filename TEXT NOT NULL,
            stored_filename TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            pii_count INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            redacted_filename TEXT,
            extracted_text TEXT
        )
    """)
    conn.commit()
    conn.close()


def update_extracted_text(doc_id, text, status="extracted"):
    conn = get_connection()
    conn.execute(
        "UPDATE documents SET extracted_text = ?, status = ? WHERE id = ?",
        (text, status, doc_id),
    )
    conn.commit()
    conn.close()