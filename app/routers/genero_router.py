# app/routers/genero_router.py
# Define los endpoints de la API para el recurso 'Genero'

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.db import get_db
from app.schemas.genero import GeneroRead, GeneroCreate, GeneroUpdate, GeneroReadWithPeliculas
from app.services import genero_service

router = APIRouter(
    prefix="/generos",
    tags=["Géneros 🎭"] # Etiqueta para la documentación de FastAPI
)

@router.post("/", response_model=GeneroRead, status_code=status.HTTP_201_CREATED)
def create_genero_endpoint(
    genero: GeneroCreate, 
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo género (ej: Acción, Comedia, Drama).
    """
    db_genero = genero_service.get_genero_by_nombre(db, nombre=genero.nombre)
    if db_genero:
        raise HTTPException(status_code=400, detail="El nombre del género ya existe")
    return genero_service.create_genero(db=db, genero=genero)

@router.get("/", response_model=List[GeneroRead])
def read_all_generos(db: Session = Depends(get_db)):
    """
    Obtiene una lista de todos los géneros.
    """
    return genero_service.get_all_generos(db=db)

@router.get("/{genero_id}", response_model=GeneroReadWithPeliculas)
def read_genero_by_id_with_peliculas(
    genero_id: int, 
    db: Session = Depends(get_db)
):
    """
    Obtiene un género específico por su ID, incluyendo 
    la lista de películas asociadas a él.
    """
    # Usamos el servicio optimizado
    db_genero = genero_service.get_genero_with_peliculas(db, genero_id)
    if db_genero is None:
        raise HTTPException(status_code=404, detail="Género no encontrado")
    return db_genero

@router.put("/{genero_id}", response_model=GeneroRead)
def update_genero_endpoint(
    genero_id: int,
    genero_update: GeneroUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza un género por su ID.
    """
    db_genero = genero_service.update_genero(db, genero_id, genero_update)
    if db_genero is None:
        raise HTTPException(status_code=404, detail="Género no encontrado")
    return db_genero

@router.delete("/{genero_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_genero_endpoint(
    genero_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina un género por su ID.
    """
    success = genero_service.delete_genero(db, genero_id)
    if not success:
        raise HTTPException(status_code=404, detail="Género no encontrado")