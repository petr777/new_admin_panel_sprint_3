from connector.postgres import PostgresMovies
from connector.elastic import ElasticMovies
from loguru import logger
from utility.backoff import backoff
import time
from etl.models import Movies
from collections import defaultdict

limit = 2

@backoff(logger=logger)
def extract(pg_db: PostgresMovies, table_name: str):
    state_date = pg_db.first_modified(table_name)
    for ids in pg_db.get_all_ids_gte_modified(table_name=table_name, state_date=state_date, limit=limit):
        ids = [_id for _id, modified in ids]
        data = pg_db.get_data_from_elastic_movies(ids)
        yield data
        time.sleep(1)

def transform(movies):
    result = defaultdict(dict)
    for item in movies:
        movie = Movies(**item)
        data = result[movie.id]


        genre_name = movie.genre_name
        if genre_name and genre_name not in data.genres_names:
            genre = Genre(id=movie.genre_id, name=genre_name)
            data.genres_names.append(genre_name)
            data.genres.append(genre)

    print(result)
    print('#####')

        # genre_name = movie.genre_name
        # print(genre_name)
        #
        # if genre_name:
        #     #genre = Genre(id=mv.genre_id, name=genre_name)
        #     data.genres_names.append(genre_name)
        #     data.genres.append(genre)
        #
        #
        # print(movie.json())


def run(pg_db, es_db):
    table_name = 'film_work'
    for data in extract(pg_db, table_name):
        transform(data)


if __name__ == '__main__':
    with PostgresMovies() as pg_db, ElasticMovies() as es_db:
        run(pg_db, es_db)