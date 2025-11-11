# app/main.py
# Punto de entrada principal de la aplicación FastAPI y Orquestación de la DB
# Lógica de Filtrado robusta para evitar errores 422.

import os
from fastapi import FastAPI, Depends, Query, Request 
from sqlalchemy import text 
from sqlalchemy.orm import Session 
from typing import Optional

# --- Importaciones de Infraestructura ---
from app.db import Base, engine, SessionLocal, get_db
from app.config import templates # Motor Jinja2

# --- Importaciones de Modelos y Módulos ---
from app.models import pelicula, genero # Necesario para DDL
from app.models.pelicula import PeliculaORM # Necesario para servicios
from app.models.genero import GeneroORM # Necesario para servicios
from app.routers import pelicula_router, genero_router 
# TODO: Importar los routers de sala, horario y venta aquí

from app.services import pelicula_service, genero_service


# --- RUTAS DE LOS ARCHIVOS ---
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


# --- ORQUESTACIÓN DE ARRANQUE (Inicialización de DB) ---
if not os.path.exists(DB_FILE_PATH):
    print("🚨 DB no encontrada. Creando y cargando esquema/datos iniciales.")
    db = SessionLocal()
    
    execute_sql_file(db, SCHEMA_FILE_PATH)
    execute_sql_file(db, SEED_FILE_PATH)
    
    db.close()
    print("✨ Base de datos inicializada correctamente.")


# --- INSTANCIA DE APLICACIÓN ---
app = FastAPI(
    title="API Cartelera de Cine",
    description="Proyecto desarrollado en Python + IA (FastAPI y SQLAlchemy)",
    version="1.0.0"
)


# --- ENDPOINT DE LA PÁGINA WEB (RUTA /) CON FILTROS ---

@app.get("/", tags=["Web UI"])
def homepage_cartelera(
    request: Request,
    db: Session = Depends(get_db),
    # Recibimos todos los parámetros como string opcional, que puede ser "" o None
    genero_id: Optional[str] = Query(None),
    duracion_max: Optional[str] = Query(None),
    disponible: Optional[str] = Query(None) # Recibe "True" o None
):
    """
    [GET] Ruta principal que muestra la cartelera, aplicando filtros dinámicos.
    """
    
    # 1. LIMPIEZA DE PARÁMETROS (Convierte "" a None y luego a INT)
    
    # Si genero_id es "" o None, es None. Si es dígito, se convierte a INT.
    clean_genero_id = int(genero_id) if genero_id and genero_id.isdigit() else None
    
    # Si duracion_max es "" o None, es None. Si es dígito, se convierte a INT.
    clean_duracion_max = int(duracion_max) if duracion_max and duracion_max.isdigit() else None
    
    # Checkbox: Solo es True si la URL contiene ?disponible=True
    filtro_disponible_bool = disponible == "True"

    
    # 2. Obtener la lista de películas filtradas usando el servicio
    peliculas = pelicula_service.get_peliculas_filtradas(
        db=db,
        genero_id=clean_genero_id,
        duracion_max=clean_duracion_max,
        disponible=filtro_disponible_bool
    )

    # 3. Obtener lista de géneros para rellenar el selector del filtro
    generos_disponibles = genero_service.get_all_generos(db)

    # 4. Crear un diccionario para mantener el estado de los filtros activos
    filtros_activos = {
        'genero_id': clean_genero_id,
        'duracion_max': clean_duracion_max,
        'disponible': filtro_disponible_bool
    }
    
    # 5. Renderizar la plantilla con los datos
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

# --- INCLUSIÓN DE ROUTERS ---

app.include_router(pelicula_router.router)
app.include_router(genero_router.router)
# app.include_router(sala_router.router)
# app.include_router(horario_router.router)
    
    