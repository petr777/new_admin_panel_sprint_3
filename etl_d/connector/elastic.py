from elasticsearch import Elasticsearch, helpers
import json

class ElasticBase:

    def __init__(self, dsl: dict):
        self.dsl = dsl

    def __enter__(self):
        self.client = Elasticsearch(**self.dsl)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()