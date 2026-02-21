import psycopg2
from psycopg2 import sql
from contextlib import contextmanager
from src.config.index import Config
import logging

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Manages PostgreSQL database connections"""
    
    def __init__(self):
        self.config = Config()
        self.conn = None
    
    def connect(self):
        """Establish a connection to the PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(
                host=self.config.DB_HOST,
                port=self.config.DB_PORT,
                database=self.config.DB_NAME,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD
            )
            logger.info("Successfully connected to PostgreSQL database")
            return self.conn
        except psycopg2.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def disconnect(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Disconnected from database")
    
    @contextmanager
    def get_cursor(self):
        """Context manager for database cursor"""
        cursor = self.conn.cursor()
        try:
            yield cursor
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            cursor.close()
    
    def execute_query(self, query, params=None):
        """Execute a SELECT query and return results"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except psycopg2.Error as e:
            logger.error(f"Failed to execute query: {e}")
            raise
    
    def execute_update(self, query, params=None):
        """Execute INSERT, UPDATE, or DELETE query"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount
        except psycopg2.Error as e:
            logger.error(f"Failed to execute update: {e}")
            raise

# Global database instance
db = DatabaseConnection()
