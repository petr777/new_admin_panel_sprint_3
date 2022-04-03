from etl.connector.postgres import PostgresMovies
from etl.connector.elastic import ElasticMovies
from loguru import logger
from utility.backoff import backoff
import time
from etl.models import Movies
from collections import defaultdict
from itertools import groupby
import operator
from pprint import pprint
from enum import Enum

limit = 3

class Role(Enum):
    ACTOR = 'actor'
    WRITER = 'writer'
    DIRECTOR = 'director'

@backoff(logger=logger)
def extract(pg_db: PostgresMovies, table_name: str):
    state_date = pg_db.first_modified(table_name)
    for ids in pg_db.get_all_ids_gte_modified(table_name=table_name, state_date=state_date['modified'], limit=limit):
        ids = [k['id'] for k in ids]
        data = pg_db.get_data_from_elastic_movies(ids)
        yield data
        time.sleep(1)


def get_value(data):
    movie = dict()
    genre = set()
    writers_names = set()
    for item in data:
        movie['title'] = item['title']
        movie['description'] = item['description']
        movie['rating'] = item['rating']
        movie['type'] = item['type']
        movie['created'] = item['created']
        movie['modified'] = item['modified']

        if item.get('name'):
            genre.add(item['name'])

        if item.get('role'):
            print(item.get('role'), item.get('id'))

            #add_role_person(item.get('role'), data, item)


    movie['genre'] = genre
    movie['writers_names'] = writers_names

    pprint(movie)
    return movie


def transform(movies):
    result_list = []
    for fw_id, data in groupby(movies, key=operator.itemgetter("fw_id")):
        good = dict(
            {'id': fw_id},
            **get_value(data)
        )

        # good_dict.update(
        #     get_value('type', data)
        # )

        # day_dict.update({
        #     'title': d['title'] for d in data,
        # })
        # day_dict.update(
        #     {d['type']: d['role'] for d in data}
        # )
        result_list.append(good)

    print(result_list)


def run(pg_db, es_db):
    table_name = 'film_work'
    for movies in extract(pg_db, table_name):
        transform(movies)


if __name__ == '__main__':
    with PostgresMovies() as pg_db, ElasticMovies() as es_db:
        run(pg_db, es_db)