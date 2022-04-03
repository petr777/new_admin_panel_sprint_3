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


class ElasticMovies(ElasticBase):




    def set_bulk(self, index, data):
        for doc in data:
            self.client.index(
                index=index, id=str(doc.id), document=doc.json()
            )



        # for row in self.generate_data(index, data):
        #     self.client.index(
        #         index=index, id=row., document=doc
        #     )
        #     print(row)


        # helpers.bulk(self.client, self.generate_elastic_data(index, data))


    def generate_data(self, index, data):
        for item in data:
            yield {
                '_index': index,
                '_id': str(item.id),
                '_source': item.json()
            }


