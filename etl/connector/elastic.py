import json

from elasticsearch import Elasticsearch, helpers
from etl.settings import ELASTIC_DSL

class ElasticBase:

    def __init__(self):
        self.dsl = ELASTIC_DSL

    def __enter__(self):
        self.client = Elasticsearch(**self.dsl)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()


class ElasticMovies(ElasticBase):

    def set_bulk(self, index, data):
        # for row in self.generate_elastic_data(index, data):
        #     print(row)
        return helpers.bulk(self.client, self.generate_elastic_data(index, data))


    def generate_elastic_data(self, index, data: list):
        for item in data:
            _id = str(item.id)
            yield {
                '_index': index,
                '_id': _id,
                '_source': item.json()
            }


