# app/services/pelicula_service.py
# Lógica de negocio (CRUD) para el módulo de Películas

from sqlalchemy.orm import Session
from app.models.pelicula import PeliculaORM
from app.schemas.pelicula import PeliculaCreate, PeliculaUpdate
from typing import List, Optional

# --- Servicio 1: Añadir película ---
def add_pelicula(db: Session, pelicula: PeliculaCreate) -> PeliculaORM:
    """
    Añade una nueva película a la base de datos.
    """
    # Convertimos el schema Pydantic a un objeto ORM
    db_pelicula = PeliculaORM(**pelicula.model_dump())
    
    db.add(db_pelicula)
    db.commit()
    db.refresh(db_pelicula) # Refrescamos para obtener el ID asignado
    return db_pelicula

# --- Servicio 2: Ver películas disponibles ---
def get_peliculas_disponibles(db: Session) -> List[PeliculaORM]:
    """
    Devuelve una lista de todas las películas marcadas como 'disponible'.
    """
    return db.query(PeliculaORM).filter(PeliculaORM.disponible == True).all()

# --- Servicio 3 (Implícito): Ver todas las películas ---
def get_all_peliculas(db: Session) -> List[PeliculaORM]:
    """
    Devuelve todas las películas, disponibles o no.
    """
    return db.query(PeliculaORM).all()

# --- Servicio 4 (Implícito): Ver una película por ID ---
def get_pelicula_by_id(db: Session, pelicula_id: int) -> Optional[PeliculaORM]:
    """
    Busca una película por su ID.
    """
    return db.query(PeliculaORM).filter(PeliculaORM.id == pelicula_id).first()

# --- Servicio 5: Editar película ---
def update_pelicula(db: Session, pelicula_id: int, pelicula_update: PeliculaUpdate) -> Optional[PeliculaORM]:
    """
    Actualiza una película existente en la BBDD.
    """
    db_pelicula = get_pelicula_by_id(db, pelicula_id)
    
    if not db_pelicula:
        return None # Película no encontrada
        
    # Obtenemos los datos del update, excluyendo los que no se pasaron (None)
    update_data = pelicula_update.model_dump(exclude_unset=True)
    
    # Aplicamos las actualizaciones
    for key, value in update_data.items():
        setattr(db_pelicula, key, value)
        
    db.commit()
    db.refresh(db_pelicula)
    return db_pelicula

# --- Servicio 6: Eliminar película ---
def delete_pelicula(db: Session, pelicula_id: int) -> bool:
    """
    Elimina una película de la BBDD. Devuelve True si se eliminó.
    """
    db_pelicula = get_pelicula_by_id(db, pelicula_id)
    
    if db_pelicula:
        db.delete(db_pelicula)
        db.commit()
        return True
    return False
