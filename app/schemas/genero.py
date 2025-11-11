# app/schemas/genero.py
# Define los modelos Pydantic (BaseModel) para validación en la API

from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# --- Esquema Base ---
# Campos que definen un género
class GeneroBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

# --- Esquema de Creación (POST /generos) ---
class GeneroCreate(GeneroBase):
    pass # Es idéntico al Base en este caso

# --- Esquema de Actualización (PUT /generos/{id}) ---
class GeneroUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

# --- Esquema de Lectura (GET /generos) ---
class GeneroRead(GeneroBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# --- Esquema de Lectura Avanzado (Opcional) ---
# Muy útil: Muestra un género Y todas las películas asociadas a él.
# Necesita Pydantic v2 para manejar bien las referencias cíclicas.
# (Importamos PeliculaRead 'lazy' para evitar importación circular)

from .pelicula import PeliculaRead # Aseguramos importación

class GeneroReadWithPeliculas(GeneroRead):
    peliculas: List[PeliculaRead] = []