import logging
from typing import List, Optional
from .custom_operations import Operations

class Database(Operations):
    def __init__(self, db_type: str, db_name: str = None, host: str = None, port: int = None, user: str = None, password: str = None, database: str = None):
        super().__init__()
        self.db_type = db_type.lower()
        self.connection = None
        self.cursor = None
        
        if self.db_type == 'sqlite':
            import sqlite3
            self.connection = sqlite3.connect(db_name)
            
        elif self.db_type == 'mysql':
            import mysql.connector
            self.connection = mysql.connector.connect(
                host=host,
                port=port or 3306,
                user=user,
                password=password,
                database=database
            )
            
        elif self.db_type == 'postgresql':
            import psycopg2
            self.connection = psycopg2.connect(
                host=host,
                port=port or 5432,
                user=user,
                password=password,
                dbname=database
            )
            
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    def insert_queries(self, queries: List[str]) -> None:
        cursor = self.connection.cursor()
        for query in queries:
            try:
                cursor.execute(query)
                logging.info(f"Executed query: {query}")
            except Exception as e:
                logging.error(f"Failed to execute query: {query} with error: {e}")
        self.connection.commit()
        cursor.close()

    def close(self):
        if self.connection:
            self.connection.close()