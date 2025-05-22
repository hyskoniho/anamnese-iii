import pandas as pd
import logging
from Models.models import ColumnMapping, ExcelData
from Transformer import *
from Database.db import Database
from typing import List

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    data = r"C:\Users\Arklok\Documents\Projetos\FACULDADE\anamnese\repository\data\tbl\dados_reais.xlsx"
    
    df = pd.read_excel(data)
    
    tr = PacienteTransformer(df)
    print("\n"*10)
    print(tr.n_dataframe)
    print("\n"*2)
    tr.remove_n_row(267)
    print(tr.n_dataframe)

    # column_mappings: List[ColumnMapping] = [
    #     ColumnMapping(column_name='name', sql_type='TEXT'),
    #     ColumnMapping(column_name='age', sql_type='INTEGER'),
    #     ColumnMapping(column_name='email', sql_type='TEXT'),
    # ]

    # excel_file_path: str = 'data.xlsx'
    # df: pd.DataFrame = pd.read_excel(excel_file_path)

    # excel_to_sql: ExcelToSQL = ExcelToSQL(column_mappings)
    # missing_columns: List[str] = excel_to_sql.validate_columns(df)

    # if not missing_columns:
    #     indexes_to_insert: List[int] = [0, 1, 2]  # Example indexes
    #     queries: List[str] = excel_to_sql.generate_insert_query(df, indexes_to_insert)

    #     db: Database = Database('your_database.db')
    #     db.insert_queries(queries)
    # else:
    #     logging.error("Cannot proceed due to missing columns.")