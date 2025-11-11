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
        
