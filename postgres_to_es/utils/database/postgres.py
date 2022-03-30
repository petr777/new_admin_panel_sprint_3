import time
from loguru import logger
from postgres_to_es.utils.backoff import backoff
import psycopg2
from psycopg2.extras import DictCursor
from postgres_to_es.utils import comeon

class PostgresBase:

    psycopg2.extras.register_uuid()

    def __init__(self, dsl: dict, logger=logger):
        self.dsl = dsl
        self.logger = logger
        self.connect()


    @backoff(logger=logger)
    def connect(self) -> None:
        self.db = psycopg2.connect(**self.dsl, cursor_factory=DictCursor)
        logger.info(f'Соединение с БД: {dsl.get("dbname")} установленно')
        self.cursor = self.db.cursor()


    @backoff(logger=logger)
    def query(self, sql: str):
        try:
            self.cursor.execute(sql, [])
        except psycopg2.OperationalError:
            self.logger.error(f'Нет соединение с БД: {dsl.get("dbname")}')
            self.connect()
            self.cursor.execute(sql, [])
        return self.cursor.fetchall()



class PostgresFilmWork(PostgresBase):

    def get_many(self, table_name: str, skip: int = 0, limit: int = 100):
        rows = self.query(
            f"""SELECT * FROM content.{table_name}
                ORDER BY id DESC
                LIMIT {limit} OFFSET {skip};""")
        return rows


dsl = {
    'host': '127.0.0.1',
    'port': 5432,
    'user': 'admin',
    'password': '22061941',
    'dbname': 'movies_database'
}

def start(pg_db, table_name, limit: int = 100):
    skip = 0
    while True:
        rows = pg_db.get_many(table_name=table_name, skip=skip, limit=limit)
        model = comeon.model(table_name)
        yield from (model(**row) for row in rows)
        if not rows:
            break
        skip += limit
        time.sleep(0.5)

if __name__ == "__main__":
    pg = PostgresFilmWork(dsl)
    for item in start(pg, 'person_film_work'):
        print(item.id)

