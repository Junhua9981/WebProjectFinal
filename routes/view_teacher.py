from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from database.database import *
from models.teacher import *
from models.response import *

router = APIRouter()


@router.get("/", response_description="Teachers retrieved")
async def get_teacher():
    students = await retrieve_teacher()
    return ResponseModel(students, "Teachers data retrieved successfully") \
        if len(students) > 0 \
        else ResponseModel(
        students, "Empty list returned")