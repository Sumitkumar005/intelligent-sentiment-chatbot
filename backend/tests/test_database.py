import os
import tempfile
import sqlite3
import pytest
from database import DatabaseManager
def test_init_db_creates_tables():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        db_path = tmp.name
    try:
        db = DatabaseManager(db_path)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        assert cursor.fetchone() is not None, "conversations table should exist"
        assert cursor.fetchone() is not None, "messages table should exist"
        cursor.execute("PRAGMA table_info(conversations)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        assert 'id' in columns, "conversations should have id column"
        assert 'created_at' in columns, "conversations should have created_at column"
        assert 'overall_sentiment' in columns, "conversations should have overall_sentiment column"
        assert 'sentiment_explanation' in columns, "conversations should have sentiment_explanation column"
        cursor.execute("PRAGMA table_info(messages)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        assert 'id' in columns, "messages should have id column"
        assert 'conversation_id' in columns, "messages should have conversation_id column"
        assert 'sender' in columns, "messages should have sender column"
        assert 'message_text' in columns, "messages should have message_text column"
        assert 'sentiment' in columns, "messages should have sentiment column"
        assert 'sentiment_score' in columns, "messages should have sentiment_score column"
        assert 'timestamp' in columns, "messages should have timestamp column"
        conn.close()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
def test_database_connection_failure_handling():
    invalid_path = "/nonexistent_directory/test.db"
    with pytest.raises(Exception):
        db = DatabaseManager(invalid_path)
        db.create_conversation()