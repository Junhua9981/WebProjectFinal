from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from database.database import *
from models.comments import *
from models.response import *

router = APIRouter()

@router.get("/", response_description="Get Comment")
async def get_comment():
    comment = await retrieve_recent_comment()
    return CommentResposeModel(comment) \
        if comment \
        else ErrorResponseModel("An error occured", 404, "Comment doesn't exist.")