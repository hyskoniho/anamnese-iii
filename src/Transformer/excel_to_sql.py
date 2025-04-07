import pandas as pd
import logging
from typing import List, Dict
from Models.models import ColumnMapping, ExcelData

logging.basicConfig(level=logging.INFO)

class ExcelToSQL:
    def __init__(self, column_mappings: List[ColumnMapping]):
        self.column_mappings = {mapping.column_name: mapping.sql_type for mapping in column_mappings}

    def validate_columns(self, df: pd.DataFrame) -> List[str]:
        missing_columns = [col for col in self.column_mappings if col not in df.columns]
        if missing_columns:
            logging.warning(f"Missing columns: {missing_columns}")
        return missing_columns

    def generate_insert_query(self, df: pd.DataFrame, indexes: List[int]) -> List[str]:
        queries = []
        for index in indexes:
            row = df.iloc[index]
            columns = ', '.join(self.column_mappings.keys())
            values = ', '.join(f"'{row[col]}'" for col in self.column_mappings.keys())
            query = f"INSERT INTO your_table_name ({columns}) VALUES ({values});"
            queries.append(query)
        return queries