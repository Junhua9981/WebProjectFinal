from fastapi import Body, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext

from database.database import user_collection
from auth.jwt_handler import signJWT
from database.database import add_user
from models.user import UserModel
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
            return LoginSucResModel("success", 200, "Logged In",  signJWT(user_credentials.username) )

        return LoginFailResModel("Fail", 404,"Incorrect email or password")

    return LoginFailResModel("Fail", 404,"Incorrect email or password")

@router.post("/register")
async def user_signup(user: UserModel = Body(...)):
    user_exists = await user_collection.find_one({"email":  user.email})
    if(user_exists):
        return "Email already exists"
    
    user.password = hash_helper.encrypt(user.password)
    new_user = await add_user(jsonable_encoder(user))
    return new_user