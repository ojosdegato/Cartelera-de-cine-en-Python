# app/services/pelicula_service.py
# Lógica de negocio (CRUD) para el módulo de Películas

from sqlalchemy.orm import Session, joinedload
from app.models.pelicula import PeliculaORM
from app.schemas.pelicula import PeliculaCreate, PeliculaUpdate
from typing import List, Optional
from sqlalchemy import or_, func, cast, String


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

# ESTA FUNCIÓN ES UN SERVICIO PURO, SIN DECORADORES DE FASTAPI
def get_pelicula_detalle(db: Session, pelicula_id: int) -> Optional[PeliculaORM]:
    """
    Obtiene una película por ID y carga eagerly el género asociado.
    """
    return db.query(PeliculaORM).options(
        joinedload(PeliculaORM.genero)
    ).filter(PeliculaORM.id == pelicula_id).first()


# Nueva función para aplicar los filtros dinámicos en buscador y genero
def get_peliculas_filtradas(
    db: Session,
    query: Optional[str] = None,
    genero_id: Optional[int] = None,
    duracion_max: Optional[int] = None,
    disponible: Optional[bool] = None,
) -> List[PeliculaORM]:
    """
    Obtiene películas aplicando de forma combinada:

    - Búsqueda de texto global (query) sobre:
        * título
        * director
        * descripción
        * actores (columna JSON, convertida a texto)
    - Filtro por género (genero_id)
    - Filtro por duración máxima (duracion_max)
    - Filtro por disponibilidad (disponible=True)

    Todos los filtros se combinan con AND.
    """
    # 1. Consulta base con eager loading del género
    query_stmt = db.query(PeliculaORM).options(
        joinedload(PeliculaORM.genero)
    )

    filtros = []

    # A) BÚSQUEDA GLOBAL (OR lógico)
    if query:
        term = f"%{query.lower()}%"

        filtros.append(
            or_(
                func.lower(PeliculaORM.titulo).like(term),
                func.lower(PeliculaORM.director).like(term),
                func.lower(PeliculaORM.descripcion).like(term),
                # Actores: la columna JSON se castea a texto y se busca ahí
                func.lower(cast(PeliculaORM.actores, String)).like(term),
            )
        )

    # B) FILTROS PARAMÉTRICOS (AND lógico)
    if genero_id is not None:
        filtros.append(PeliculaORM.genero_id == genero_id)

    if duracion_max is not None and duracion_max > 0:
        filtros.append(PeliculaORM.duracion <= duracion_max)

    # Si disponible es True, filtramos solo las disponibles; si es None/False, no filtramos
    if disponible:
        filtros.append(PeliculaORM.disponible == True)

    # 3) Aplicar filtros y ordenar
    return query_stmt.filter(*filtros).order_by(PeliculaORM.titulo).all()