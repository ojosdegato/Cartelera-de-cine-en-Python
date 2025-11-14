# app/db.py
from pathlib import Path
import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Directorio base del paquete app ( .../Cartelera-de-cine-en-Python/app )
BASE_DIR = Path(__file__).resolve().parent

# Rutas reales
DB_PATH = BASE_DIR / "database" / "cartelera_cine.db"
SQL_PATH = BASE_DIR / "database" / "db.sql"

# URL que usará SQLAlchemy (alineada con DB_PATH)
DATABASE_URL = f"sqlite:///{DB_PATH}"


def init_db() -> None:
    """
    Inicializa la base de datos SOLO si no existe.
    Si existe, no ejecuta el SQL otra vez ni muestra el mensaje de inicialización.
    """

    if DB_PATH.exists():
        print(f"ℹ️ Base de datos encontrada en: {DB_PATH}")
        return

    # Si llegamos aquí → la DB NO existe
    print("🚨 DB no encontrada. Creando y cargando esquema/datos iniciales.")

    if not SQL_PATH.is_file():
        print(f"❌ Archivo SQL no encontrado: {SQL_PATH}")
        return

    # Crear carpeta database si no existe
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Crear la base de datos y ejecutar el script SQL
    conn = sqlite3.connect(DB_PATH)
    try:
        with SQL_PATH.open("r", encoding="utf-8") as f:
            sql_script = f.read()
        conn.executescript(sql_script)
        conn.commit()
        print(f"✨ Base de datos inicializada correctamente desde: {SQL_PATH}")
    finally:
        conn.close()



# Inicializar la BBDD (si hace falta) antes de crear el engine
init_db()

# Configuración de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Necesario en SQLite + FastAPI
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    """
    Dependencia para FastAPI: abre una sesión por petición y la cierra al final.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
