from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional

from jwt_manager import create_token
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routes.movie import movie_router

app = FastAPI()
app.tittle = 'Mi aplicación FastApi'
app.version = '0.0.1'

app.add_middleware(ErrorHandler)
app.include_router(movie_router)

Base.metadata.create_all(bind=engine)

class User(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "id": 0,
                "nombre": "Movie name",
                "Animador": "Animator name"
            }
        }
        
class Movie(BaseModel):
    id: Optional[int]=None
    nombre: str = Field(min_length=1, max_length=15)
    Animador: str = Field(min_length=1, max_length=15)

movies = [
    {
        "id": 1,
        "nombre": "mugen train",
        "Animador": "Funemi animation"
    },
    {
        "id": 2,
        "nombre": "Juan pieza",
        "Animador": "Funemi animation"
    }
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')


@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == 'jandresj1999@gmail.com' and user.password == 'contrasena':
        token:str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    return JSONResponse(status_code=400, content='The user or file do not exist')