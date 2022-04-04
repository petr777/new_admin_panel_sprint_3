import requests
from requests.auth import HTTPBasicAuth

headers = {
    'Content-Type': 'application/json',
}

json_data = {
    'settings': {
        'refresh_interval': '1s',
        'analysis': {
            'filter': {
                'english_stop': {
                    'type': 'stop',
                    'stopwords': '_english_',
                },
                'english_stemmer': {
                    'type': 'stemmer',
                    'language': 'english',
                },
                'english_possessive_stemmer': {
                    'type': 'stemmer',
                    'language': 'possessive_english',
                },
                'russian_stop': {
                    'type': 'stop',
                    'stopwords': '_russian_',
                },
                'russian_stemmer': {
                    'type': 'stemmer',
                    'language': 'russian',
                },
            },
            'analyzer': {
                'ru_en': {
                    'tokenizer': 'standard',
                    'filter': [
                        'lowercase',
                        'english_stop',
                        'english_stemmer',
                        'english_possessive_stemmer',
                        'russian_stop',
                        'russian_stemmer',
                    ],
                },
            },
        },
    },
    'mappings': {
        'dynamic': 'strict',
        'properties': {
            'id': {
                'type': 'keyword',
            },
            'imdb_rating': {
                'type': 'float',
            },
            'genre': {
                'type': 'keyword',
            },
            'title': {
                'type': 'text',
                'analyzer': 'ru_en',
                'fields': {
                    'raw': {
                        'type': 'keyword',
                    },
                },
            },
            'description': {
                'type': 'text',
                'analyzer': 'ru_en',
            },
            'director': {
                'type': 'text',
                'analyzer': 'ru_en',
            },
            'actors_names': {
                'type': 'text',
                'analyzer': 'ru_en',
            },
            'writers_names': {
                'type': 'text',
                'analyzer': 'ru_en',
            },
            'actors': {
                'type': 'nested',
                'dynamic': 'strict',
                'properties': {
                    'id': {
                        'type': 'keyword',
                    },
                    'name': {
                        'type': 'text',
                        'analyzer': 'ru_en',
                    },
                },
            },
            'writers': {
                'type': 'nested',
                'dynamic': 'strict',
                'properties': {
                    'id': {
                        'type': 'keyword',
                    },
                    'name': {
                        'type': 'text',
                        'analyzer': 'ru_en',
                    },
                },
            },
        },
    },
}


basic = HTTPBasicAuth('elastic', '22061941')
response = requests.put('http://127.0.0.1:9200/movies', headers=headers, json=json_data, auth=basic)

print(response.json())



# from pprint import pprint
#
#
# pprint({'_index': 'movies', '_id': '92f246d5-c125-4362-b380-2a993f975757', '_source': '{"id": "92f246d5-c125-4362-b380-2a993f975757", "imdb_rating": 6.5, "genre": ["Drama", "Family"], "title": "The Christmas Star", "description": "Horace McNickle (Edward Asner) is a two-time felon serving prison time for counterfeiting. On the week before Christmas, he escapes from prison dressed as Santa Claus due to his uncanny resemblance to St. Nick resulting from his long white beard and heavyset features. McNickle hides out from the police in a nearby suburban neighborhood where he is befriended and helped by two local children who think he is the real Santa Claus. McNickle takes advantage of the kids naivety to help him get his counterfeit money hidden somewhere in a local department store while he develops kind-hearted feelings for his two con victims that make him slowly understand the true nature of Christmas.", "director": "Alan Shapiro", "actors": [{"id": "81b3b0d6-81d9-45aa-a90b-614978cf7b29", "full_name": "Rene Auberjonois"}, {"id": "ac3ed300-a7e4-42bb-8cfc-1c7fd5e74357", "full_name": "Jim Metzler"}, {"id": "eac1449e-09ed-4912-8467-fba3d489c6bb", "full_name": "Edward Asner"}, {"id": "f531412e-cee1-4b39-9715-d3659fdfc69e", "full_name": "Susan Tyrrell"}], "actors_names": ["Rene Auberjonois", "Edward Asner", "Jim Metzler", "Susan Tyrrell"], "writers": [{"id": "d2fb411a-eb9a-4c96-888d-7e22468b1b08", "full_name": "Alan Shapiro"}, {"id": "b07edee7-1b23-40c3-be1a-30486bbeda78", "full_name": "Carol Dysinger"}], "writers_names": ["Carol Dysinger", "Alan Shapiro"]}'})
