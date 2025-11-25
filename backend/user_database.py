import sqlite3
from datetime import datetime
from typing import Optional
from models.User import User
import os
from db_adapter import DatabaseAdapter
class UserDatabaseManager:
    def __init__(self, db_path: str = None):
        self.adapter = DatabaseAdapter()
        if db_path is None:
            db_path = os.getenv('DATABASE_PATH', './chatbot.db')
        self.db_path = db_path
        self.init_user_tables()
    
    def get_connection(self):
        return self.adapter.get_connection()
    def init_user_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                name TEXT,
                otp TEXT,
                otp_expires_at TEXT,
                email_verified INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                type TEXT DEFAULT 'user',
                created_at TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    def create_user(self, user: User) -> User:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (id, email, name, otp, otp_expires_at, email_verified, status, type, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user.id,
            user.email,
            user.name,
            user.otp,
            user.otp_expires_at.isoformat() if user.otp_expires_at else None,
            1 if user.email_verified else 0,
            user.status,
            user.type,
            user.created_at.isoformat()
        ))
        conn.commit()
        conn.close()
        return user
    def get_user_by_email(self, email: str) -> Optional[User]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email.lower().strip(),))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        return User.from_dict(dict(row))
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        return User.from_dict(dict(row))
    def update_user_otp(self, user_id: str, otp: str, otp_expires_at: datetime):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET otp = ?, otp_expires_at = ? WHERE id = ?
        ''', (otp, otp_expires_at.isoformat(), user_id))
        conn.commit()
        conn.close()
    def clear_user_otp(self, user_id: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET otp = NULL, otp_expires_at = NULL WHERE id = ?
        ''', (user_id,))
        conn.commit()
        conn.close()
    def verify_user_email(self, user_id: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET email_verified = 1 WHERE id = ?
        ''', (user_id,))
        conn.commit()
        conn.close()
    def update_user_name(self, user_id: str, name: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET name = ? WHERE id = ?
        ''', (name, user_id))
        conn.commit()
        conn.close()