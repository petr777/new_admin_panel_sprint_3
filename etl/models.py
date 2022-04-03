import datetime
from typing import Optional, List, Set
from uuid import UUID
from pydantic import BaseModel
from pydantic.fields import Field


class Movies(BaseModel):
    id: UUID = Field(alias='fw_id')
    # title: str
    # description: Optional[str]
    # rating: Optional[float]
    # type: str
    # created: datetime.datetime
    # modified: datetime.datetime
    # role: Optional[str]
    # person_id: Optional[UUID] = Field(alias='id')
    # person_name: Optional[str] = Field(alias='full_name')
    # genre_id: Optional[str] = Field(alias='genre_id')
    # genre_name: Optional[str] = Field(alias='name')