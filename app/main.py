import os
from fastapi import FastAPI, Depends, Query 
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlalchemy import text, select, or_ 
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List 

# Importaciones de configuración de DB
from app.db import Base, engine, SessionLocal, get_db

# Importaciones de modelos, routers y services
from app.models import pelicula, genero
from app.models.pelicula import PeliculaORM
from app.models.genero import GeneroORM
from app.routers import pelicula_router, genero_router 
from app.services import pelicula_service, genero_service 


# --- RUTAS Y CONFIGURACIÓN ---
DB_FILE_PATH = "./cartelera_cine.db"
SCHEMA_FILE_PATH = "cartelera_schema.sql"
SEED_FILE_PATH = "seed_data.sql"

# 1. CONFIGURACIÓN DE JINJA2: Apunta a la carpeta 'templates'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "..", "templates"))


# --- 2. FUNCIÓN PARA EJECUTAR SQL (Mecanismo de carga) ---
def execute_sql_file(db_session, file_path):
    """
    Ejecuta todas las sentencias SQL contenidas en un archivo.
    """
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


# --- 3. ORQUESTACIÓN DE ARRANQUE (Inicialización de DB) ---
if not os.path.exists(DB_FILE_PATH):
    print("🚨 DB no encontrada. Creando y cargando esquema/datos iniciales.")
    db = SessionLocal()
    
    # Paso A: Creación de Tablas (DDL)
    execute_sql_file(db, SCHEMA_FILE_PATH)
    
    # Paso B: Carga de Datos Semilla (DML)
    execute_sql_file(db, SEED_FILE_PATH)
    
    db.close()
    print("✨ Base de datos inicializada correctamente.")


# --- 4. INSTANCIA DE APLICACIÓN ---
app = FastAPI(
    title="API Cartelera de Cine",
    description="Proyecto desarrollado en Python + IA (FastAPI y SQLAlchemy)",
    version="1.0.0"
)

# --- 5. INCLUSIÓN DE RUTAS API ---
app.include_router(pelicula_router.router)
app.include_router(genero_router.router)
# ...

# --- 6. ENDPOINT DE LA PÁGINA WEB (RUTA /) CON FILTROS ---

@app.get("/", tags=["Web UI"])
def homepage_cartelera(
    request: Request, 
    db: Session = Depends(get_db),
    # Parámetros de consulta (Query Parameters)
    genero_id: Optional[int] = Query(None, description="Filtrar por ID de Género"),
    duracion_max: Optional[int] = Query(None, description="Máxima duración en minutos"),
    disponibilidad: Optional[str] = Query(None, description="Filtrar por Disponibilidad: 'disponible' o 'no_disponible'")
):
    """
    Ruta principal (/) que muestra la cartelera, aplicando filtros dinámicos.
    """
    
    # Construcción dinámica de la consulta
    stmt = (
        select(PeliculaORM)
        .options(joinedload(PeliculaORM.genero))
        .order_by(PeliculaORM.titulo) 
    )
    
    # Aplicar Filtro de Género
    if genero_id is not None:
        stmt = stmt.where(PeliculaORM.genero_id == genero_id)
        
    # Aplicar Filtro de Duración Máxima
    if duracion_max is not None and duracion_max > 0:
        stmt = stmt.where(PeliculaORM.duracion <= duracion_max)
        
    # Aplicar Filtro de Disponibilidad (Clasificación)
    if disponibilidad == "disponible":
        stmt = stmt.where(PeliculaORM.disponible == True)
    elif disponibilidad == "no_disponible":
        stmt = stmt.where(PeliculaORM.disponible == False)
    
    
    try:
        # Ejecutar la consulta filtrada
        peliculas = db.scalars(stmt).all()
        
        # Obtener todos los géneros para rellenar el selector del filtro HTML
        generos = db.query(GeneroORM).order_by(GeneroORM.nombre).all()
        
    except Exception as e:
        print(f"Error fatal al obtener datos con filtros: {e}")
        peliculas = []
        generos = []


    # Renderizar plantilla: Pasamos los datos y los filtros activos
    return templates.TemplateResponse(
        name="index.html", 
        context={
            "request": request, 
            "titulo": "Cartelera Oficial", 
            "peliculas": peliculas,
            "generos": generos, 
            "filtros_activos": {
                "genero_id": genero_id,
                "duracion_max": duracion_max,
                "disponibilidad": disponibilidad
            }
        }
    )