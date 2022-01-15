from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class StudentModel(BaseModel):
    id: int
    name: str
    email: EmailStr

    # fullname: str = Field(...)
    # email: EmailStr = Field(...)
    # course_of_study: str = Field(...)
    # year: int = Field(...)
    # gpa: float = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "George",
                "email": "george@x.edu.com"
            }
        }


class UpdateStudentModel(StudentModel):

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "George",
                "email": "george@x.edu.com"
            }
        }

