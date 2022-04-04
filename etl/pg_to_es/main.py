from etl.connector.postgres import PostgresMovies
from etl.connector.elastic import ElasticMovies
from loguru import logger
from utility.backoff import backoff
from etl.models import Movies, Person
from itertools import groupby
import operator
from enum import Enum

limit = 300
total = []

class Role(Enum):
    ACTOR = 'actor'
    WRITER = 'writer'
    DIRECTOR = 'director'


@backoff(logger=logger)
def extract(pg_db: PostgresMovies, table_name: str):
    state_date = pg_db.first_modified(table_name)
    for ids in pg_db.get_all_ids_gte_modified(table_name=table_name, state_date=state_date['modified'], limit=limit):
        global total
        ids = [k['id'] for k in ids]
        data = pg_db.get_data_from_elastic_movies(ids)
        yield data


def get_value(data):
    movie = dict()
    genres = set()
    writers = list()
    writers_names = set()
    actors = list()
    actors_names = set()
    directors = list()
    directors_names = set()
    for item in data:
        movie['title'] = item['title']
        movie['description'] = item['description']
        movie['rating'] = item['rating']
        movie['type'] = item['type']
        movie['created'] = item['created']
        movie['modified'] = item['modified']

        if item.get('name'):
            genres.add(item['name'])

        if item.get('role') == Role.DIRECTOR.value:
            p = Person(**{
                'id': item.get('id'),
                'name': item.get('full_name')
            })
            directors.append(p)
            directors_names.add(item.get('full_name'))

        if item.get('role') == Role.WRITER.value:
            p = Person(**{
                'id': item.get('id'),
                'name': item.get('full_name')
            })
            writers.append(p)
            writers_names.add(item.get('full_name'))

        if item.get('role') == Role.ACTOR.value:
            p = Person(**{
                'id': item.get('id'),
                'name': item.get('full_name')
            })
            actors.append(p)
            actors_names.add(item.get('full_name'))

    movie['genre'] = genres
    movie['writers'] = [i for n, i in enumerate(writers) if i not in writers[n + 1:]]
    movie['writers_names'] = writers_names

    movie['actors'] = [i for n, i in enumerate(actors) if i not in actors[n + 1:]]
    movie['actors_names'] = actors_names

    movie['director'] = [i for n, i in enumerate(directors) if i not in directors[n + 1:]]
    movie['directors_names'] = directors_names

    return movie


def transform(movies):
    movies = sorted(movies, key=operator.itemgetter('fw_id'))
    movies_from_es = []
    for fw_id, data in groupby(movies, key=operator.itemgetter("fw_id")):
        item = dict(
            {'id': fw_id},
            **get_value(data)
        )
        mv = Movies(**item)
        movies_from_es.append(mv)
    return movies_from_es


def load(data, es_db):
    for res in es_db.set_bulk('movies', data):
        print(res)


def run(pg_db, es_db):
    table_name = 'film_work'
    for movies in extract(pg_db, table_name):
        data = transform(movies)
        load(data, es_db)

if __name__ == '__main__':
    with PostgresMovies() as pg_db, ElasticMovies() as es_db:
        run(pg_db, es_db)