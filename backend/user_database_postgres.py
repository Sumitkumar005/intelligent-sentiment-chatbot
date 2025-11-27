"""
PostgreSQL User Database Adapter
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from typing import Optional
from models.User import User
import logging

logger = logging.getLogger(__name__)

class UserDatabaseManager:
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL required for PostgreSQL")
        
        # Fix Render's postgres:// URL
        if self.database_url.startswith('postgres://'):
            self.database_url = self.database_url.replace('postgres://', 'postgresql://', 1)
        
        self.init_user_tables()
    
    def get_connection(self):
        return psycopg2.connect(self.database_url, cursor_factory=RealDictCursor)
    
    def init_user_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Drop and recreate users table to fix data type issues
            cursor.execute('DROP TABLE IF EXISTS users CASCADE')
            
            cursor.execute('''
                CREATE TABLE users (
                    id VARCHAR(255) PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    name VARCHAR(255),
                    otp VARCHAR(10),
                    otp_expires_at TIMESTAMP,
                    email_verified INTEGER DEFAULT 0,
                    status VARCHAR(50) DEFAULT 'active',
                    type VARCHAR(50) DEFAULT 'user',
                    created_at TIMESTAMP NOT NULL
                )
            ''')
            
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
            
            conn.commit()
            logger.info("✅ User tables initialized")
        except Exception as e:
            conn.rollback()
            logger.error(f"❌ Error initializing user tables: {e}")
            raise
        finally:
            cursor.close()
            conn.close()
    
    def create_user(self, user: User) -> User:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (id, email, name, otp, otp_expires_at, email_verified, status, type, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                user.id,
                user.email,
                user.name,
                user.otp,
                user.otp_expires_at,
                1 if user.email_verified else 0,  # Convert boolean to integer
                user.status,
                user.type,
                user.created_at
            ))
            conn.commit()
            return user
        except Exception as e:
            conn.rollback()
            logger.error(f"❌ Error creating user: {e}")
            raise
        finally:
            cursor.close()
            conn.close()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM users WHERE email = %s', (email.lower().strip(),))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            return User.from_dict(dict(row))
        finally:
            cursor.close()
            conn.close()
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            return User.from_dict(dict(row))
        finally:
            cursor.close()
            conn.close()
    
    def update_user_otp(self, user_id: str, otp: str, otp_expires_at: datetime):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users SET otp = %s, otp_expires_at = %s WHERE id = %s
            ''', (otp, otp_expires_at, user_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"❌ Error updating OTP: {e}")
            raise
        finally:
            cursor.close()
            conn.close()
    
    def clear_user_otp(self, user_id: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users SET otp = NULL, otp_expires_at = NULL WHERE id = %s
            ''', (user_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"❌ Error clearing OTP: {e}")
            raise
        finally:
            cursor.close()
            conn.close()
    
    def verify_user_email(self, user_id: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users SET email_verified = 1 WHERE id = %s
            ''', (user_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"❌ Error verifying email: {e}")
            raise
        finally:
            cursor.close()
            conn.close()
    
    def update_user_name(self, user_id: str, name: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users SET name = %s WHERE id = %s
            ''', (name, user_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"❌ Error updating name: {e}")
            raise
        finally:
            cursor.close()
            conn.close()
