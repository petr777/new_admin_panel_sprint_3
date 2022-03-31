from utils.backoff import backoff
from utils import comehere
from loguru import logger
from config.settings import POSTGRES_DSL, SQLLITE_DB
from database.postgres import PostgresMovies
from database.sqlite import SQLiteMovies
from enum import Enum, auto


class ProcessState(Enum):
    LOADING = auto()
    PROCESSING = auto()
    SAVING = auto()
    EXECUDTED = auto()


@backoff(logger=logger)
def run(db, name, limit: int = 1000):
    model_data = comehere.model(name)
    skip = 0
    while True:
        items = db.get_many(table_name=name, skip=skip, limit=limit)
        yield from (model_data(**item) for item in items)
        if not items:
            break
        skip += limit

name = 'person_film_work'
with SQLiteMovies(SQLLITE_DB) as postgres_db:

    for row in run(postgres_db, name):
        print(row)

