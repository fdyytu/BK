import sqlite3
from typing import Any
import os
from .exceptions import ConnectionError, QueryError
from .constants import SQLITE_PRAGMA, MAX_CONNECTIONS, TIMEOUT
from .validators import DatabaseValidator

class DatabaseConnection:
    _instance = None
    _connection_count = 0

    def __new__(cls, *args, **kwargs):
        """Singleton pattern untuk memastikan hanya ada satu instance"""
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_file: str = "application.db"):
        """Inisialisasi koneksi database"""
        if not hasattr(self, 'initialized'):
            self.db_file = db_file
            self.validator = DatabaseValidator()
            self.initialized = True

    def _initialize_connection(self, conn: sqlite3.Connection) -> None:
        """Initialize connection settings"""
        for pragma, value in SQLITE_PRAGMA.items():
            conn.execute(f"PRAGMA {pragma} = {value}")

    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        if self._connection_count >= MAX_CONNECTIONS:
            raise ConnectionError("Too many database connections")

        try:
            conn = sqlite3.connect(self.db_file, timeout=TIMEOUT)
            self._initialize_connection(conn)
            conn.row_factory = sqlite3.Row
            self._connection_count += 1
            return conn
        except sqlite3.Error as e:
            raise ConnectionError(f"Failed to connect to database: {e}")

    def execute_query(self, query: str, params: tuple = None) -> Any:
        """Execute database query"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor
        except sqlite3.Error as e:
            conn.rollback()
            raise QueryError(f"Query execution failed: {e}")
        finally:
            self._connection_count -= 1
            conn.close()