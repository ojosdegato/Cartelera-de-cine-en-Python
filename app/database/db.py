from pathlib import Path
import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Directorio base del módulo database ( .../app/database )
BASE_DIR = Path(__file__).resolve().parent

# Rutas REALES
DB_PATH = BASE_DIR / "cartelera_cine.db"   # /app/database/cartelera_cine.db
SQL_PATH = BASE_DIR / "db.sql"             # /app/database/db.sql

# URL para SQLAlchemy
DATABASE_URL = f"sqlite:///{DB_PATH}"


def init_db() -> None:
    """
    Inicializa la base de datos SOLO si no existe.
    """
    if DB_PATH.exists():
        print(f"ℹ️ Base de datos encontrada en: {DB_PATH}")
        return

    print("🚨 DB no encontrada. Creando y cargando esquema/datos iniciales.")

    if not SQL_PATH.is_file():
        print(f"❌ Archivo SQL no encontrado: {SQL_PATH}")
        return

    # Crear carpeta database si no existe
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    try:
        with SQL_PATH.open("r", encoding="utf-8") as f:
            sql_script = f.read()
        conn.executescript(sql_script)
        conn.commit()
        print(f"✨ Base de datos inicializada correctamente desde: {SQL_PATH}")
    finally:
        conn.close()


# Ejecutar inicialización al importar el módulo
init_db()

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
