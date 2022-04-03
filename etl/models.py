import datetime
from typing import Optional, List, Set
from uuid import UUID
from pydantic import BaseModel
from pydantic.fields import Field
import datetime
from typing import Optional, List, Set
from uuid import UUID

from pydantic import BaseModel
from pydantic.fields import Field




#
# class FilmElastick(BaseModel):
#     id: str = Field(alias='fw_id')
#     title: str
#     description: Optional[str]
#     imdb_rating: Optional[float] = Field(alias='rating', default=0)
#     actors: List[Person] = []
#     actors_names: Set = set()
#     writers: List[Person] = []
#     writers_names: Set = set()
#     directors: List[Person] = []
#     directors_names: Set = set()
#     genres: List[Genre] = []
#     genres_names: List = []



# class Person(BaseModel):
#     id: str
#     name: str = Field(alias='full_name')
#
#
# class PersonRaw(Person):
#     role_raw: Optional[str] = Field(alias='role')
#     film_work_id: Optional[str]
#
#
# class PersonElastic(Person):
#     name: str
#     role: Set[str] = set()
#     film_ids: Set[str] = set()
#
#
# class Genre(BaseModel):
#     id: str
#     name: str
#
#
# class GenreRaw(Genre):
#     description: Optional[str]
#     film_work_id: str
#
#
# class GenreElastic(Genre):
#     description: Optional[str]
#     film_ids: Set[str] = set()
#
#
# class FilmElastick(BaseModel):
#     id: str = Field(alias='fw_id')
#     title: str
#     description: Optional[str]
#     imdb_rating: Optional[float] = Field(alias='rating', default=0)
#     actors: List[Person] = []
#     actors_names: Set = set()
#     writers: List[Person] = []
#     writers_names: Set = set()
#     directors: List[Person] = []
#     directors_names: Set = set()
#     genres: List[Genre] = []
#     genres_names: List = []
#
class Movies(BaseModel):
    id: UUID = Field(alias='fw_id')
    title: str
    description: Optional[str]
    rating: Optional[float]
    type: str
    created: datetime.datetime
    modified: datetime.datetime
    role: Optional[str]
    person_id: Optional[UUID] = Field(alias='id')
    person_name: Optional[str] = Field(alias='full_name')
    genre_id: Optional[str] = Field(alias='genre_id')
    genre_name: Optional[str] = Field(alias='name')