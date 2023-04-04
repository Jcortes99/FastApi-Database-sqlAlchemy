
from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "mail@mail.com",
                "password": "password"
            }
        }