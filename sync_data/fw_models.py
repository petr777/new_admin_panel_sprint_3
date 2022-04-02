from uuid import uuid4, UUID
from typing import Optional, List
from pydantic import BaseModel, Field


class ElasticMovies(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    imdb_rating: Optional[float] = Field(default=0.0)
    #genre: str
    title: Optional[str]
    # description: Optional[str]
    # director: Optional[List[str]]
    # actors_names: Optional[List]
    # writers_names: Optional[List]
    # actors: Optional[List]
    # writers: Optional[List]