# app/main.py
# Punto de entrada principal de la aplicación FastAPI y Orquestación de la DB

import os
from fastapi import FastAPI
from sqlalchemy import text # Necesario para ejecutar SQL raw

# Importaciones de configuración de DB
from app.db import Base, engine, SessionLocal

# Importaciones de modelos y routers (necesarias para el arranque y la funcionalidad)
from app.models import pelicula, genero
from app.models.pelicula import PeliculaORM
from app.models.genero import GeneroORM
from app.routers import pelicula_router, genero_router 
# TODO: Importar los routers de sala, horario y venta aquí


# --- RUTAS DE LOS ARCHIVOS ---
DB_FILE_PATH = "./cartelera_cine.db"
SCHEMA_FILE_PATH = "cartelera_schema.sql"
SEED_FILE_PATH = "seed_data.sql"


# --- 1. FUNCIÓN PARA EJECUTAR SQL (Mecanismo de carga) ---
def execute_sql_file(db_session, file_path):
    """
    Ejecuta todas las sentencias SQL contenidas en un archivo, reportando fallos.
    Esta versión maneja errores de forma explícita.
    """
    if not os.path.exists(file_path):
        print(f"⚠️ Archivo SQL no encontrado: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    # Separar comandos por punto y coma (;)
    statements = [s.strip() for s in sql_script.split(';') if s.strip()]

    try:
        # Ejecutar cada sentencia SQL
        for statement in statements:
            db_session.execute(text(statement))
            
        db_session.commit()
        print(f"✅ SQL ejecutado: {file_path}.")
        return True
    
    except Exception as e:
        db_session.rollback()
        print(f"❌ Error crítico en SQL: {file_path}")
        # IMPRIME LA SENTENCIA QUE FALLÓ para facilitar la Depuración Guiada
        print(f"   Sentencia que causó el error: {statement[:100]}...")
        print(f"   Error de DB: {e}")
        return False


# --- 2. ORQUESTACIÓN DE ARRANQUE DE LA APLICACIÓN ---

# Chequeo: Si el archivo de la base de datos no existe, lo creamos e inicializamos.
# Esto garantiza que el esquema y los datos se carguen solo una vez.
if not os.path.exists(DB_FILE_PATH):
    print("🚨 DB no encontrada. Creando y cargando esquema/datos iniciales.")
    db = SessionLocal()
    
    # Paso A: Creación de Tablas (DDL)
    execute_sql_file(db, SCHEMA_FILE_PATH)
    
    # Paso B: Carga de Datos Semilla (DML)
    execute_sql_file(db, SEED_FILE_PATH)
    
    db.close()
    print("✨ Base de datos inicializada correctamente.")


# --- 3. INSTANCIA DE APLICACIÓN ---

app = FastAPI(
    title="API Cartelera de Cine",
    description="Proyecto desarrollado en Python + IA (FastAPI y SQLAlchemy)",
    version="1.0.0"
)

# --- 4. INCLUSIÓN DE RUTAS ---

app.include_router(pelicula_router.router)
app.include_router(genero_router.router)
# app.include_router(sala_router.router)
# app.include_router(horario_router.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"mensaje": "Bienvenido a la API de Cartelera de Cine 🍿"}