from models.movie import Movie
from schemas.movie import Movie as MovieSchema

class MovieService():
    
    def __init__(self, db) -> None:
        self.db = db
        
    def get_movies(self):
        result = self.db.query(Movie).all()
        return result
    
    def get_movie(self, id):
        result = self.db.query(Movie).filter(Movie.id==id).first()
        return result
    
    def get_movie_by_category(self, animator):
        result = self.db.query(Movie).filter(Movie.Animador == animator).all()
        return result
    
    def create_movie(self,data:MovieSchema):
        result = Movie(**data.dict())
        return result