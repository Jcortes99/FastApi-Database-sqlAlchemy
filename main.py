from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder

from jwt_manager import create_token, validate_token
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel

app = FastAPI()
app.tittle = 'Mi aplicación FastApi'
app.version = '0.0.1'

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'jandresj1999@gmail.com':
            raise HTTPException(status_code=403, detail='Invalid inputs')
        

class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int]=None
    nombre: str = Field(min_length=1, max_length=15)
    Animador: str = Field(min_length=1, max_length=15)
    
    class Config:
        schema_extra = {
            "example": {
                "id": 0,
                "nombre": "Movie name",
                "Animador": "Animator name"
            }
        }

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


@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == 'jandresj1999@gmail.com' and user.password == 'contrasena':
        token:str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    return JSONResponse(status_code=400, content='The user or file do not exist')

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id==id).first()
    return JSONResponse(content=jsonable_encoder(result))

@app.get('/movies/', tags=['movies'])
def get_movies_by_categoriy(animator: str,):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.Animador == animator)
    result = result.all()
    return JSONResponse(content=jsonable_encoder(result))

@app.post('/movies', tags=['movies'], status_code=201)
def create_movie(movie:Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"result":"Successful", "insertion":movie.dict()})

@app.put('/movies/{movie_id}', tags=['movies'])
def update_movie(movie_id: int, nombre: str = Body(), animator: str = Body()):
    for movie in movies:
        if movie["id"] == movie_id:
            movie['nombre'] = nombre
            movie['Animador'] = animator
            movie['modify'] = "True"
        return 'Succesful Update'
    return "The Id do not exist in the database"

@app.delete('/movies/{movie_id}', tags=['movies'])
def delete_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            movies.remove(movie)
            return f"The movie with the id {movie_id} was succesfuly delete"
    return "The Id do not exist in the database"