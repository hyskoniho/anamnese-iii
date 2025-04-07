from pydantic import BaseModel
from typing import List

class ColumnMapping(BaseModel):
    column_name: str
    sql_type: str

class ExcelData(BaseModel):
    data: List[dict]