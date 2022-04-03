import sqlite3
from pathlib import Path
import psycopg2
from psycopg2.extras import DictCursor
from settings import PG_DB, SQLLITE_DB
from models import (
    Film_Work, Person, Person_Film_Work, Genre, Genre_Film_Work,
)
from loguru import logger


class SQLite:

    def __init__(self, path: Path):
        self.path = path

    def __enter__(self):
        self.connection: sqlite3.Connection = sqlite3.connect(self.path)
        self.connection.row_factory = self.dict_factory
        self.cursor: sqlite3.Cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def show_tables_name(self):
        """Функция получения имен таблиц в БД."""

        query = """SELECT name FROM sqlite_master WHERE type = 'table'"""
        names = [name.get('name') for name in self.cursor.execute(query)]
        return names

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def get_many(self, table_name: str, skip: int = 0, limit: int = 100):
        query = f"""SELECT * FROM {table_name}
        ORDER BY id DESC
        LIMIT {limit} OFFSET {skip};
        """
        return self.cursor.execute(query).fetchall()

    def count_data(self, table_name: str):
        """Функция получения количества записей в запрашиваемой таблице."""

        query = "SELECT Count() FROM %s" % table_name
        self.cursor.execute(query)
        return self.cursor.fetchone().get('Count()')


class Postgres:

    psycopg2.extras.register_uuid()

    def __init__(self, dsl: dict):
        self.dsl = dsl

    def __enter__(self):
        self.connection = psycopg2.connect(
            **self.dsl,
            cursor_factory=DictCursor,
        )
        self.cursor = self.connection.cursor()
        return self

    def get_values(self, row):
        """Получение значений в строке с данными."""
        return tuple(row.dict().values())

    def sql_mogrify(self, row, col_name):
        """Генерация строкового представления вставки данных."""

        args = self.cursor.mogrify(
            f"{','.join(['%s'] * len(col_name))}",
            self.get_values(row)).decode()
        return '(' + args + ')'

    def save_many(self, data: list, col_name: list, table_name: str):
        data = [self.sql_mogrify(row, col_name) for row in data]

        self.cursor.execute(f"""
         INSERT INTO content.{table_name} ({','.join(col_name)})
         VALUES {','.join(data)}
         ON CONFLICT (id) DO NOTHING;
         """)

    def count_data(self, table_name: str):
        """Функция получения количества записей в запрашиваемой таблице."""

        query = f"SELECT COUNT(*) FROM content.{table_name};"
        self.cursor.execute(query, [])
        results = self.cursor.fetchone()
        return results[0]

    def get_many(self, table_name: str, skip: int = 0, limit: int = 100):
        query = f"""SELECT * FROM content.{table_name}
        ORDER BY id DESC
        LIMIT {limit} OFFSET {skip};
        """
        self.cursor.execute(query, [])
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()


def get_model(table_name: str):
    """ Функция получения pydantic модели данных соответствующей таблице."""

    data_model = {
        'film_work': Film_Work,
        'person': Person,
        'person_film_work': Person_Film_Work,
        'genre': Genre,
        'genre_film_work': Genre_Film_Work,
    }
    return data_model.get(table_name)


def syncing_table(sqlite_db, pg_db, name: str, limit: int = 10000):
    model = get_model(name)
    col_name = model.__fields__.keys()
    skip = 0
    while True:
        rows = sqlite_db.get_many(name, skip=skip, limit=limit)
        data = [model(**row) for row in rows]
        if not rows:
            break
        pg_db.save_many(data, col_name, name)
        skip += limit
        logger.debug(f"Синхронизированно {len(rows)} записей в таблицах {name}")


def load_from_sqlite(sqlite_db, pg_db):
    tables = sqlite_db.show_tables_name()

    for name in tables:
        syncing_table(sqlite_db, pg_db, name)

print(PG_DB)
if __name__ == "__main__":
    with SQLite(SQLLITE_DB) as sqlite_db, Postgres(PG_DB) as pg_db:
        load_from_sqlite(sqlite_db, pg_db)
