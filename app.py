from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from auth.jwt_bearer import JWTBearer
from routes.student import router as StudentRouter
from routes.admin import router as AdminRouter
from routes.user import router as UserRouter
from routes.teacher import router as TeacherRouter
from decouple import config

app = FastAPI()

token_listener = JWTBearer()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


JWT_SECRET = config('secret')
MOGO = config('MONGO_DETAILS')

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to this fantastic app.{MOGO}"}


app.include_router(AdminRouter, tags=["Administrator"], prefix="/admin")
app.include_router(UserRouter, tags=["Users"], prefix="/user")
# app.include_router(StudentRouter, tags=["Students"], prefix="/student", dependencies=[Depends(token_listener)])
app.include_router(TeacherRouter, tags=["Teachers"], prefix="/teacher", dependencies=[Depends(token_listener)])