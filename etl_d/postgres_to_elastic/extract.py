from etl_d.connector.postgres import PostgresMovies
from etl_d.connector.elastic import ElasticMovies
from etl_d.state import JsonFileStorage, State
from etl_d.settings import POSTGRES_DSL, ELASTIC_DSL
from loguru import logger
from utility.backoff import backoff
import time
from models import Movies

def extract(db, name, state_date, limit: int = 10):
    skip = 0
    while True:
        film_works = db.get_ids_gte_modified(
            table_name=name, skip=skip, limit=limit, state_date=state_date
        )
        if not film_works:
            break
        film_works_ids = [str(item.get('id')) for item in film_works]
        data = db.get_data_from_elastic_movies(film_works_ids)
        yield data
        skip += limit
        #time.sleep(10)


def transform(data):
    for movies in data:
        yield [Movies(**dict(movie)) for movie in movies]

total = 0

def load(elastic_db, data):
    for movies in data:
        elastic_db.set_bulk('movies', movies)


#@backoff(logger=logger)
def run(db, elastic_db, name, state):

    state_date = state.get_state(name)

    if not state_date:
        state_date = db.first_modified(name)

    data = extract(db, name, state_date)
    data = transform(data)
    data = load(elastic_db, data)


name = 'film_work'

if __name__ == '__main__':
    storage = JsonFileStorage(f'{name}.json')
    state = State(storage)
    with PostgresMovies(POSTGRES_DSL) as db, ElasticMovies(ELASTIC_DSL) as elastic_db:
        run(db, elastic_db, name, state)
