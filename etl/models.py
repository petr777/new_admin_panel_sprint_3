import datetime
from typing import Optional, Union, List, Set
from uuid import UUID
from pydantic import BaseModel
from pydantic.fields import Field



class Person(BaseModel):
    id: UUID
    name: str

class Movies(BaseModel):
    id: UUID
    imdb_rating: Optional[float] = Field(alias='rating', default=0)
    genre: Set = set()
    title: str
    description: Optional[str]
    director: List[Person] = []
    actors: List[Person] = []
    actors_names: Set = set()
    writers: List[Person] = []
    writers_names: Set = set()

