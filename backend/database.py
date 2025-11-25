import sqlite3
import uuid
from datetime import datetime
from typing import Optional, List, Dict
import os
from db_adapter import DatabaseAdapter
class DatabaseManager:
    def __init__(self, db_path: str = None):
        self.adapter = DatabaseAdapter()
        if db_path is None:
            db_path = os.getenv('DATABASE_PATH', './chatbot.db')
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        return self.adapter.get_connection()
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                title TEXT,
                created_at TEXT NOT NULL,
                overall_sentiment TEXT,
                sentiment_explanation TEXT
            )
        ''')
        
        # Create messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                conversation_id TEXT NOT NULL,
                sender TEXT NOT NULL,
                message_text TEXT NOT NULL,
                sentiment TEXT,
                sentiment_score REAL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (conversation_id) REFERENCES conversations (id)
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_conversations_user_id 
            ON conversations(user_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_messages_conversation_id 
            ON messages(conversation_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_messages_timestamp 
            ON messages(timestamp)
        ''')
        
        conn.commit()
        conn.close()
    def create_conversation(self, user_id: int, title: str = None) -> str:
        conversation_id = str(uuid.uuid4())
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO conversations (id, user_id, created_at, title) VALUES (?, ?, ?, ?)',
            (conversation_id, user_id, datetime.now(), title)
        )
        conn.commit()
        conn.close()
        return conversation_id
    def save_message(
        self,
        conversation_id: str,
        sender: str,
        text: str,
        sentiment: Optional[str] = None,
        sentiment_score: Optional[float] = None
    ) -> str:
        message_id = str(uuid.uuid4())
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO messages 
            (id, conversation_id, sender, message_text, sentiment, sentiment_score, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            message_id,
            conversation_id,
            sender,
            text,
            sentiment,
            sentiment_score,
            datetime.now()
        ))
        conn.commit()
        conn.close()
        return message_id
    def get_conversation(self, conversation_id: str) -> Dict:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM conversations WHERE id = ?',
            (conversation_id,)
        )
        conversation_row = cursor.fetchone()
        if not conversation_row:
            conn.close()
            return None
        message_rows = cursor.fetchall()
        conn.close()
        conversation = {
            'id': conversation_row['id'],
            'user_id': conversation_row['user_id'],
            'title': conversation_row['title'],
            'created_at': conversation_row['created_at'],
            'overall_sentiment': conversation_row['overall_sentiment'],
            'sentiment_explanation': conversation_row['sentiment_explanation'],
            'messages': [
                {
                    'id': row['id'],
                    'conversation_id': row['conversation_id'],
                    'sender': row['sender'],
                    'message_text': row['message_text'],
                    'sentiment': row['sentiment'],
                    'sentiment_score': row['sentiment_score'],
                    'timestamp': row['timestamp']
                }
                for row in message_rows
            ]
        }
        return conversation
    def get_all_conversations(self, user_id: int = None) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        if user_id is not None:
            cursor.execute('''
                SELECT 
                    c.id,
                    c.user_id,
                    c.title,
                    c.created_at,
                    c.overall_sentiment,
                    c.sentiment_explanation,
                    COUNT(m.id) as message_count
                FROM conversations c
                LEFT JOIN messages m ON c.id = m.conversation_id
                WHERE c.user_id = ?
                GROUP BY c.id
                ORDER BY c.created_at DESC
            ''', (user_id,))
        else:
            cursor.execute('''
                SELECT 
                    c.id,
                    c.user_id,
                    c.title,
                    c.created_at,
                    c.overall_sentiment,
                    c.sentiment_explanation,
                    COUNT(m.id) as message_count
                FROM conversations c
                LEFT JOIN messages m ON c.id = m.conversation_id
                GROUP BY c.id
                ORDER BY c.created_at DESC
            ''')
        rows = cursor.fetchall()
        conn.close()
        conversations = [
            {
                'conversation_id': row['id'],
                'user_id': row['user_id'],
                'title': row['title'],
                'created_at': row['created_at'],
                'overall_sentiment': row['overall_sentiment'],
                'sentiment_explanation': row['sentiment_explanation'],
                'message_count': row['message_count']
            }
            for row in rows
        ]
        return conversations
    def save_conversation_sentiment(
        self,
        conversation_id: str,
        sentiment_data: Dict
    ):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE conversations 
            SET overall_sentiment = ?, sentiment_explanation = ?
            WHERE id = ?
        ''', (
            sentiment_data.get('overall_sentiment'),
            sentiment_data.get('explanation'),
            conversation_id
        ))
        conn.commit()
        conn.close()
    def update_conversation_title(self, conversation_id: str, title: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE conversations 
            SET title = ?
            WHERE id = ?
        ''', (title, conversation_id))
        conn.commit()
        conn.close()
    def delete_conversation(self, conversation_id: str) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'DELETE FROM messages WHERE conversation_id = ?',
                (conversation_id,)
            )
            cursor.execute(
                'DELETE FROM conversations WHERE id = ?',
                (conversation_id,)
            )
            conn.commit()
            deleted = cursor.rowcount > 0
            conn.close()
            return deleted
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e