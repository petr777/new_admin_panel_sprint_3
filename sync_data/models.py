from uuid import uuid4, UUID
from datetime import datetime
from typing import Optional, Union, List
from pydantic import BaseModel, Field, FilePath


class Base(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created: Union[datetime, None] = Field(alias="created_at")
    modified: Union[datetime, None] = Field(alias="updated_at")

    class Config:
        allow_population_by_field_name = True


class Film_Work(Base):
    title: str
    description: Optional[str] = None
    creation_date: Optional[datetime] = None
    file_path: Optional[FilePath] = None
    rating: Union[float, None] = Field(default=0.0)
    type: str


class Genre(Base):
    name: str
    description: Union[str, None]


class Person(Base):
    full_name: str


class Person_Film_Work(Base):
    role: str
    film_work_id: UUID = Field(default_factory=uuid4)
    person_id: UUID = Field(default_factory=uuid4)


class Genre_Film_Work(Base):
    film_work_id: UUID = Field(default_factory=uuid4)
    genre_id: UUID = Field(default_factory=uuid4)


class ElasticMovies(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    imdb_rating: Optional[float] = Field(default=0.0)
    genre: Optional[str]
    title: Optional[str]
    description: Optional[str]
    director: Optional[List[str]]
    actors_names: Optional[List]
    writers_names: Optional[List]
    actors: Optional[List]
    writers: Optional[List]