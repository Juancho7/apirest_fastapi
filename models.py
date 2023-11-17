from pydantic import BaseModel
from typing import Optional


class Book(BaseModel):
    id: Optional[int]
    title: str
    author: str
    release_year: int
