from elasticsearch import Elasticsearch

class ElasticBase:

    def __init__(self, dsl: dict):
        self.dsl = dsl

    def __enter__(self):
        self.client = Elasticsearch(**self.dsl)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()


class ElasticMovies(ElasticBase):

    def create_(self, id: int, doc: dict):
        res = self.client.index(index="test-index", id=id, document=doc)
        return res['result']


dsl = {
    'hosts': ['http://localhost:9200'],
    'basic_auth': ('elastic', '22061941')
}
with ElasticMovies(dsl) as es:
    print(es.create_index(id=1, doc={'a': 1, 'b': 2}))

