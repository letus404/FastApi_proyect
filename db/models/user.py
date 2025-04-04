### User model ###

from pydantic import BaseModel, Field  # Base para crear modelos de datos en FastAPI
from typing import Optional  # Para definir campos opcionales

# Definición del modelo de datos para un usuario
class User(BaseModel):
    id: Optional[str] = None 
    username: str 
    email: str
