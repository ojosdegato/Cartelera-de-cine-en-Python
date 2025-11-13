# app/schemas/pelicula.py
# Define los modelos Pydantic (BaseModel) para validación en la API

from pydantic import BaseModel, ConfigDict
from typing import List, Optional


# --- Esquema Base ---
# Campos comunes que se comparten al crear y leer.
# Corresponde 1 a 1 con how_to_do.md
class PeliculaBase(BaseModel):
    titulo: str
    duracion: int
    disponible: bool
    
    # Campos opcionales
    director: Optional[str] = None
    descripcion: Optional[str] = None
    trailer: Optional[str] = None
    productora: Optional[str] = None
    idioma: Optional[str] = None
    vose: Optional[bool] = None
    actores: Optional[List[str]] = None

# --- Esquema de Creación (POST /peliculas) ---
# Hereda de Base y añade campos necesarios solo al crear.
class PeliculaCreate(PeliculaBase):
    genero_id: int # Al crear, solo pasamos el ID del género

# --- Esquema de Actualización (PUT /peliculas/{id}) ---
# Todos los campos son opcionales para permitir actualizaciones parciales.
class PeliculaUpdate(BaseModel):
    titulo: Optional[str] = None
    duracion: Optional[int] = None
    disponible: Optional[bool] = None
    genero_id: Optional[int] = None
    director: Optional[str] = None
    descripcion: Optional[str] = None
    trailer: Optional[str] = None
    productora: Optional[str] = None
    idioma: Optional[str] = None
    vose: Optional[bool] = None
    actores: Optional[List[str]] = None

# --- Esquema de Lectura (GET /peliculas) ---
# Hereda de Base y añade campos que se devuelven desde la BBDD.
class PeliculaRead(PeliculaBase):
    id: int
    genero_id: int
    
    # Configuración para que Pydantic pueda leer desde el modelo ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)

# (Opcional pero recomendado: Schema para lectura con género anidado)
# Si quisieramos devolver el objeto género completo en lugar del ID:
#
# from .genero import GeneroRead # (Suponiendo que Kary crea este schema)
#
# class PeliculaReadWithGenero(PeliculaRead):
#     genero: GeneroRead

# Importar GeneroRead para el anidamiento
from .genero import GeneroRead
 
class PeliculaReadWithGenero(PeliculaRead):
    # Sobreescribe el campo de la base para incluir el objeto ORM cargado
    genero: GeneroRead