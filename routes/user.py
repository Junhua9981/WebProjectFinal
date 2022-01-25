from fastapi import Body, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext
from pydantic import BaseModel

from database.database import login_token, send_activate_mail, user_collection
from auth.jwt_handler import signJWT
from database.database import add_user
from database.mail import send_mail
from models.user import ActivateUserModel, UserModel, RegisterUserModel, ActivateCodeModel
from models.response import LoginFailResModel, LoginSucResModel, ResponseModel, ResModel

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])

@router.post("/login")
async def user_login(user_credentials: HTTPBasicCredentials = Body(...)):
    user = await user_collection.find_one({"email": user_credentials.username})
    if (user):
        if user.get('activated'):
            password = hash_helper.verify(
                user_credentials.password, user["password"])
            if (password):
                tk = signJWT(user_credentials.username)
                await login_token(user_credentials.username, tk['access_token'])
                return LoginSucResModel("success", 200, "Logged In",  tk['access_token'] )

            return LoginFailResModel("Fail", 404,"Incorrect email or password")
        else:
            return LoginFailResModel("Fail", 404, "Please activate your account")

    return LoginFailResModel("Fail", 404,"Incorrect email or password")

@router.post("/register")
async def user_signup(user: RegisterUserModel = Body(...)):
    user = await user_collection.find_one({"email":  user.email})
    if user and user.activated == False:
        user.password = hash_helper.encrypt(user.password)
        user.activated = True
        new_user = await add_user(jsonable_encoder(user))
        return new_user
    else :
        return ResModel("Fail", 404, "User already exists")

@router.get("/test")
async def test(email: str):
    await send_mail(email, "Here is your activate code" , "12345")
    return "sent"

@router.post("/getCode")
async def send_code(user: ActivateCodeModel = Body(...)):
    res = await send_activate_mail(user.email)
    if res:
        return ResModel("success", 200, "Activation code sent")
    else:
        return ResModel("Fail", 404, "User does not exist")

@router.post("/activate")
async def activate(user: ActivateUserModel = Body(...)):
    user_exists = await user_collection.find_one({"email":  user.email})
    if(user_exists):
        if(user_exists['activateCode'] == user.activateCode):
            await user_collection.update_one({"email":  user.email}, {"$set": {"activated": True, "password": hash_helper.encrypt(user.password)}})
            return ResModel("success", 200, "Activated")
        else:
            return ResModel("fail", 404, "Incorrect activate code")
    else:
        return ResModel("fail", 404, "User does not exist")

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