# app/config.py
# Contiene la configuración global de la aplicación,
# incluyendo el motor de plantillas Jinja2.

import os
from fastapi.templating import Jinja2Templates

# Obtener el directorio base (la carpeta 'app')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Inicialización de la instancia de Jinja2Templates
# Se busca la carpeta 'templates' subiendo un nivel (..) desde 'app'.
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "..", "templates"))

# Otras configuraciones globales pueden ir aquí en el futuro.