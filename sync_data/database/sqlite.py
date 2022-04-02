import sqlite3
from pathlib import Path
import datetime


class SQLiteBase:


    def __init__(self, path: Path):
        self.path = path


    def __enter__(self):
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = self.dict_factory
        self.cursor = self.connection.cursor()
        return self


    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


    def query(self, sql: str):
        return self.cursor.execute(sql)


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


class SQLiteMovies(SQLiteBase):

    def get_many(self, table_name: str, state_date: datetime, skip: int = 0, limit: int = 100):
        sql = f"""SELECT * FROM {table_name}
        ORDER BY modified
        where modified >= {state_date} 
        LIMIT {limit} OFFSET {skip};"""
        return self.query(sql).fetchall()