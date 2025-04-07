import sqlite3
import logging
from typing import List

logging.basicConfig(level=logging.INFO)

class Database:
    def __init__(self, db_name: str):
        self.connection = sqlite3.connect(db_name)

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