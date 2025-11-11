# setup_proyecto.py
# -----------------
# Script para generar automáticamente la estructura completa del proyecto
# 'Cartelera de Cine', incluyendo todos los módulos y el código
# desarrollado para Pelicula y Genero.
#
# Ejecutar con: python setup_proyecto.py
# -----------------

import os
import textwrap
from pathlib import Path

# --- Definición de la Estructura de Ficheros y su Contenido ---
# (Usamos textwrap.dedent para eliminar la indentación de los strings)

project_structure = {
    "app": {
        "__init__.py": "",
        
        "main.py": textwrap.dedent("""\
            # app/main.py
            # Punto de entrada principal de la aplicación FastAPI

            from fastapi import FastAPI
            from app.db import Base, engine
            from app.routers import pelicula_router, genero_router
            # TODO: Importar los routers de sala, horario y venta
            # from app.routers import sala_router, horario_router, venta_router

            # Creamos las tablas en la BBDD (si no existen)
            Base.metadata.create_all(bind=engine)

            # Instancia principal de la aplicación
            app = FastAPI(
                title="API Cartelera de Cine",
                description="Proyecto desarrollado en Python + IA (FastAPI y SQLAlchemy)",
                version="1.0.0"
            )

            # Incluimos los routers de los módulos
            app.include_router(pelicula_router.router)
            app.include_router(genero_router.router)
            # app.include_router(sala_router.router)
            # app.include_router(horario_router.router)
            # app.include_router(venta_router.router)

            @app.get("/", tags=["Root"])
            def read_root():
                return {"mensaje": "Bienvenido a la API de Cartelera de Cine 🍿"}
        """),
        
        "db.py": textwrap.dedent("""\
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
        """),

        "models": {
            "__init__.py": "",
            "pelicula.py": textwrap.dedent("""\
                # app/models/pelicula.py
                # Define la tabla 'peliculas' en la BBDD

                from sqlalchemy import String, Integer, Boolean, ForeignKey, JSON
                from sqlalchemy.orm import Mapped, mapped_column, relationship
                from app.db import Base # Importamos la Base declarativa

                # Importación de tipo para la relación bidireccional
                from typing import TYPE_CHECKING
                if TYPE_CHECKING:
                    from .genero import GeneroORM

                class PeliculaORM(Base):
                    __tablename__ = "peliculas"

                    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
                    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
                    genero_id: Mapped[int] = mapped_column(ForeignKey("generos.id"), nullable=False)
                    duracion: Mapped[int] = mapped_column(Integer, nullable=False)
                    disponible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

                    # --- Columnas Opcionales (nullable=True) ---
                    director: Mapped[str | None] = mapped_column(String(100), nullable=True)
                    descripcion: Mapped[str | None] = mapped_column(String(1000), nullable=True)
                    trailer: Mapped[str | None] = mapped_column(String(255), nullable=True)
                    productora: Mapped[str | None] = mapped_column(String(100), nullable=True)
                    idioma: Mapped[str | None] = mapped_column(String(50), nullable=True)
                    vose: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
                    actores: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)

                    # --- Relación Bidireccional (Lado "Many") ---
                    genero: Mapped["GeneroORM"] = relationship(back_populates="peliculas")
                    
                    def __repr__(self):
                        return f"<Pelicula(id={self.id}, titulo='{self.titulo}')>"
            """),
            "genero.py": textwrap.dedent("""\
                # app/models/genero.py
                # Define la tabla 'generos' en la BBDD

                from sqlalchemy import String, Integer
                from sqlalchemy.orm import Mapped, mapped_column, relationship
                from app.db import Base # Importamos la Base declarativa
                from typing import List, TYPE_CHECKING

                # Importación de tipo para la relación bidireccional
                if TYPE_CHECKING:
                    from .pelicula import PeliculaORM

                class GeneroORM(Base):
                    __tablename__ = "generos"

                    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
                    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
                    descripcion: Mapped[str | None] = mapped_column(String(500), nullable=True)

                    # --- Relación Bidireccional (Lado "One") ---
                    peliculas: Mapped[List["PeliculaORM"]] = relationship(
                        back_populates="genero",
                        cascade="all, delete-orphan"
                    )

                    def __repr__(self):
                        return f"<Genero(id={self.id}, nombre='{self.nombre}')>"
            """),
            "sala.py": "# TODO: Implementar el modelo SalaORM (Reyes)",
            "horario.py": "# TODO: Implementar el modelo HorarioORM (Manuel)",
            "venta.py": "# TODO: Implementar el modelo VentaORM (Iñaki)",
        },

        "schemas": {
            "__init__.py": "",
            "pelicula.py": textwrap.dedent("""\
                # app/schemas/pelicula.py
                # Define los modelos Pydantic (BaseModel) para validación en la API

                from pydantic import BaseModel, ConfigDict
                from typing import List, Optional

                class PeliculaBase(BaseModel):
                    titulo: str
                    duracion: int
                    disponible: bool
                    director: Optional[str] = None
                    descripcion: Optional[str] = None
                    trailer: Optional[str] = None
                    productora: Optional[str] = None
                    idioma: Optional[str] = None
                    vose: Optional[bool] = None
                    actores: Optional[List[str]] = None

                class PeliculaCreate(PeliculaBase):
                    genero_id: int

                class PeliculaUpdate(BaseModel):
                    titulo: Optional[str] = None
                    duracion: Optional[int] = None
                    disponible: Optional[bool] = None
                    genero_id: Optional[int] = None
                    director: Optional[str] = None
                    descripcion: Optional[str] = None
                    trailer: Optional[str] = None
                    productora: Optional[str] = None
                    idioma: Optional[str] = None
                    vose: Optional[bool] = None
                    actores: Optional[List[str]] = None

                class PeliculaRead(PeliculaBase):
                    id: int
                    genero_id: int
                    model_config = ConfigDict(from_attributes=True)
            """),
            "genero.py": textwrap.dedent("""\
                # app/schemas/genero.py
                # Define los modelos Pydantic (BaseModel) para validación en la API

                from pydantic import BaseModel, ConfigDict
                from typing import List, Optional
                from .pelicula import PeliculaRead # Importación para schema anidado

                class GeneroBase(BaseModel):
                    nombre: str
                    descripcion: Optional[str] = None

                class GeneroCreate(GeneroBase):
                    pass

                class GeneroUpdate(BaseModel):
                    nombre: Optional[str] = None
                    descripcion: Optional[str] = None

                class GeneroRead(GeneroBase):
                    id: int
                    model_config = ConfigDict(from_attributes=True)

                class GeneroReadWithPeliculas(GeneroRead):
                    peliculas: List[PeliculaRead] = []
            """),
            "sala.py": "# TODO: Implementar los schemas de Sala (Reyes)",
            "horario.py": "# TODO: Implementar los schemas de Horario (Manuel)",
            "venta.py": "# TODO: Implementar los schemas de Venta (Iñaki)",
        },

        "services": {
            "__init__.py": "",
            "pelicula_service.py": textwrap.dedent("""\
                # app/services/pelicula_service.py
                # Lógica de negocio (CRUD) para el módulo de Películas

                from sqlalchemy.orm import Session
                from app.models.pelicula import PeliculaORM
                from app.schemas.pelicula import PeliculaCreate, PeliculaUpdate
                from typing import List, Optional

                def add_pelicula(db: Session, pelicula: PeliculaCreate) -> PeliculaORM:
                    db_pelicula = PeliculaORM(**pelicula.model_dump())
                    db.add(db_pelicula)
                    db.commit()
                    db.refresh(db_pelicula)
                    return db_pelicula

                def get_peliculas_disponibles(db: Session) -> List[PeliculaORM]:
                    return db.query(PeliculaORM).filter(PeliculaORM.disponible == True).all()

                def get_all_peliculas(db: Session) -> List[PeliculaORM]:
                    return db.query(PeliculaORM).all()

                def get_pelicula_by_id(db: Session, pelicula_id: int) -> Optional[PeliculaORM]:
                    return db.query(PeliculaORM).filter(PeliculaORM.id == pelicula_id).first()

                def update_pelicula(db: Session, pelicula_id: int, pelicula_update: PeliculaUpdate) -> Optional[PeliculaORM]:
                    db_pelicula = get_pelicula_by_id(db, pelicula_id)
                    if not db_pelicula:
                        return None
                    update_data = pelicula_update.model_dump(exclude_unset=True)
                    for key, value in update_data.items():
                        setattr(db_pelicula, key, value)
                    db.commit()
                    db.refresh(db_pelicula)
                    return db_pelicula

                def delete_pelicula(db: Session, pelicula_id: int) -> bool:
                    db_pelicula = get_pelicula_by_id(db, pelicula_id)
                    if db_pelicula:
                        db.delete(db_pelicula)
                        db.commit()
                        return True
                    return False
            """),
            "genero_service.py": textwrap.dedent("""\
                # app/services/genero_service.py
                # Lógica de negocio (CRUD) para el módulo de Géneros

                from sqlalchemy.orm import Session, joinedload
                from app.models.genero import GeneroORM
                from app.schemas.genero import GeneroCreate, GeneroUpdate
                from typing import List, Optional

                def create_genero(db: Session, genero: GeneroCreate) -> GeneroORM:
                    db_genero = GeneroORM(**genero.model_dump())
                    db.add(db_genero)
                    db.commit()
                    db.refresh(db_genero)
                    return db_genero

                def get_genero_by_id(db: Session, genero_id: int) -> Optional[GeneroORM]:
                    return db.query(GeneroORM).filter(GeneroORM.id == genero_id).first()

                def get_genero_by_nombre(db: Session, nombre: str) -> Optional[GeneroORM]:
                    return db.query(GeneroORM).filter(GeneroORM.nombre == nombre).first()

                def get_all_generos(db: Session) -> List[GeneroORM]:
                    return db.query(GeneroORM).all()

                def update_genero(db: Session, genero_id: int, genero_update: GeneroUpdate) -> Optional[GeneroORM]:
                    db_genero = get_genero_by_id(db, genero_id)
                    if not db_genero:
                        return None
                    update_data = genero_update.model_dump(exclude_unset=True)
                    for key, value in update_data.items():
                        setattr(db_genero, key, value)
                    db.commit()
                    db.refresh(db_genero)
                    return db_genero

                def delete_genero(db: Session, genero_id: int) -> bool:
                    db_genero = get_genero_by_id(db, genero_id)
                    if db_genero:
                        db.delete(db_genero)
                        db.commit()
                        return True
                    return False

                def get_genero_with_peliculas(db: Session, genero_id: int) -> Optional[GeneroORM]:
                    return db.query(GeneroORM).options(
                        joinedload(GeneroORM.peliculas)
                    ).filter(GeneroORM.id == genero_id).first()
            """),
            "sala_service.py": "# TODO: Implementar los services de Sala (Reyes)",
            "horario_service.py": "# TODO: Implementar los services de Horario (Manuel)",
            "venta_service.py": "# TODO: Implementar los services de Venta (Iñaki)",
        },

        "routers": {
            "__init__.py": "",
            "pelicula_router.py": textwrap.dedent("""\
                # app/routers/pelicula_router.py
                # Define los endpoints de la API para el recurso 'Pelicula'

                from fastapi import APIRouter, Depends, HTTPException, status
                from sqlalchemy.orm import Session
                from typing import List

                from app.db import get_db
                from app.schemas.pelicula import PeliculaRead, PeliculaCreate, PeliculaUpdate
                from app.services import pelicula_service

                router = APIRouter(
                    prefix="/peliculas",
                    tags=["Películas 🎬"]
                )

                @router.post("/", response_model=PeliculaRead, status_code=status.HTTP_201_CREATED)
                def create_pelicula(
                    pelicula: PeliculaCreate, 
                    db: Session = Depends(get_db)
                ):
                    # TODO: Añadir verificación de que el genero_id existe
                    return pelicula_service.add_pelicula(db=db, pelicula=pelicula)

                @router.get("/disponibles/", response_model=List[PeliculaRead])
                def read_peliculas_disponibles(db: Session = Depends(get_db)):
                    return pelicula_service.get_peliculas_disponibles(db=db)

                @router.put("/{pelicula_id}", response_model=PeliculaRead)
                def update_pelicula_endpoint(
                    pelicula_id: int,
                    pelicula_update: PeliculaUpdate,
                    db: Session = Depends(get_db)
                ):
                    db_pelicula = pelicula_service.update_pelicula(db, pelicula_id, pelicula_update)
                    if db_pelicula is None:
                        raise HTTPException(status_code=404, detail="Película no encontrada")
                    return db_pelicula

                @router.delete("/{pelicula_id}", status_code=status.HTTP_204_NO_CONTENT)
                def delete_pelicula_endpoint(
                    pelicula_id: int,
                    db: Session = Depends(get_db)
                ):
                    success = pelicula_service.delete_pelicula(db, pelicula_id)
                    if not success:
                        raise HTTPException(status_code=404, detail="Película no encontrada")
            """),
            "genero_router.py": textwrap.dedent("""\
                # app/routers/genero_router.py
                # Define los endpoints de la API para el recurso 'Genero'

                from fastapi import APIRouter, Depends, HTTPException, status
                from sqlalchemy.orm import Session
                from typing import List

                from app.db import get_db
                from app.schemas.genero import GeneroRead, GeneroCreate, GeneroUpdate, GeneroReadWithPeliculas
                from app.services import genero_service

                router = APIRouter(
                    prefix="/generos",
                    tags=["Géneros 🎭"]
                )

                @router.post("/", response_model=GeneroRead, status_code=status.HTTP_201_CREATED)
                def create_genero_endpoint(
                    genero: GeneroCreate, 
                    db: Session = Depends(get_db)
                ):
                    db_genero = genero_service.get_genero_by_nombre(db, nombre=genero.nombre)
                    if db_genero:
                        raise HTTPException(status_code=400, detail="El nombre del género ya existe")
                    return genero_service.create_genero(db=db, genero=genero)

                @router.get("/", response_model=List[GeneroRead])
                def read_all_generos(db: Session = Depends(get_db)):
                    return genero_service.get_all_generos(db=db)

                @router.get("/{genero_id}", response_model=GeneroReadWithPeliculas)
                def read_genero_by_id_with_peliculas(
                    genero_id: int, 
                    db: Session = Depends(get_db)
                ):
                    db_genero = genero_service.get_genero_with_peliculas(db, genero_id)
                    if db_genero is None:
                        raise HTTPException(status_code=404, detail="Género no encontrado")
                    return db_genero

                @router.put("/{genero_id}", response_model=GeneroRead)
                def update_genero_endpoint(
                    genero_id: int,
                    genero_update: GeneroUpdate,
                    db: Session = Depends(get_db)
                ):
                    db_genero = genero_service.update_genero(db, genero_id, genero_update)
                    if db_genero is None:
                        raise HTTPException(status_code=404, detail="Género no encontrado")
                    return db_genero

                @router.delete("/{genero_id}", status_code=status.HTTP_204_NO_CONTENT)
                def delete_genero_endpoint(
                    genero_id: int,
                    db: Session = Depends(get_db)
                ):
                    success = genero_service.delete_genero(db, genero_id)
                    if not success:
                        raise HTTPException(status_code=404, detail="Género no encontrado")
            """),
            "sala_router.py": "# TODO: Implementar el router de Sala (Reyes)",
            "horario_router.py": "# TODO: Implementar el router de Horario (Manuel)",
            "venta_router.py": "# TODO: Implementar el router de Venta (Iñaki)",
        }
    },
    
    "requirements.txt": textwrap.dedent("""\
        fastapi==0.120.0
        uvicorn==0.38.0
        sqlalchemy==2.0.44
    """),

    ".gitignore": textwrap.dedent("""\
        # Bytecode de Python
        __pycache__/
        *.pyc
        
        # Bases de datos locales
        *.db
        *.db-journal*
        
        # Entornos virtuales
        venv/
        .venv/
        
        # Configuracion de IDEs
        .vscode/
        .idea/
        
        # Ficheros de OS
        .DS_Store
    """)
}

# --- Lógica del Script ---

def create_project(base_path, structure):
    """
    Función recursiva para crear carpetas y ficheros.
    """
    for name, content in structure.items():
        current_path = base_path / name
        if isinstance(content, dict):
            # Es una carpeta, crearla y entrar recursivamente
            current_path.mkdir(exist_ok=True)
            create_project(current_path, content)
        else:
            # Es un fichero, escribir el contenido
            try:
                with open(current_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Creado: {current_path}")
            except Exception as e:
                print(f"❌ Error creando {current_path}: {e}")

if __name__ == "__main__":
    # El script creará la estructura dentro de una carpeta 'cartelera_cine_proyecto'
    # para no llenar el directorio actual.
    
    project_root = Path.cwd() / "cartelera_cine"
    project_root.mkdir(exist_ok=True)
    
    print(f"Generando estructura del proyecto en: {project_root}\n")
    create_project(project_root, project_structure)
    print("\n¡Estructura del proyecto generada con éxito! 🚀")
