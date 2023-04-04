from fastapi import APIRouter
from fastapi.responses import JSONResponse
from jwt_manager import create_token

from models.user import User

user_router = APIRouter()

@user_router.post('/login', tags=['auth'])
def login(user: User):
    if user.email == 'jandresj1999@gmail.com' and user.password == 'contrasena':
        token:str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    return JSONResponse(status_code=400, content='The user or file do not exist')