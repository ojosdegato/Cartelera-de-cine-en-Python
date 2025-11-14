# app/config.py
# Contiene la configuración global de la aplicación,
# incluyendo el motor de plantillas Jinja2.

# Otras configuraciones globales pueden ir aquí en el futuro.

# Archivo de configuración central, rutas de infraestructura y metadatos.

import os
from fastapi.templating import Jinja2Templates
from pathlib import Path

# Obtener el directorio base para referencias de ruta
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. RUTAS DE ARCHIVOS DE INFRAESTRUCTURA (Movidas desde main.py)
#DB_FILE_PATH = "./database/cartelera_cine.db"
DB_FILE_PATH = "sqlite:///database/cartelera_cine.db"

#SCHEMA_FILE_PATH = "database/db.sql"
#SEED_FILE_PATH   = "database/db.sql"

BASE_DIR = Path(__file__).resolve().parent  # si config.py está en app/, esto es app/

SQL_PATH = BASE_DIR / "database" / "db.sql"

SCHEMA_FILE_PATH = str(SQL_PATH)
SEED_FILE_PATH   = str(SQL_PATH)

STATIC_DIR = "static" # Directorio para archivos estáticos


# 2. CONFIGURACIÓN DE JINJA2
# Apunta a la carpeta 'templates' que está un nivel arriba de 'app/config.py'
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "..", "templates"))


# 3. METADATOS DE LA APLICACIÓN (Movidos desde la instancia FastAPI en main.py)
APP_METADATA = {
    "title": "API Cartelera de Cine - javiercachon.com",
    "description": "Proyecto de Cartelera de Cine desarrollado con Python/FastAPI, SQLAlchemy y Jinja2. Un ejemplo de Software Libre y Excelencia Educativa.",
    "version": "1.0.0"
}