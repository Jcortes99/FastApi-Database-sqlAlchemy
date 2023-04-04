from fastapi import Body, Depends, APIRouter
from fastapi.responses import JSONResponse
from typing import List
from fastapi.encoders import jsonable_encoder

from config.database import Session
from models.movie import Movie as MovieModel
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie


movie_router = APIRouter()

@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.get('/movies/{id}', tags=['movies'])
def get_movie(id: int):
    db = Session()
    result = MovieService(db).get_movie(id)
    if result:
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    return JSONResponse(status_code=400, content={"message":"Id do not exist"})

@movie_router.get('/movies/', tags=['movies'])
def get_movies_by_categoriy(animator: str,):
    db = Session()
    if result:
        result = MovieService(db).get_movie_by_category(animator)
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    return JSONResponse(status_code=400, content={"message":"The animator was not found"})

@movie_router.post('/movies', tags=['movies'], status_code=201)
def create_movie(movie:Movie) -> dict:
    db = Session()
    new_movie = MovieService(db).create_movie(movie)
    if new_movie:
        db.add(new_movie)
        db.commit()
        return JSONResponse(status_code=201, content={"result":"Successful", "insertion":movie.dict()})
    return JSONResponse(status_code=400, content={"message":"Error creating the new movie row"})


@movie_router.put('/movies/{movie_id}', tags=['movies'])
def update_movie(movie_id: int, nombre: str = Body(), animator: str = Body()):
    db = Session()
    result = MovieService(db).get_movie(movie_id)
    if result:
        aux = jsonable_encoder(result)
        result.nombre = nombre
        result.Animador= animator
        db.commit()
        return JSONResponse(status_code=201, content={'Message':'The row was update succesfuly', 'Item':aux})
    return "The Id do not exist in the database"

@movie_router.delete('/movies/{movie_id}', tags=['movies'])
def delete_movie(movie_id: int):
    db = Session()
    result = MovieService(db).get_movie(movie_id)
    if result:
        aux = jsonable_encoder(result)
        db.delete(result)
        db.commit()
        return JSONResponse(status_code=200, content={'Message':'The row was delete succesfuly', 'Item':aux})
    return "The Id do not exist in the database"