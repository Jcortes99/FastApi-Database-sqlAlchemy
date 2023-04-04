from typing import Optional
from pydantic import BaseModel, Field

class Movie(BaseModel):
    id: Optional[int]=None
    nombre: str = Field(min_length=1, max_length=15)
    Animador: str = Field(min_length=1, max_length=15)
    class Config:
        schema_extra = {
            "example": {
                "id": 0,
                "nombre": "juanito",
                "Animador": "pablito"
            }
        }