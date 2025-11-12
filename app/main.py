# app/main.py
# Punto de entrada principal de la aplicación FastAPI y Orquestación de la DB
# Incluye la lógica de montaje de archivos estáticos y la gestión de filtros robusta.

import os
from typing import Optional 
from fastapi import FastAPI, Depends, Query, Request 
from fastapi.staticfiles import StaticFiles # Necesario para archivos estáticos como favicon
from sqlalchemy import text 
from sqlalchemy.orm import Session 

from starlette.responses import HTMLResponse
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRoute
from starlette.exceptions import HTTPException as StarletteHTTPException # Necesario para atrapar errores de ruteo


# --- Importaciones de Infraestructura y Configuración ---
from app.db import Base, engine, SessionLocal, get_db
from app.config import templates # Motor Jinja2

# --- Importaciones de Modelos, Routers y Services ---
from app.models import pelicula, genero # Necesario para DDL
from app.models.pelicula import PeliculaORM
from app.models.genero import GeneroORM
from app.routers import pelicula_router, genero_router 
from app.services import pelicula_service, genero_service


# --- CONFIGURACIÓN Y RUTAS DE INFRAESTRUCTURA ---
DB_FILE_PATH = "./cartelera_cine.db"
SCHEMA_FILE_PATH = "cartelera_schema.sql"
SEED_FILE_PATH = "seed_data.sql"


# --- FUNCIÓN PARA EJECUTAR SQL (Mecanismo de carga) ---
def execute_sql_file(db_session, file_path):
    """Ejecuta todas las sentencias SQL contenidas en un archivo, reportando fallos."""
    if not os.path.exists(file_path):
        print(f"⚠️ Archivo SQL no encontrado: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    statements = [s.strip() for s in sql_script.split(';') if s.strip()]

    try:
        for statement in statements:
            db_session.execute(text(statement))
            
        db_session.commit()
        print(f"✅ SQL ejecutado: {file_path}.")
        return True
    
    except Exception as e:
        db_session.rollback()
        print(f"❌ Error crítico en SQL: {file_path}")
        print(f"   Sentencia que causó el error: {statement[:100]}...")
        print(f"   Error de DB: {e}")
        return False


# --- 1. INSTANCIA DE APLICACIÓN (Definición obligatoria al inicio) ---
app = FastAPI(
    title="API Cartelera de Cine",
    description="Proyecto desarrollado en Python + IA (FastAPI y SQLAlchemy)",
    version="1.0.0"
)

# --- MANEJO DE ERRORES GLOBAL (404 Not Found) ---

# Este manejador global captura errores de ruteo (404) y errores lanzados por el servidor.
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    """
    Maneja el error 404 (Not Found) y otros errores HTTP para servir nuestra plantilla HTML personalizada.
    """
    if exc.status_code == 404:
        # 1. Intentamos obtener la plantilla 404.html
        try:
            return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
        except:
            # 2. Si la plantilla falla, devolvemos una respuesta HTML simple
            return HTMLResponse("<h1>404 Not Found</h1><p>Error en el servidor de la aplicación.</p>", status_code=404)
    
    # Para otros errores (400, 500), usamos el manejo por defecto de FastAPI
    return await request.app.default_exception_handlers[exc.__class__](request, exc)

# Nota: El uso de 'request.app.default_exception_handlers' requiere que se use StarletteHTTPException.

# --- 2. MONTAJE DE ARCHIVOS ESTÁTICOS ---
# Necesario para el favicon.ico y futuros archivos CSS/JS
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except RuntimeError:
    print("⚠️ Advertencia: Creando directorio 'static/' para montaje.")
    os.makedirs("static", exist_ok=True)
    app.mount("/static", StaticFiles(directory="static"), name="static")


# --- 3. ORQUESTACIÓN DE ARRANQUE (Inicialización de DB) ---
if not os.path.exists(DB_FILE_PATH):
    print("🚨 DB no encontrada. Creando y cargando esquema/datos iniciales.")
    db = SessionLocal()
    
    execute_sql_file(db, SCHEMA_FILE_PATH)
    execute_sql_file(db, SEED_FILE_PATH)
    
    db.close()
    print("✨ Base de datos inicializada correctamente.")


# --- 4. INCLUSIÓN DE ROUTERS ---

app.include_router(pelicula_router.router)
app.include_router(genero_router.router)
# TODO: Incluir app.include_router(sala_router.router) y otros aquí


# --- 5. ENDPOINT DE LA PÁGINA WEB (RUTA /) CON FILTROS ---

@app.get("/", tags=["Web UI"])
def homepage_cartelera(
    request: Request,
    db: Session = Depends(get_db),
    # Recibimos el parámetro de búsqueda libre
    q: Optional[str] = Query(None), 
    # Recibimos parámetros de filtro como string opcional (para manejar "")
    genero_id: Optional[str] = Query(None),
    duracion_max: Optional[str] = Query(None),
    disponible: Optional[str] = Query(None)
):
    """
    [GET] Ruta principal que muestra la cartelera, aplicando filtros dinámicos.
    """
    
    # 1. LIMPIEZA DE PARÁMETROS (Convierte "" a None y luego a INT/BOOL)
    
    # Lógica de limpieza para evitar 422: si no es None Y es un dígito, conviertelo.
    clean_genero_id = int(genero_id) if genero_id and genero_id.isdigit() else None
    clean_duracion_max = int(duracion_max) if duracion_max and duracion_max.isdigit() else None
    
    # Checkbox de disponibilidad
    filtro_disponible_bool = disponible == "True"

    
    # 2. Obtener la lista de películas filtradas usando el servicio
    peliculas = pelicula_service.get_peliculas_filtradas(
        db=db,
        query=q, # <-- PASAMOS EL NUEVO TÉRMINO DE BÚSQUEDA
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
    
    # 4. Renderizar la plantilla con los datos
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