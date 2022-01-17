from pydantic import BaseModel, Field, EmailStr

class RegisterUserModel(BaseModel):
    email: EmailStr
    password: str


class UserModel(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
    token: str 
    class Config:
        schema_extra = {
            "example": {
                "email": "abdulazeez@x.com",
                "password": "Yourpasswordgoes here."
            }
        }

class UpdateUserModel(UserModel):

    class Config:
        schema_extra = {
            "example": {
                "name": "Abdulazeez Abdulazeez Adeshina",
                "email": "user@usr.com",
                "password": "Yourpasswordgoes here."
            }
        }


