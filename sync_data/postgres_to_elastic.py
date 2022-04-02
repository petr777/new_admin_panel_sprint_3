import time
from utils.backoff import backoff
from utils import comehere
from loguru import logger
from config.settings import POSTGRES_DSL, SQLLITE_DB
from database.postgres import PostgresMovies
from state.state import JsonFileStorage, State



def extract(db, name, state_date, limit: int = 10):
    skip = 0
    while True:
        film_works = db.get_ids_gte_modified(table_name=name, skip=skip, limit=limit, state_date=state_date)
        film_works_ids = [str(item.get('id')) for item in film_works]
        data = db.get_data_from_elastic_movies(film_works_ids)
        yield from data
        if not film_works:
            break
        skip += limit
        time.sleep(10)


def transform(movies):
    for movie in movies:




@backoff(logger=logger)
def run(db, name, state):
    state_date = state.get_state(name)

    if not state_date:
        state_date = db.first_modified(name)

    movies = extract(db, name, state_date)
    transform(movies)


    # for movies in extract(db, name, state_date):
    #     if state_date == str(movies.get('modified')):
    #         continue





name = 'film_work'
if __name__ == '__main__':
    storage = JsonFileStorage(f'state/{name}.json')
    state = State(storage)
    with PostgresMovies(POSTGRES_DSL) as db:
        run(db, name, state)
