from typing import List

class Operations:
    def __init__(self):
        ...
    
    def get_last_n(self, n: int, table: str, order_column: str) -> List[dict]:
        query = f"SELECT * FROM {table} ORDER BY {order_column} DESC LIMIT {n};"
        return self.execute_query(query)