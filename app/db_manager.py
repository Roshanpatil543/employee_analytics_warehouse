from __future__ import annotations

import mysql.connector
from mysql.connector import Error as MySQLError

from app.config import settings


class DatabaseConnection:
    """Singleton database connection helper for MySQL-backed app logic."""

    _instance = None
    _connection = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._initialized = True
        self.config = {
            "host": settings.db_host,
            "port": settings.db_port,
            "user": settings.db_user,
            "password": settings.db_password,
            "database": settings.db_name,
            "autocommit": False,
            "raise_on_warnings": True,
        }

    def get_connection(self):
        try:
            if self._connection is None or not self._connection.is_connected():
                self._connection = mysql.connector.connect(**self.config)
            return self._connection
        except MySQLError as exc:  # pragma: no cover - depends on runtime DB
            raise RuntimeError(f"Database connection failed: {exc}") from exc

    def close(self):
        if self._connection is not None and self._connection.is_connected():
            self._connection.close()
            self._connection = None

    def execute(self, query: str, params=None):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            return cursor
        except MySQLError as exc:
            conn.rollback()
            raise RuntimeError(f"SQL execution failed: {exc}") from exc

    def fetch_all(self, query: str, params=None):
        cursor = self.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        return result

    def fetch_one(self, query: str, params=None):
        cursor = self.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        return result
