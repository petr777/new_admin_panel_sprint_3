from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['http://localhost:9200'],
    basic_auth=('elastic', '22061941'),
)
print(es.info())