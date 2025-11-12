# Fichero: cartelera_cine.py
# Propósito: Definición centralizada y monolítica de todas las entidades del proyecto.
# NOTA: En la aplicación modular (app/main.py), estas clases residen en app/models/ y app/schemas/.

from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, sessionmaker, relationship
from sqlalchemy import String, Integer, Float, Boolean, create_engine, ForeignKey, JSON, DateTime, func
from typing import Optional, List, TYPE_CHECKING
import datetime
import time # Para simular la hora de los horarios

# URL de la base de datos para la demostración
DATABAS_URL = "sqlite:///./cartelera_cine.db"
engine = create_engine(DATABAS_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
app = FastAPI() # Instancia mínima de FastAPI

# ==============================================================================
# 1. CLASES BASE ORM (SQLAlchemy)
# ==============================================================================

class Base(DeclarativeBase):
    pass

# Declaraciones para relaciones bidireccionales
# NOTA: Es crucial que todas las clases se definan antes de Base.metadata.create_all
# para que SQLAlchemy pueda descubrir y crear todas las tablas.

# ==============================================================================
# 2. MODELOS ORM (Tablas de la Base de Datos)
# ==============================================================================


# --- ENTIDAD 1: GENERO (KARY) ---
class GeneroORM(Base):
    __tablename__ = "generos"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    descripcion: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # RELACIÓN 1-a-M (Bidireccional): Un género puede tener muchas películas
    peliculas: Mapped[List["PeliculaORM"]] = relationship(back_populates="genero", cascade="all, delete-orphan")


# --- ENTIDAD 2: PELICULA (JAVIER) ---
class PeliculaORM(Base):
    __tablename__ = "peliculas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    duracion: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # RELACIÓN M-a-1: Clave Foránea a Genero
    genero_id: Mapped[int] = mapped_column(ForeignKey("generos.id"), nullable=False)
    genero: Mapped["GeneroORM"] = relationship(back_populates="peliculas")

    # Columnas Opcionales
    director: Mapped[str | None] = mapped_column(String(100), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    trailer: Mapped[str | None] = mapped_column(String(255), nullable=True)
    productora: Mapped[str | None] = mapped_column(String(100), nullable=True)
    idioma: Mapped[str | None] = mapped_column(String(50), nullable=True)
    vose: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    actores: Mapped[list[str] | None] = mapped_column(JSON, nullable=True) # Lista almacenada como JSON
    
    disponible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


# --- ENTIDAD 3: SALA (REYES) ---
class SalaORM(Base):
    __tablename__ = "salas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    numero: Mapped[str] = mapped_column(String(50), nullable=False, unique=True) # ID o nombre de la sala
    capacidad: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False) # '2D', '3D', 'IMAX', 'Premium'
    precio_base: Mapped[float] = mapped_column(Float, nullable=False)
    disponible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


# --- ENTIDAD 4: SOCIO (MEJORA) ---
class SocioORM(Base):
    __tablename__ = "socios"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    fecha_registro: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relación 1-a-M: Un socio puede tener muchas ventas
    ventas: Mapped[List["VentaORM"]] = relationship(back_populates="socio", cascade="all, delete-orphan")


# --- ENTIDAD 5: HORARIO (MANUEL) ---
class HorarioORM(Base):
    __tablename__ = "horarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # RELACIONES FK (Qué se proyecta y dónde)
    pelicula_id: Mapped[int] = mapped_column(ForeignKey("peliculas.id"), nullable=False)
    sala_id: Mapped[int] = mapped_column(ForeignKey("salas.id"), nullable=False)

    # Detalle del Horario
    hora: Mapped[str] = mapped_column(String(20), nullable=False) # Simplificado a String para hh:mm
    disponible: Mapped[bool] = mapped_column(Boolean, nullable=False)


# --- ENTIDAD 6: VENTA (IÑAKI) ---
class VentaORM(Base):
    __tablename__ = "ventas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # RELACIONES FK
    horario_id: Mapped[int] = mapped_column(ForeignKey("horarios.id"), nullable=False)
    # RELACIÓN OPCIONAL con Socio (si la venta es de un socio registrado)
    socio_id: Mapped[int | None] = mapped_column(ForeignKey("socios.id"), nullable=True)
    socio: Mapped["SocioORM"] = relationship(back_populates="ventas")

    # Detalle de la Venta
    precio_total: Mapped[float] = mapped_column(Float, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    metodo_pago: Mapped[str] = mapped_column(String(50), nullable=False)


# ==============================================================================
# 3. MODELOS PYDANTIC (Esquemas de la API)
# ==============================================================================

# Estos modelos son usados por FastAPI para validación (ej: en POST/PUT requests)

class GeneroModel(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class PeliculaModel(BaseModel):
    titulo: str
    duracion: int
    genero_id: int
    director: Optional[str] = None
    descripcion: Optional[str] = None
    trailer: Optional[str] = None
    productora: Optional[str] = None
    idioma: Optional[str] = None
    vose: Optional[bool] = None
    actores: List[str]
    disponible: bool

class SalaModel(BaseModel):
    numero: str
    capacidad: int
    tipo: str
    precio_base: float
    disponible: bool
    
class SocioModel(BaseModel):
    nombre: str
    apellidos: str
    email: EmailStr
    telefono: Optional[str] = None
    activo: bool
    
class HorarioModel(BaseModel):
    pelicula_id: int
    sala_id: int
    hora: str
    disponible: bool
    
class VentaModel(BaseModel):
    horario_id: int
    socio_id: Optional[int] = None 
    precio_total: float
    cantidad: int
    metodo_pago: str


# ==============================================================================
# 4. CREACIÓN FORZADA DE TABLAS (DDL)
# ==============================================================================

# Si ejecuta este archivo de forma directa (como python cartelera_arquitectura.py),
# las siguientes líneas crearán todas las tablas en el archivo .db.
try:
    Base.metadata.create_all(bind=engine)
    print(f"✨ Todas las tablas han sido creadas en {DATABAS_URL}")
except Exception as e:
    print(f"❌ Error al crear tablas: {e}")