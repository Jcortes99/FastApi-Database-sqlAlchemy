from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


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


@app.get('/movies', tags=['movies'])
def get_movies():
    return movies

@app.get('/movies/{id}')
def get_movie(id: int):
    for each_movie in movies:
        if each_movie["id"] == id:
            return each_movie["nombre"]
    return []

@app.get('/movies/', tags=['movies'])
def get_movies_by_categoriy(animator: str, id:int):
    for movie in movies:
        if movie["Animador"] == animator and movie["id"] == id:
            return movie["nombre"]
    return []