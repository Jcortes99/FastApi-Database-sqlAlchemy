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
        "nombre": "mugen train",
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