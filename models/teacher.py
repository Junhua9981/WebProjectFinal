from distutils.command.config import config
from typing import Optional, List, Dict, Union

from pydantic import BaseModel, EmailStr, Field

class GradeModel(BaseModel):
    grade: float
    graded_user_number: int
    graded_user: List[str]

class TeacherModel(BaseModel):
    name:str
    teaching_subject:list(str)
    department:str
    learned_grade:GradeModel
    stress_grade:GradeModel
    sweet_score:GradeModel
    comment:list(str)
    config = {
        "schema_extra": {
            "example": {
                "name": "George",
                "teaching_subject": ["Math", "English"],
                "department": "Computer Science",
                "learned_grade": {
                    "grade": 0.0,
                    "graded_user_number": 0,
                    "graded_user": []
                },
                "stress_grade": {
                    "grade": 0.0,
                    "graded_user_number": 0,
                    "graded_user": []
                },
                "sweet_score": {
                    "grade": 0.0,
                    "graded_user_number": 0,
                    "graded_user": []
                },
                "comment": []
            }
        }
    }


class UpdateTeacherModel(TeacherModel):
    pass