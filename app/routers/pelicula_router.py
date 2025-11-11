# app/routers/pelicula_router.py
# Define los endpoints de la API para el recurso 'Pelicula'

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.schemas.pelicula import PeliculaRead, PeliculaCreate, PeliculaUpdate
from app.services import pelicula_service # Importamos su lógica

# Creamos un router específico para películas
# Todos los endpoints aquí empezarán por /peliculas
router = APIRouter(
    prefix="/peliculas",
    tags=["Películas 🎬"] # Etiqueta para la documentación de FastAPI
)

# --- Endpoint para Añadir película (Servicio 1) ---
@router.post("/", response_model=PeliculaRead, status_code=status.HTTP_201_CREATED)
def create_pelicula(
    pelicula: PeliculaCreate, 
    db: Session = Depends(get_db)
):
    """
    Añade una nueva película a la cartelera.
    """
    # (Aquí podríamos añadir lógica de negocio, ej: verificar si el género existe)
    # db_genero = db.query(GeneroORM).filter(GeneroORM.id == pelicula.genero_id).first()
    # if not db_genero:
    #     raise HTTPException(status_code=404, detail="Género no encontrado")
        
    return pelicula_service.add_pelicula(db=db, pelicula=pelicula)

# --- Endpoint para Ver películas disponibles (Servicio 2) ---
@router.get("/disponibles/", response_model=List[PeliculaRead])
def read_peliculas_disponibles(db: Session = Depends(get_db)):
    """
    Obtiene una lista de todas las películas actualmente disponibles.
    """
    peliculas = pelicula_service.get_peliculas_disponibles(db=db)
    return peliculas

# --- Endpoint para Editar película (Servicio 5) ---
@router.put("/{pelicula_id}", response_model=PeliculaRead)
def update_pelicula_endpoint(
    pelicula_id: int,
    pelicula_update: PeliculaUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza los datos de una película existente por su ID.
    """
    db_pelicula = pelicula_service.update_pelicula(db, pelicula_id, pelicula_update)
    if db_pelicula is None:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return db_pelicula

# --- Endpoint para Eliminar película (Servicio 6) ---
@router.delete("/{pelicula_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pelicula_endpoint(
    pelicula_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina una película de la base de datos por su ID.
    """
    success = pelicula_service.delete_pelicula(db, pelicula_id)
    if not success:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    # No se devuelve contenido, solo el status 204