import sys
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from auth.jwt_bearer import JWTBearer
# from routes.student import router as StudentRouter
# from routes.admin import router as AdminRouter
from routes.user import router as UserRouter
from routes.teacher import router as TeacherRouter
from routes.comments import router as CommentRouter
from routes.build_db import router as BuildDBRouter
from routes.view_teacher import router as ViewTeacherRouter
from decouple import config

app = FastAPI()

token_listener = JWTBearer()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:5501",
    "http://localhost:8080",
    "http://127.0.0.1:5501",
    "https://webprojfrontend.herokuapp.com"
]

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*']
)


JWT_SECRET = config('secret')
MOGO = config('MONGO_DETAILS')



@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to this fantastic app."}


# app.include_router(AdminRouter, tags=["Administrator"], prefix="/admin")
app.include_router(UserRouter, tags=["Users"], prefix="/user")
app.include_router(BuildDBRouter, tags=["BuildDB"], prefix="/build_db")
# app.include_router(StudentRouter, tags=["Students"], prefix="/student")
app.include_router(CommentRouter, tags=["Comments"], prefix="/comment")
app.include_router(TeacherRouter, tags=["Teachers"], prefix="/teacher", dependencies=[Depends(token_listener)])
app.include_router(ViewTeacherRouter, tags=["ViewTeachers"], prefix="/view_teacher")