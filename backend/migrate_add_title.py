import sqlite3
import os
def migrate():
    db_path = os.getenv('DATABASE_PATH', './chatbot.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("PRAGMA table_info(conversations)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'title' not in columns:
            cursor.execute('ALTER TABLE conversations ADD COLUMN title TEXT')
            conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()
if __name__ == '__main__':
    migrate()