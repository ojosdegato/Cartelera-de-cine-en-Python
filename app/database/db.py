# app/database/db.py
from pathlib import Path
import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Rutas base
BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "cartelera_cine.db"   # /app/database/cartelera_cine.db
SQL_PATH = BASE_DIR / "db.sql"             # /app/database/db.sql

DATABASE_URL = f"sqlite:///{DB_PATH}"

# 2. Motor SQLAlchemy y sesión
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# 3. Base común para todos los modelos ORM
Base = declarative_base()


def init_db() -> None:
    """
    Inicializa la base de datos SOLO si no existe.

    - Crea el fichero cartelera_cine.db.
    - Crea las tablas a partir de los modelos ORM (Base.metadata.create_all).
    - Carga los datos de ejemplo desde db.sql (solo INSERT/PRAGMA).
    """
    if DB_PATH.exists():
        print(f"ℹ️ Base de datos encontrada en: {DB_PATH}")
        return

    print("🚨 DB no encontrada. Creando estructura y cargando datos iniciales...")

    # Crear carpeta database si no existe
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # 3.1. Importar modelos para registrar las tablas en Base.metadata
    try:
        # IMPORTANTE: aquí debes tener definidos tus modelos ORM
        # que heredan de Base: PeliculaORM, GeneroORM, SalaORM, HorarioORM,
        # VentaORM, LoginORM, SocioORM, etc.
        from app.models import (
            pelicula,
            genero,
            #sala,
            #horario,
            #venta,
            #socio,
            #login,
        )  # noqa: F401

    except ImportError as exc:
        print("⚠️ Aviso: no se pudieron importar todos los módulos de modelos ORM.")
        print(f"   Detalle: {exc}")
        print("   Solo se crearán las tablas de los modelos que sí estén cargados.")

    # 3.2. Crear tablas según los modelos ORM
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas mediante SQLAlchemy a partir de los modelos ORM.")

    # 3.3. Cargar datos iniciales desde db.sql (solo INSERT, sin CREATE TABLE)
    if not SQL_PATH.is_file():
        print(f"⚠️ Archivo de seed no encontrado: {SQL_PATH}. No se cargarán datos de ejemplo.")
        return

    conn = sqlite3.connect(DB_PATH)
    try:
        with SQL_PATH.open("r", encoding="utf-8") as f:
            sql_script = f.read()
        conn.executescript(sql_script)
        conn.commit()
        print(f"✅ Datos iniciales cargados correctamente desde: {SQL_PATH}")
    finally:
        conn.close()


# Ejecutar inicialización al importar el módulo
init_db()


def get_db():
    """
    Dependencia para FastAPI: abre una sesión de BD y la cierra al finalizar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
