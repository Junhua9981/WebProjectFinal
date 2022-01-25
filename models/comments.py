from sqlite3 import Timestamp
from pydantic import BaseModel, Field, EmailStr

class CommentModel(BaseModel):
    comment: str = Field(...)
    name: str = Field(...)
    timestamp: Timestamp = Field(...)
    course: str = Field(...)