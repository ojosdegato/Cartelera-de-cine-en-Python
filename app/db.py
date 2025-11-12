# app/db.py
# Configuración central de la base de datos (SQLAlchemy)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.orm import Session
import os
import sys

# --- CONFIGURACIÓN DE RUTAS ---
# Usamos la URL de la BBDD del plan
DATABAS_URL = "sqlite:///./cartelera_cine.db"
# Usamos una ruta relativa al DDL para el chequeo de la base de datos
SCHEMA_FILE_PATH = "cartelera_schema.sql" 


# 1. CLASE BASE Y MOTOR
engine = create_engine(DATABAS_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Función de utilidad (Inyección de Dependencia)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 2. CHEQUEO Y CREACIÓN DE ESQUEMA (DDL)
# Esta lógica se ejecuta al cargar el módulo 'app.db', antes que los Routers.
def initialize_database():
    """
    Función que crea la estructura de la base de datos si es la primera vez
    que se carga, utilizando el script DDL.
    """
    
    # ⚠️ Si el archivo .db no existe, debemos ejecutar el DDL y el DML (seeding)
    # Sin embargo, en esta capa, solo nos aseguraremos de que las tablas existan
    
    # Si desea usar Base.metadata.create_all (SOLUCIÓN A), descomente este bloque:
    # try:
    #     # Intenta obtener una conexión para verificar si la base de datos funciona.
    #     conn = engine.connect()
    #     conn.close()
    # except Exception as e:
    #     print(f"Error crítico de conexión: {e}")
    #     # Aquí debería haber un mecanismo para crear el archivo .db si no existe.
    #     pass
    
    # Para la arquitectura actual (DDL externo), la inicialización debe ejecutarse en main.py.
    # Si las tablas no se cargan, es porque el DDL externo no se ha ejecutado a tiempo.
    
    # SOLUCIÓN TEMPORAL: Crear un placeholder.
    # Si Base.metadata.create_all() fuera la fuente de verdad (lo cual no lo es en su proyecto)
    # Base.metadata.create_all(bind=engine)
    pass
    
# initialize_database()
"""""
# app/db.py
# Configuración central de la base de datos (SQLAlchemy)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.orm import Session

# Usamos la URL de la BBDD del plan
DATABAS_URL = "sqlite:///./cartelera_cine.db"

# check_same_thread es necesario solo para SQLite
engine = create_engine(DATABAS_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase Base de la que heredarán todos nuestros modelos ORM
class Base(DeclarativeBase):
    pass

# Función de utilidad (Inyección de Dependencia) para obtener
# una sesión de BBDD en cada petición de la API.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
"""""