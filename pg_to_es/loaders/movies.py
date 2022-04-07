from elasticsearch import helpers
from typing import List, Generator
from connectors.es_db import ElasticBase
from loguru import logger
from model import Movies

class ElasticMovies(ElasticBase):

    def generate_elastic_data(self, index, data: List[Movies]) -> Generator:
        for item in data:
            movie = {
                '_id': item.id,
                '_index': index,
                **item.dict(),
                'director': [p.name for p in item.director],
            }
            yield movie


    def save_bulk(self, index, data: List[Movies]) -> None:
        res, _ = helpers.bulk(
            self.client,
            self.generate_elastic_data(index, data)
        )
        logger.info(f'Синхронизированно записей {res}')
