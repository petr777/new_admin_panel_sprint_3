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
    pass


