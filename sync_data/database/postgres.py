import psycopg2
from psycopg2.extras import DictCursor

class PostgresBase:

    psycopg2.extras.register_uuid()

    def __init__(self, dsl: dict):
        self.dsl = dsl

    def __enter__(self):
        self.connection = psycopg2.connect(
            **self.dsl, cursor_factory=DictCursor
        )
        self.cursor = self.connection.cursor()
        return self

    def query(self, sql):
        try:
            self.cursor.execute(sql, [])
        except (psycopg2.OperationalError, psycopg2.InterfaceError):
            self.__enter__()
        return self.cursor


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()


class PostgresMovies(PostgresBase):

    def get_many(self, table_name: str, skip: int = 0, limit: int = 100):
        sql = f"""SELECT * FROM {table_name} ORDER BY id DESC LIMIT {limit} OFFSET {skip};"""
        return self.query(sql).fetchall()



