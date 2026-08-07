from pydantic import BaseModel
from typing import Optional


class NoteCreate(BaseModel):
    title: str
    body: str
    category_id: Optional[int] = None


class UserCreate(BaseModel):
    username: str
    password: str