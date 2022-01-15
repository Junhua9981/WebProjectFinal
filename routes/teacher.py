from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from database.database import *
from models.teacher import *
from models.response import *

router = APIRouter()

@router.get("/{teacher_name}", response_description="Get Teacher Detail")
async def get_teacher_detail(teacher_name: str):
    teacher = await search_teacher(teacher_name)
    return ResponseModel(teacher, "Teacher data retrieved successfully") \
        if teacher \
        else ErrorResponseModel("An error occured", 404, "Teacher doesn't exist.")

@router.post("/{teacher_name}", response_description="Add Teacher Detail")
async def add_teacher(teacher_name: str):
    teacher = await add_teacher(teacher_name)
    return ResponseModel(teacher, "Teacher data added successfully") \
        if teacher \
        else ErrorResponseModel("An error occured", 404, "Teacher already exists.")

@router.put("/{teacher_name}", response_description="Modify Teacher Detail")
async def modify_teacher_detail(teacher_name: str, teacher_data: TeacherModel):
    teacher = await update_teacher(teacher_name, teacher_data)
    return ResponseModel(teacher, "Teacher data modified successfully") \
        if teacher \
        else ErrorResponseModel("An error occured", 404, "Teacher doesn't exist.")

@router.put("/comment/{teacher_name}", response_description="Modify Teacher Comment")
async def modify_teacher_comment(teacher_name: str, comment: str):
    teacher = await update_teacher_comment(teacher_name, comment)
    return ResponseModel(teacher, "Teacher comment modified successfully") \
        if teacher \
        else ErrorResponseModel("An error occured", 404, "Teacher doesn't exist.")
