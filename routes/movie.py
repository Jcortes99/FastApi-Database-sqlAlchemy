from fastapi import Body, Depends, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi.encoders import jsonable_encoder

from config.database import Session
from models.movie import Movie as MovieModel
from  middlewares.jwt_bearer import JWTBearer


movie_router = APIRouter()

class Movie(BaseModel):
    id: Optional[int]=None
    nombre: str = Field(min_length=1, max_length=15)
    Animador: str = Field(min_length=1, max_length=15)

@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.get('/movies/{id}', tags=['movies'])
def get_movie(id: int):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id==id).first()
    return JSONResponse(content=jsonable_encoder(result))

@movie_router.get('/movies/', tags=['movies'])
def get_movies_by_categoriy(animator: str,):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.Animador == animator)
    result = result.all()
    return JSONResponse(content=jsonable_encoder(result))

@movie_router.post('/movies', tags=['movies'], status_code=201)
def create_movie(movie:Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"result":"Successful", "insertion":movie.dict()})


@movie_router.put('/movies/{movie_id}', tags=['movies'])
def update_movie(movie_id: int, nombre: str = Body(), animator: str = Body()):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if result:
        result.nombre = nombre
        result.Animador= animator
        db.commit()
        return JSONResponse(status_code=201, content={'Message':'The row was update succesfuly'})
    return "The Id do not exist in the database"

@movie_router.delete('/movies/{movie_id}', tags=['movies'])
def delete_movie(movie_id: int):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if result:
        aux = result.dict()
        db.delete(result)
        db.commit()
        return JSONResponse(status_code=201, content={'Message':'The row was delete succesfuly', 'Item':aux})
    return "The Id do not exist in the database"