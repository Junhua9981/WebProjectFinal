from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Abdulazeez Abdulazeez Adeshina",
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


