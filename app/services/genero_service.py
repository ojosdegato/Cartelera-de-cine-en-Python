# app/services/genero_service.py
# Lógica de negocio (CRUD) para el módulo de Géneros

from sqlalchemy.orm import Session, joinedload
from app.models.genero import GeneroORM
from app.schemas.genero import GeneroCreate, GeneroUpdate
from typing import List, Optional

def create_genero(db: Session, genero: GeneroCreate) -> GeneroORM:
    """
    Añade un nuevo género a la base de datos.
    """
    db_genero = GeneroORM(**genero.model_dump())
    db.add(db_genero)
    db.commit()
    db.refresh(db_genero)
    return db_genero

def get_genero_by_id(db: Session, genero_id: int) -> Optional[GeneroORM]:
    """
    Busca un género por su ID.
    """
    return db.query(GeneroORM).filter(GeneroORM.id == genero_id).first()

def get_genero_by_nombre(db: Session, nombre: str) -> Optional[GeneroORM]:
    """
    Busca un género por su nombre (útil para evitar duplicados).
    """
    return db.query(GeneroORM).filter(GeneroORM.nombre == nombre).first()

def get_all_generos(db: Session) -> List[GeneroORM]:
    """
    Devuelve una lista de todos los géneros.
    """
    return db.query(GeneroORM).all()

def update_genero(db: Session, genero_id: int, genero_update: GeneroUpdate) -> Optional[GeneroORM]:
    """
    Actualiza un género existente.
    """
    db_genero = get_genero_by_id(db, genero_id)
    if not db_genero:
        return None
        
    update_data = genero_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_genero, key, value)
        
    db.commit()
    db.refresh(db_genero)
    return db_genero

def delete_genero(db: Session, genero_id: int) -> bool:
    """
    Elimina un género. (Si se configuró 'cascade', borrará sus películas).
    """
    db_genero = get_genero_by_id(db, genero_id)
    if db_genero:
        db.delete(db_genero)
        db.commit()
        return True
    return False

# --- Servicio Avanzado (Para el Schema Opcional) ---

def get_genero_with_peliculas(db: Session, genero_id: int) -> Optional[GeneroORM]:
    """
    Busca un género por ID y carga explícitamente sus películas
    asociadas para evitar el problema de "lazy loading" (N+1 query).
    """
    return db.query(GeneroORM).options(
        joinedload(GeneroORM.peliculas) # Carga proactiva
    ).filter(GeneroORM.id == genero_id).first()
    
# app/services/genero_service.py
from sqlalchemy import select

def delete_genero(db: Session, genero_id: int) -> bool:
    db_genero = get_genero_by_id(db, genero_id)
    if db_genero:
        # ⚠️ Verificación para PROHIBIR el borrado si hay películas (si la cascada no existiera)
        if db_genero.peliculas: # El atributo 'peliculas' se carga con el ORM
            print(f"ERROR: No se puede eliminar el género {genero_id} porque tiene películas asociadas.")
            return False

        db.delete(db_genero)
        db.commit()
        return True
    return False