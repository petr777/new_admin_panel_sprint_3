import operator
from enum import Enum
from itertools import groupby
from typing import List, Dict


class Role(Enum):
    ACTOR = 'actor'
    WRITER = 'writer'
    DIRECTOR = 'director'

    @staticmethod
    def list():
        return list(map(lambda r: r.value, Role))


class Transformation:

    def groupby(self, data, _id):
        data = sorted(data, key=operator.itemgetter(_id))
        for _id, new_data in groupby(data, key=operator.itemgetter(_id)):
            yield _id, list(new_data)

    def fetch_by_filter(
            self, data: List[Dict],
            field: str,
            key: str,
            filter: str):

        result = [item for item in data if item[field] == key]
        result = list({v[filter]: v for v in result}.values())
        return result

    def uniq_by_key(self, data: List[Dict], filter: str):
        result = list({v[filter]: v for v in data}.values())
        return [item[filter] for item in result]
