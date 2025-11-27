"""
PostgreSQL Database Adapter for Sentiment Chatbot
Provides persistent storage for conversations and messages
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class PostgresDatabase:
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is required for PostgreSQL")
        
        # Fix Render's postgres:// URL to postgresql://
        if self.database_url.startswith('postgres://'):
            self.database_url = self.database_url.replace('postgres://', 'postgresql://', 1)
        
        logger.info("🐘 Initializing PostgreSQL database...")
        self.init_database()
        logger.info("✅ PostgreSQL database initialized successfully")
    
    def get_connection(self):
        """Get database connection with RealDictCursor"""
        return psycopg2.connect(self.database_url, cursor_factory=RealDictCursor)
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Note: Users table is managed by user_database_postgres.py
            # Just create conversations and messages tables here
            
            # Create conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255),
                    title VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    overall_sentiment VARCHAR(50),
                    sentiment_explanation TEXT
                )
            ''')
            
            # Create messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
                    sender VARCHAR(50) NOT NULL,
                    message_text TEXT NOT NULL,
                    sentiment VARCHAR(50),
                    sentiment_score REAL,
                    compound_score REAL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id)')
            
            conn.commit()
            logger.info("✅ Database tables created/verified")
            
        except Exception as e:
            conn.rollback()
            logger.error(f"❌ Error initializing database: {e}")
            raise
        finally:
            cursor.close()
            conn.close()
    
    def create_conversation(self, user_id: str, title: str = None) -> str:
        """Create a new conversation (returns string ID to match SQLite interface)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO conversations (user_id, title) VALUES (%s, %s) RETURNING id',
                (user_id, title)
            )
            conversation_id = str(cursor.fetchone()['id'])
            conn.commit()
            logger.info(f"✅ Created conversation {conversation_id} for user {user_id}")
            return conversation_id
        except Exception as e:
            conn.rollback()
            logger.error(f"❌ Error creating conversation: {e}")
            raise
        finally:
            cursor.close()
            conn.close()
    
    def save_message(
        self,
        conversation_id: str,
        sender: str,
        text: str,
        sentiment: str = None,
        sentiment_score: float = None
    ) -> str:
        """Add a message to a conversation (matches SQLite interface)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO messages 
                (conversation_id, sender, message_text, sentiment, sentiment_score, compound_score)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (int(conversation_id), sender, text, sentiment, sentiment_score, sentiment_score))
            
            message_id = str(cursor.fetchone()['id'])
            conn.commit()
            return message_id
        except Exception as e:
            conn.rollback()
            logger.error(f"❌ Error adding message: {e}")
            raise
        finally:
            cursor.close()
            conn.close()
    
    def get_conversation(self, conversation_id: str) -> Dict:
        """Get a conversation with all its messages"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Get conversation details
            cursor.execute(
                'SELECT * FROM conversations WHERE id = %s',
                (int(conversation_id),)
            )
            conversation = cursor.fetchone()
            
            if not conversation:
                return None
            
            # Get all messages
            cursor.execute('''
                SELECT * FROM messages 
                WHERE conversation_id = %s 
                ORDER BY timestamp ASC
            ''', (int(conversation_id),))
            
            messages = cursor.fetchall()
            
            return {
                'conversation_id': str(conversation['id']),
                'user_id': conversation['user_id'],
                'title': conversation['title'],
                'created_at': conversation['created_at'].isoformat() if conversation['created_at'] else None,
                'overall_sentiment': conversation['overall_sentiment'],
                'sentiment_explanation': conversation['sentiment_explanation'],
                'messages': [dict(msg) for msg in messages]
            }
        finally:
            cursor.close()
            conn.close()
    
    def get_all_conversations(self, user_id: str = None) -> List[Dict]:
        """Get all conversations for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
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
                    WHERE c.user_id = %s
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
            
            conversations = [
                {
                    'conversation_id': str(row['id']),
                    'user_id': row['user_id'],
                    'title': row['title'],
                    'created_at': row['created_at'].isoformat() if row['created_at'] else None,
                    'overall_sentiment': row['overall_sentiment'],
                    'sentiment_explanation': row['sentiment_explanation'],
                    'message_count': row['message_count']
                }
                for row in rows
            ]
            
            return conversations
        finally:
            cursor.close()
            conn.close()
    
    def update_conversation_sentiment(
        self,
        conversation_id: str,
        overall_sentiment: str,
        sentiment_explanation: str
    ):
        """Update conversation sentiment analysis"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE conversations 
                SET overall_sentiment = %s, sentiment_explanation = %s
                WHERE id = %s
            ''', (overall_sentiment, sentiment_explanation, int(conversation_id)))
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"❌ Error updating conversation sentiment: {e}")
            raise
        finally:
            cursor.close()
            conn.close()
    
    def delete_conversation(self, conversation_id: str):
        """Delete a conversation and all its messages"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM conversations WHERE id = %s', (int(conversation_id),))
            conn.commit()
            logger.info(f"✅ Deleted conversation {conversation_id}")
            return True
        except Exception as e:
            conn.rollback()
            logger.error(f"❌ Error deleting conversation: {e}")
            raise
        finally:
            cursor.close()
            conn.close()
    
    def update_conversation_title(self, conversation_id: str, title: str):
        """Update conversation title"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'UPDATE conversations SET title = %s WHERE id = %s',
                (title, int(conversation_id))
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"❌ Error updating conversation title: {e}")
            raise
        finally:
            cursor.close()
            conn.close()
