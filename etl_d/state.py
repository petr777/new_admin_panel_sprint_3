import abc
from typing import Any, Optional
import json
from pathlib import Path


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass

class RedisStorage(BaseStorage):

    def __init__(self, redis_adapter):
        self.redis_adapter = redis_adapter

    def save_state(self, state: dict) -> None:
        self.redis_adapter.set('data', json.dumps(state))

    def retrieve_state(self) -> dict:
        value = self.redis_adapter.get('data')
        if not value:
            return {}
        return json.loads(value)


class JsonFileStorage(BaseStorage):

    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path
        Path(self.file_path).touch()


    def save_state(self, state: dict) -> None:
        with open(self.file_path, 'w') as f:
            j = json.dumps(state)
            f.write(j)

    def retrieve_state(self) -> dict:
        with open(self.file_path, 'r') as f:
            content = f.read()
            if not content:
                return {}
            return json.loads(content)

class State:
    """
    Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение на работу с БД или распределённым хранилищем.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        self.storage.save_state({key: value})

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу"""
        state = self.storage.retrieve_state()
        if key in state.keys():
            return state[key]
        return None

