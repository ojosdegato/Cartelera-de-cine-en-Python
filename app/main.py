
  # app/main.py
# Punto de entrada principal de la aplicación FastAPI.
# Contiene solo la orquestación, mounts, manejadores de error y el endpoint raíz.

import os
from typing import Optional 
from fastapi import FastAPI, Depends, Query, Request 
from fastapi.staticfiles import StaticFiles 
from sqlalchemy.orm import Session 

from starlette.responses import HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException # Para atrapar errores de ruteo

# --- Importaciones de Infraestructura y Utilidades (TODO MOVILIZADO) ---
# Importamos la configuración y las rutas
from app.config import templates, APP_METADATA, DB_FILE_PATH, SCHEMA_FILE_PATH, SEED_FILE_PATH, STATIC_DIR 
# Importamos el mecanismo de carga de SQL (de app/utils.py)
from app.utils import execute_sql_file 
# Importamos los componentes de la DB
from app.db import SessionLocal, get_db, Base, engine


# --- Importaciones de Modelos, Routers y Services ---
from app.models import pelicula, genero # Necesario para DDL
from app.routers import pelicula_router, genero_router 
from app.services import pelicula_service, genero_service


# -------------------------------------------------------------
# --- 1. INSTANCIA DE APLICACIÓN Y MANEJO DE ERRORES ---
# -------------------------------------------------------------

# A. INSTANCIA DE APLICACIÓN (Usando APP_METADATA de app/config.py)
app = FastAPI(**APP_METADATA)


# B. MANEJO DE ERRORES GLOBAL (404 Not Found)
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Maneja el error 404 (Not Found) y otros errores HTTP para servir nuestra plantilla HTML personalizada.
    """
    if exc.status_code == 404:
        try:
            # Usamos el objeto 'templates' importado de config
            return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
        except Exception:
            # Fallback en caso de que la plantilla 404.html no se pueda cargar
            return HTMLResponse("<h1>404 Not Found</h1><p>Error en el servidor de la aplicación.</p>", status_code=404)
    
    return await request.app.default_exception_handlers[exc.__class__](request, exc)


# -------------------------------------------------------------
# --- 2. MONTAJE DE ARCHIVOS ESTÁTICOS Y ORQUESTACIÓN ---
# -------------------------------------------------------------

# A. MONTAJE DE ARCHIVOS ESTÁTICOS (Usando STATIC_DIR de config)
try:
    app.mount(f"/{STATIC_DIR}", StaticFiles(directory=STATIC_DIR), name=STATIC_DIR)
except RuntimeError:
    print(f"⚠️ Advertencia: Creando directorio '{STATIC_DIR}/' para montaje.")
    os.makedirs(STATIC_DIR, exist_ok=True)
    app.mount(f"/{STATIC_DIR}", StaticFiles(directory=STATIC_DIR), name=STATIC_DIR)

# -------------------------------------------------------------
# --- 3. INCLUSIÓN DE ROUTERS Y ENDPOINT RAÍZ ---
# -------------------------------------------------------------

app.include_router(pelicula_router.router)
app.include_router(genero_router.router)
#app.include_router(sala_router.router)
#app.include_router(horario_router.router)
#app.include_router(venta_router.router)
#app.include_router(socio_router.router)
# TODO: Incluir app.include_router(sala_router.router) y otros aquí


@app.get("/", tags=["Web UI"])
def homepage_cartelera(
    request: Request,
    db: Session = Depends(get_db),
    q: Optional[str] = Query(None), 
    genero_id: Optional[str] = Query(None),
    duracion_max: Optional[str] = Query(None),
    disponible: Optional[str] = Query(None)
):
    """
    [GET] Ruta principal que muestra la cartelera, aplicando filtros dinámicos.
    """
    
    # 1. LIMPIEZA DE PARÁMETROS (La lógica se mantiene en el router para el manejo de Query params)
    clean_genero_id = int(genero_id) if genero_id and genero_id.isdigit() else None
    clean_duracion_max = int(duracion_max) if duracion_max and duracion_max.isdigit() else None
    filtro_disponible_bool = disponible == "True"

    
    # 2. Obtener la lista de películas filtradas usando el servicio
    peliculas = pelicula_service.get_peliculas_filtradas(
        db=db,
        query=q,
        genero_id=clean_genero_id,
        duracion_max=clean_duracion_max,
        disponible=filtro_disponible_bool
    )

    # 3. Obtener lista de géneros y crear el diccionario de filtros activos
    generos_disponibles = genero_service.get_all_generos(db)

    filtros_activos = {
        'q': q,
        'genero_id': clean_genero_id,
        'duracion_max': clean_duracion_max,
        'disponible': filtro_disponible_bool
    }
    
    # 4. Renderizar la plantilla
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "titulo": "Gestión de Cartelera - CRUD",
            "peliculas": peliculas,
            "generos": generos_disponibles, 
            "filtros_activos": filtros_activos 
        }
    )  