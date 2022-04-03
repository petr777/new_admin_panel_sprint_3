from pydantic import BaseModel
from pydantic.fields import Field
from uuid import uuid4, UUID
from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, Field, FilePath
from pprint import pprint
import datetime





class Movies(BaseModel):
    #id: UUID = Field(default_factory=uuid4)
    film_work_id: UUID = Field(alias='fw_id')
    imdb_rating: Union[float, None] = Field(alias='rating', default=0.0)
    title: str
    description: Optional[str]
    genre: str = Field(alias='name')
    type: str
    id: UUID
    person_role: Optional[str] = Field(alias='role')
    person_full_name: Optional[str] = Field(alias='full_name')
    created: datetime.datetime
    modified: datetime.datetime



