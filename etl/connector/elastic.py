from elasticsearch import Elasticsearch, helpers


class ElasticBase:

    def __init__(self, dsl: dict):
        self.dsl = dsl

    def __enter__(self):
        self.client = Elasticsearch(**self.dsl)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()


class ElasticMovies(ElasticBase):

    def set_bulk(self, index, data):
        helpers.bulk(self.client, self.generate_elastic_data(index, data))


    def generate_elastic_data(self, index, data):
        for item in data:
            print(item)
            yield {
                '_index': index,
                '_id': str(item.id),
                '_source': item.json()
            }


