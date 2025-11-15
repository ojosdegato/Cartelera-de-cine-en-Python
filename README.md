
  <p align="center">
  <img src="banner_adecco.png" alt="HueteDevs banner" width="750" />
  </p>
   
# 🎬 Cartelera de Cine en Python

Bienvenido al repositorio oficial de **Cartelera de Cine**, una aplicación desarrollada en **Python** cuyo objetivo es gestionar de forma eficiente la cartelera digital de un cine.  
Este proyecto forma parte del aprendizaje del curso **Python + Inteligencia Artificial**, combinando programación estructurada, POO, bases de datos, APIs y arquitectura web moderna.

---

## 🚀 Finalidad del Proyecto
El sistema backend permite:
- 📌 Mostrar información de películas disponibles en cartelera.
- 🕒 Gestionar horarios y salas.
- 🎫 Administrar ventas de entradas y precios.
- 🎭 Organizar géneros y clasificaciones.
- 👥 Gestionar usuarios, autenticación y socios.
- 📚 Aplicar POO, estructuras de datos y buenas prácticas de desarrollo.
- ⚡ Integrar tecnologías modernas como **FastAPI** y **SQLAlchemy**.

---

## 👥 Equipo de Desarrollo
- Javier Cachón Garrido  
- Kary Haro Pérez  
- Manuel Jesús Marín García  
- Reyes Delestal Barrios  
- Iñaki Huete Montes  

---

## 🛠️ Tecnologías utilizadas
- Python 3  
- FastAPI  
- SQLAlchemy (ORM)  
- SQLite  
- Jinja2  
- Bootstrap 4/5  
- HTML5, CSS3, JavaScript  
- Visual Studio Code  

---

## 🏛️ Arquitectura del Sistema
El proyecto sigue una **arquitectura modular**, separando:
- Entidades de dominio (modelos).
- Lógica de negocio (servicios).
- Servicios web (endpoints y vistas).

📂 **Estructura del proyecto:**
. ├── app/ │ ├── main.py │ ├── models/ # Entidades (pelicula, genero, sala, horario, venta, socio, login) │ ├── routes/ # Endpoints CRUD por módulo │ ├── database/ # Configuración y base de datos SQLite │ ├── templates/ # Vistas HTML (Jinja2) │ └── static/ # Recursos estáticos (CSS, JS, imágenes) ├── requirements.txt ├── README.md └── run.py

Código

---

## 🎬 Entidades principales
- **Película** 🎞️ → Información de películas, relación con géneros y horarios.  
- **Sala** 🏟️ → Representa las salas físicas del cine.  
- **Horario** 🕒 → Sesiones de películas en salas y horarios específicos.  
- **Venta** 💳 → Registro de entradas vendidas y métodos de pago.  
- **Género** 🏷️ → Catálogo de géneros cinematográficos.  
- **Login / Usuario** 🔐 → Autenticación y roles de usuario.  
- **Socio / Fidelización** 👥 → Gestión de clientes registrados y programa de puntos.  

---

## 📦 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/HueteDevs/Proyecto_Adecco
   cd Proyecto_Adecco
Crear entorno virtual (opcional pero recomendado)

bash
# Linux / MacOS
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
Instalar dependencias

bash
pip install -r requirements.txt
▶️ Ejecución
Servidor de desarrollo con Uvicorn

bash
uvicorn app.main:app --reload
API disponible en:

Swagger UI → http://127.0.0.1:8000/docs

ReDoc → http://127.0.0.1:8000/redoc

Ejecución alternativa

bash
python run.py
🗄️ Base de Datos
Motor: SQLite (cartelera_cine.db)

Ubicación: app/database/

Inicialización:

bash
python -m app.cartelera_cine.db
Esto crea las tablas y carga datos de ejemplo (películas, horarios, etc.).

🌐 Endpoints principales
/peliculas → CRUD de películas y filtros.

/generos → Gestión de géneros.

/salas → Administración de salas.

/horarios → Gestión de sesiones.

/ventas → Registro de ventas y recaudación.

/socios → Alta y gestión de socios.

/auth → Registro, login y credenciales.

🚀 Futuras Mejoras
Sistema completo de compra de entradas (frontend + backend).

Panel de administración web.

Estadísticas avanzadas (ventas, ocupación, popularidad).

Machine Learning para recomendaciones personalizadas.

🤝 Contribuciones
Este proyecto está en constante evolución. Cada aportación suma: pull requests, issues y sugerencias son bienvenidas.

📜 Licencia
Este proyecto se distribuye bajo licencia MIT.
