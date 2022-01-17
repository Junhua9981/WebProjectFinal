from fastapi import Body, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext
from pydantic import BaseModel

from database.database import login_token, user_collection
from auth.jwt_handler import signJWT
from database.database import add_user
from models.user import UserModel, RegisterUserModel
from models.response import LoginFailResModel, LoginSucResModel, ResponseModel

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])

@router.post("/login")
async def user_login(user_credentials: HTTPBasicCredentials = Body(...)):
    # NEW CODE
    user = await user_collection.find_one({"email": user_credentials.username})
    if (user):
        password = hash_helper.verify(
            user_credentials.password, user["password"])
        if (password):
            tk = signJWT(user_credentials.username)
            await login_token(user_credentials.username, tk['access_token'])
            return LoginSucResModel("success", 200, "Logged In",  tk['access_token'] )

        return LoginFailResModel("Fail", 404,"Incorrect email or password")

    return LoginFailResModel("Fail", 404,"Incorrect email or password")

@router.post("/register")
async def user_signup(user: RegisterUserModel = Body(...)):
    user_exists = await user_collection.find_one({"email":  user.email})
    if(user_exists):
        return "Email already exists"
    
    user.password = hash_helper.encrypt(user.password)
    new_user = await add_user(jsonable_encoder(user))
    return new_user

class courseTable(BaseModel):
    courseTable: str
    token:str

@router.post("/courseTable")
async def post_courseTable(c: courseTable = Body(...)):
    user_exists = await user_collection.find_one({"token":  c.token})
    if(user_exists):
        await user_collection.update_one({"token":  c.token}, {"$set": {"courseTable": c.courseTable}})
        return ResponseModel("success",  "courseTable updated")
    
    return ResponseModel("Fail", "User not found")

@router.get("/courseTable")
async def get_courseTable(token:str):
    user_exists = await user_collection.find_one({"token": token})
    if(user_exists):
        return ResponseModel(user_exists["courseTable"], "success" )
    
    return ResponseModel("Fail", "User not found")