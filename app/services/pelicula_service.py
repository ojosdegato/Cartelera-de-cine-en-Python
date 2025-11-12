# app/services/pelicula_service.py
# Lógica de negocio (CRUD) para el módulo de Películas

from sqlalchemy.orm import Session, joinedload
from app.models.pelicula import PeliculaORM
from app.schemas.pelicula import PeliculaCreate, PeliculaUpdate
from typing import List, Optional
from sqlalchemy import or_, String, func 




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


# Nueva función para aplicar los filtros dinámicos
def get_peliculas_filtradas(
    db: Session,
    genero_id: Optional[int] = None,
    duracion_max: Optional[int] = None,
    disponible: Optional[bool] = None # USAMOS BOOL
) -> List[PeliculaORM]:
    """
    Obtiene películas aplicando filtros dinámicos (género, duración, disponibilidad).
    """
    # 1. Iniciar la consulta base con eager loading para el género
    query = db.query(PeliculaORM).options(
        joinedload(PeliculaORM.genero)
    )

    # 2. Construir la lista de condiciones (filtros)
    filtros = []
    
    if genero_id is not None:
        filtros.append(PeliculaORM.genero_id == genero_id)
        
    if duracion_max is not None and duracion_max > 0:
        filtros.append(PeliculaORM.duracion <= duracion_max)
        
    # Aplicar filtro de Clasificación (Disponibilidad)
    # Si el valor es True, filtramos por disponible=True
    if disponible: 
        filtros.append(PeliculaORM.disponible == True)

    # 3. Aplicar todos los filtros y ejecutar la consulta
    # Aseguramos el orden alfabético para una mejor UX
    return query.filter(*filtros).order_by(PeliculaORM.titulo).all()

# Buscador
def get_peliculas_filtradas(
    db: Session,
    # Nuevo parámetro de búsqueda
    query: Optional[str] = None, 
    genero_id: Optional[int] = None,
    duracion_max: Optional[int] = None,
    disponible: Optional[bool] = None
) -> List[PeliculaORM]:
    """
    Obtiene películas aplicando filtros dinámicos y búsqueda de texto global.
    """
    # 1. Iniciar la consulta base
    query_stmt = db.query(PeliculaORM).options(
        joinedload(PeliculaORM.genero)
    )

    # 2. Construir la lista de condiciones (filtros)
    filtros = []
    
    # A. BÚSQUEDA GLOBAL (OR LÓGICO)
    if query:
        # Preparamos el término de búsqueda para LIKE (case-insensitive)
        # Convertimos la entrada del usuario a minúsculas, asegurando la uniformidad
        search_term = f"%{query.lower()}%" 
        
        # Usamos or_ para buscar la palabra clave en Título, Director y Descripción
        # Todos los campos de la DB también se convierten a minúsculas con func.lower()
        filtros.append(or_(
            func.lower(PeliculaORM.titulo).like(search_term),
            func.lower(PeliculaORM.director).like(search_term),
            func.lower(PeliculaORM.descripcion).like(search_term),
            # Lógica para Actores: Busca la coincidencia dentro del string JSON
            PeliculaORM.actores.like(search_term) 
        ))
    
    # B. FILTROS PARAMÉTRICOS (AND LÓGICO)
    if genero_id is not None:
        filtros.append(PeliculaORM.genero_id == genero_id)
        
    if duracion_max is not None and duracion_max > 0:
        filtros.append(PeliculaORM.duracion <= duracion_max)
        
    # El filtro 'disponible' (clasificación) solo se aplica si es True
    if disponible: 
        filtros.append(PeliculaORM.disponible == True)

    # 3. Aplicar todos los filtros y ejecutar la consulta
    return query_stmt.filter(*filtros).order_by(PeliculaORM.titulo).all()