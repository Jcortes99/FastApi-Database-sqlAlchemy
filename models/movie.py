from config.database import Base
from sqlalchemy import Column, Integer, String, Float

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key = True)
    nombre = Column(String, nullable=False)
    Animador = Column(String, nullable=False)