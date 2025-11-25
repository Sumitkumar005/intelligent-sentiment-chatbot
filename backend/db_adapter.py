"""
Database adapter that supports both SQLite and PostgreSQL
"""
import os
import sqlite3
from typing import Any, List, Tuple

# Try to import psycopg2 for PostgreSQL support
try:
    import psycopg2
    import psycopg2.extras
    POSTGRES_AVAILABLE = True
except ImportError as e:
    POSTGRES_AVAILABLE = False
    import logging
    logging.warning(f"psycopg2 not available: {e}. PostgreSQL support disabled.")


class DatabaseAdapter:
    """Unified database interface for SQLite and PostgreSQL"""
    
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        self.is_postgres = self.database_url and self.database_url.startswith('postgresql')
        
        # Only check for psycopg2 if we actually need to use PostgreSQL
        if self.is_postgres and not POSTGRES_AVAILABLE:
            # Log warning but don't fail - will fail later when trying to connect
            import logging
            logging.warning("PostgreSQL URL detected but psycopg2 not available. Falling back to SQLite.")
            self.is_postgres = False
    
    def get_connection(self):
        """Get database connection"""
        if self.is_postgres:
            conn = psycopg2.connect(self.database_url)
            return conn
        else:
            db_path = os.getenv('DATABASE_PATH', './chatbot.db')
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            return conn
    
    def execute(self, conn, query: str, params: Tuple = None):
        """Execute a query and return cursor"""
        cursor = conn.cursor()
        
        # Convert SQLite ? placeholders to PostgreSQL %s
        if self.is_postgres and '?' in query:
            query = query.replace('?', '%s')
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        return cursor
    
    def fetchone(self, cursor) -> dict:
        """Fetch one row as dictionary"""
        if self.is_postgres:
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, row))
            return None
        else:
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def fetchall(self, cursor) -> List[dict]:
        """Fetch all rows as list of dictionaries"""
        if self.is_postgres:
            rows = cursor.fetchall()
            if rows:
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
            return []
        else:
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_placeholder(self) -> str:
        """Get the parameter placeholder for the database"""
        return '%s' if self.is_postgres else '?'
    
    def adapt_schema(self, sqlite_schema: str) -> str:
        """Adapt SQLite schema to PostgreSQL if needed"""
        if not self.is_postgres:
            return sqlite_schema
        
        # Convert SQLite types to PostgreSQL types
        schema = sqlite_schema
        schema = schema.replace('TEXT PRIMARY KEY', 'TEXT PRIMARY KEY')
        schema = schema.replace('INTEGER DEFAULT', 'INTEGER DEFAULT')
        schema = schema.replace('REAL', 'REAL')
        
        return schema
