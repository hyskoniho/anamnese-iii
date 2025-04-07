import pandas as pd
import logging
from Models.models import ColumnMapping, ExcelData
from Transformer.excel_to_sql import ExcelToSQL
from Database.db import Database

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    column_mappings = [
        ColumnMapping(column_name='name', sql_type='TEXT'),
        ColumnMapping(column_name='age', sql_type='INTEGER'),
        ColumnMapping(column_name='email', sql_type='TEXT'),
    ]

    excel_file_path = 'data.xlsx'
    df = pd.read_excel(excel_file_path)

    excel_to_sql = ExcelToSQL(column_mappings)
    missing_columns = excel_to_sql.validate_columns(df)

    if not missing_columns:
        indexes_to_insert = [0, 1, 2]  # Example indexes
        queries = excel_to_sql.generate_insert_query(df, indexes_to_insert)

        db = Database('your_database.db')
        db.insert_queries(queries)
    else:
        logging.error("Cannot proceed due to missing columns.")