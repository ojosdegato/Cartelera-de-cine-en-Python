# app/models/genero.py
# Define la tabla 'generos' en la BBDD

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.db import Base # Importamos la Base declarativa
from typing import List, TYPE_CHECKING

# Importación de tipo para la relación bidireccional
if TYPE_CHECKING:
    from .pelicula import PeliculaORM

class GeneroORM(Base):
    __tablename__ = "generos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # --- Columnas Requeridas (según how_to_do.md) ---
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    
    # --- Columna Opcional ---
    descripcion: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # --- Relación Bidireccional (Lado "One") ---
    # Esto cumple con "RELACION Bidireccional Pelicula a Genero ManyToOne" 
    # Define la colección de películas que pertenecen a este género.
    # 'back_populates="genero"' es el vínculo mágico que lo conecta 
    # con el atributo 'genero' en PeliculaORM.
    peliculas: Mapped[List["PeliculaORM"]] = relationship(
        back_populates="genero",
        cascade="all, delete-orphan" # Opcional: si borro un género, borra sus películas
    )

    def __repr__(self):
        return f"<Genero(id={self.id}, nombre='{self.nombre}')>"