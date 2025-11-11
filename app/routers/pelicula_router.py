# app/routers/pelicula_router.py
# Módulo de gestión de películas, incluyendo la lógica de la API REST y las vistas HTML (Jinja2).

from fastapi import APIRouter, Depends, HTTPException, status, Form 
from fastapi.requests import Request 
from fastapi.responses import RedirectResponse 
from sqlalchemy.orm import Session
from typing import List, Optional

# --- Importaciones Específicas del Proyecto (Rompiendo la Circularidad) ---
from app.db import get_db
from app.config import templates # Motor Jinja2, importado de un archivo de configuración
from app.schemas.pelicula import PeliculaRead, PeliculaCreate, PeliculaUpdate
from app.services import pelicula_service, genero_service 
from app.models.pelicula import PeliculaORM # Necesario para la firma de tipos en el servicio

# Creación del Router (Todas las rutas inician con /peliculas)
router = APIRouter(
    prefix="/peliculas",
    tags=["Películas 🎬"] # Etiqueta para la documentación de FastAPI
)

# ==============================================================================
# 1. RUTAS DE LA WEB UI (Jinja2) - CRUD Web
# ==============================================================================

# --- RUTA: CREAR PELÍCULA (GET: Muestra Formulario) ---
@router.get("/nueva", tags=["Web UI"])
def view_crear_pelicula(request: Request, db: Session = Depends(get_db)):
    """
    [GET] Muestra el formulario para crear una nueva película.
    """
    try:
        generos = genero_service.get_all_generos(db)
        return templates.TemplateResponse(
            "pelicula_form.html", 
            {
                "request": request,
                "titulo": "Añadir Nueva Película",
                "generos": generos,
                "pelicula": None,
                "accion": "crear"
            }
        )
    except Exception as e:
        print(f"Error al cargar el formulario de creación: {e}")
        raise HTTPException(status_code=500, detail="Error interno al cargar datos necesarios.")

# --- RUTA: CREAR PELÍCULA (POST: Procesa Formulario) ---
@router.post("/nueva", tags=["Web UI"], status_code=status.HTTP_303_SEE_OTHER)
def create_pelicula_from_form(
    db: Session = Depends(get_db),
    # Captura de datos del formulario (Form data)
    titulo: str = Form(...),
    duracion: int = Form(...),
    genero_id: int = Form(...),
    disponible: bool = Form(False),
    director: Optional[str] = Form(None),
    descripcion: Optional[str] = Form(None),
    trailer: Optional[str] = Form(None),
    productora: Optional[str] = Form(None),
    idioma: Optional[str] = Form(None),
    vose: bool = Form(False),
    actores: str = Form("[]")
):
    """
    [POST] Procesa los datos del formulario, valida, crea la nueva película y redirige.
    """
    try:
        if not genero_service.get_genero_by_id(db, genero_id):
            raise HTTPException(status_code=400, detail="Género ID no válido.")

        actores_list = [a.strip() for a in actores.split(',') if a.strip()] 

        pelicula_data = PeliculaCreate(
            titulo=titulo, duracion=duracion, genero_id=genero_id, disponible=disponible, 
            director=director if director else None, descripcion=descripcion if descripcion else None,
            trailer=trailer if trailer else None, productora=productora if productora else None,
            idioma=idioma if idioma else None, vose=vose, actores=actores_list
        )
        pelicula_service.add_pelicula(db, pelicula_data)
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error al crear película desde formulario: {e}")
        raise HTTPException(status_code=500, detail="Error interno al procesar la creación.")


# === RUTA: VER DETALLE (READ) ===
@router.get("/{pelicula_id}", tags=["Web UI"])
def view_pelicula_detalle(pelicula_id: int, request: Request, db: Session = Depends(get_db)):
    """
    [GET] Muestra el detalle de una película específica por su ID.
    """
    pelicula = pelicula_service.get_pelicula_detalle(db, pelicula_id)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    return templates.TemplateResponse(
        "pelicula_detalle.html", 
        {"request": request, "pelicula": pelicula}
    )

# === RUTA: EDITAR PELÍCULA (UPDATE - GET) ===
@router.get("/editar/{pelicula_id}", tags=["Web UI"])
def view_editar_pelicula(pelicula_id: int, request: Request, db: Session = Depends(get_db)):
    """
    [GET] Muestra el formulario con los datos pre-rellenados de una película existente.
    ESTA RUTA FALTABA Y CAUSABA EL ERROR 405.
    """
    try:
        # 1. Obtener la película y verificar su existencia
        pelicula = pelicula_service.get_pelicula_detalle(db, pelicula_id)
        if not pelicula:
            raise HTTPException(status_code=404, detail="Película no encontrada")
        
        # 2. Obtener la lista de géneros para el selector
        generos = genero_service.get_all_generos(db)

        # 3. Renderizar el formulario. Pasamos el objeto 'pelicula' para el pre-rellenado.
        return templates.TemplateResponse(
            "pelicula_form.html", 
            {
                "request": request,
                "titulo": f"Editar Película: {pelicula.titulo}",
                "generos": generos,
                "pelicula": pelicula,
                "accion": "editar"
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error al cargar formulario de edición para ID {pelicula_id}: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor.")


# === RUTA: EDITAR PELÍCULA (UPDATE - POST) ===
@router.post("/editar/{pelicula_id}", tags=["Web UI"], status_code=status.HTTP_303_SEE_OTHER)
def update_pelicula_from_form(
    pelicula_id: int,
    db: Session = Depends(get_db),
    # Captura de datos del formulario (Igual que en POST /nueva)
    titulo: str = Form(...), duracion: int = Form(...), genero_id: int = Form(...),
    disponible: bool = Form(False), director: Optional[str] = Form(None),
    descripcion: Optional[str] = Form(None), trailer: Optional[str] = Form(None),
    productora: Optional[str] = Form(None), idioma: Optional[str] = Form(None),
    vose: bool = Form(False), actores: str = Form("[]")
):
    """
    [POST] Procesa la actualización de los datos de una película existente.
    """
    try:
        if not genero_service.get_genero_by_id(db, genero_id):
            raise HTTPException(status_code=400, detail="Género ID no válido.")

        actores_list = [a.strip() for a in actores.split(',') if a.strip()]
        
        pelicula_update = PeliculaUpdate(
            titulo=titulo, duracion=duracion, genero_id=genero_id, disponible=disponible, 
            director=director if director else None, descripcion=descripcion if descripcion else None,
            trailer=trailer if trailer else None, productora=productora if productora else None,
            idioma=idioma if idioma else None, vose=vose, actores=actores_list
        )

        if not pelicula_service.update_pelicula(db, pelicula_id, pelicula_update):
            raise HTTPException(status_code=404, detail="Película no encontrada para actualizar.")

        return RedirectResponse(url=f"/peliculas/{pelicula_id}", status_code=status.HTTP_303_SEE_OTHER)

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error al actualizar película {pelicula_id} desde formulario: {e}")
        raise HTTPException(status_code=500, detail="Error interno al procesar la actualización.")
    
    # === RUTA: EJECUTAR ELIMINACIÓN (POST) ===
@router.post("/eliminar/{pelicula_id}", tags=["Web UI"], status_code=status.HTTP_303_SEE_OTHER)
def execute_eliminar_pelicula(pelicula_id: int, db: Session = Depends(get_db)):
    """
    [POST] Ejecuta el servicio de eliminación definitiva de la película.
    """
    try:
        success = pelicula_service.delete_pelicula(db, pelicula_id)
        if not success:
            # Si el servicio devuelve False (no encontrada o error)
            raise HTTPException(status_code=404, detail="Película no encontrada para eliminar.")

        # Redirige a la página principal después de la eliminación
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error al ejecutar eliminación de película ID {pelicula_id}: {e}")
        raise HTTPException(status_code=500, detail="Error interno al procesar la eliminación.")


# ==============================================================================
# 2. RUTAS DE LA API REST (JSON) - CRUD para Consumidores Externos
# ==============================================================================
# Nota: Estas rutas están pensadas para una aplicación cliente o para la documentación Swagger (JSON).

@router.post("/", response_model=PeliculaRead, status_code=status.HTTP_201_CREATED)
def create_pelicula_api(
    pelicula: PeliculaCreate, 
    db: Session = Depends(get_db)
):
    """
    [POST] Añade una nueva película a la cartelera (JSON Payload).
    """
    return pelicula_service.add_pelicula(db=db, pelicula=pelicula)

@router.get("/disponibles/", response_model=List[PeliculaRead])
def read_peliculas_disponibles_api(db: Session = Depends(get_db)):
    """
    [GET] Obtiene una lista de todas las películas actualmente disponibles (JSON).
    """
    # Usamos la función de servicio que obtiene todas las películas disponibles
    return pelicula_service.get_peliculas_disponibles(db=db) 

@router.put("/{pelicula_id}", response_model=PeliculaRead)
def update_pelicula_endpoint_api(
    pelicula_id: int,
    pelicula_update: PeliculaUpdate,
    db: Session = Depends(get_db)
):
    """
    [PUT] Actualiza los datos de una película existente por su ID (JSON Payload).
    """
    db_pelicula = pelicula_service.update_pelicula(db, pelicula_id, pelicula_update)
    if db_pelicula is None:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return db_pelicula


@router.delete("/{pelicula_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pelicula_endpoint_api(
    pelicula_id: int,
    db: Session = Depends(get_db)
):
    """
    [DELETE] Elimina una película de la base de datos por su ID.
    """
    success = pelicula_service.delete_pelicula(db, pelicula_id)
    if not success:
        raise HTTPException(status_code=404, detail="Película no encontrada")
