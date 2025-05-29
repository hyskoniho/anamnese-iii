import pandas as pd
from datetime import datetime
from typing import Any

class Utils:
    @staticmethod
    def get_max_length(data):
        """
        Get the maximum length of the sequences in the dataset.
        :param data: The dataset containing the sequences.
        :return: The maximum length of the sequences.
        """
        max_length = 0
        for sequence in data:
            if len(sequence) > max_length:
                max_length = len(sequence)
        return max_length
    
    @staticmethod
    def format_value(value: Any) -> str:
        """
        Format the value for SQL insertion.
        :param value: The value to be formatted.
        :return: The formatted value as a string.
        """
        if pd.isna(value):
            return 'NULL'
        elif isinstance(value, str):
            return f"'{value.replace('\'', '\'\'')}'"
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, datetime):
            return f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'"
        else:
            return 'NULL'
    
    @staticmethod
    def generate_sql_insert(mapping: dict, dataframe: pd.DataFrame, table_name: str, batch_size: int = 500) ->  list[str]:
        """
        Generate SQL insert statements for the given mapping and dataframe.
        :param mapping: The mapping of column names to table names.
        :param dataframe: The dataframe containing the data to be inserted.
        :param batch_size: The number of rows to insert in each batch.
        :return: A list of SQL insert statements.
        """
        
        sql_statements: list[str] = []
        for i in range(0, len(dataframe), batch_size):
            batch = dataframe.iloc[i:i + batch_size]
            for _, row in batch.iterrows():
                columns = ', '.join([f"\"{mapping[col]}\"" for col in row.index])
                values = ', '.join([f"'{str(value).replace("\n", "")}'" if isinstance(value, str) else str(value) for value in row.values])
                sql_statements.append(f"INSERT INTO {table_name} ({columns}) VALUES ({values});")
        return sql_statements