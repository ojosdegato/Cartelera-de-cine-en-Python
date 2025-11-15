
  <p align="center">
  <img src="banner_adecco.png" alt="HueteDevs banner" width="750" />
  </p>
   
🎥 Cartelera de Cine en Python

La magia del cine… programada en Python 🐍🍿

🛡️ Badges del Proyecto
<p align="center"> <img src="https://img.shields.io/badge/Python-3.12-blue" /> <img src="https://img.shields.io/badge/FastAPI-ASGI%20Framework-009688" /> <img src="https://img.shields.io/badge/SQLAlchemy-ORM-orange" /> <img src="https://img.shields.io/badge/SQLite-Database-lightgrey" /> <img src="https://img.shields.io/badge/Status-En%20desarrollo-yellow" /> </p>
1. Introducción

Bienvenido al repositorio oficial de Cartelera de Cine, una aplicación desarrollada en Python + FastAPI para gestionar la programación digital de un cine.
Combina POO, bases de datos, APIs REST, arquitectura modular y tecnologías modernas para su ejecución.

2. Finalidad del Proyecto

El backend permite:

📌 Mostrar películas en cartelera

🕒 Gestionar horarios y salas

🎫 Registrar ventas de entradas

🎭 Administrar géneros

👥 Gestionar usuarios, login y socios

🚀 Usar FastAPI + SQLAlchemy

📚 Aplicar POO, capas de negocio y buenas prácticas

3. Equipo de Desarrollo

Javier Cachón Garrido

Kary Haro Pérez

Manuel Jesús Marín García

Reyes Delestal Barrios

Iñaki Huete Montes

4. Tecnologías Utilizadas

Python 3

FastAPI

SQLAlchemy (ORM)

SQLite

Pydantic

Jinja2

Bootstrap 4/5

HTML / CSS / JavaScript

Visual Studio Code

5. Arquitectura General
┌──────────────────────────────┐
│            Cliente           │
│   Navegador / SPA / Móvil    │
└───────────────┬──────────────┘
                │ HTTP/JSON
                ▼
      ┌───────────────────────┐
      │        FastAPI        │
      │    (Controladores)    │
      └─────────────┬─────────┘
                    │
                    ▼
       ┌──────────────────────┐
       │       Servicios       │
       │   (Lógica negocio)    │
       └────────────┬──────────┘
                    │
                    ▼
      ┌────────────────────────┐
      │    SQLAlchemy (ORM)    │
      └──────────────┬─────────┘
                     │
                     ▼
        ┌──────────────────────┐
        │      SQLite DB       │
        └──────────────────────┘

6. Estructura del Proyecto
.
├── app/
│   ├── main.py
│   ├── models/
│   │   ├── pelicula.py
│   │   ├── genero.py
│   │   ├── sala.py
│   │   ├── horario.py
│   │   ├── venta.py
│   │   ├── socio.py
│   │   └── login.py
│   ├── routes/
│   │   ├── peliculas.py
│   │   ├── generos.py
│   │   ├── salas.py
│   │   ├── horarios.py
│   │   ├── ventas.py
│   │   ├── socios.py
│   │   └── login.py
│   ├── database/
│   │   ├── db.py
│   │   ├── db.sql
│   │   └── cartelera_cine.db
│   ├── templates/
│   │   ├── base.html
│   │   ├── peliculas/
│   │   ├── generos/
│   │   ├── salas/
│   │   ├── horarios/
│   │   ├── ventas/
│   │   ├── socios/
│   │   └── login/
│   └── static/
│       ├── css/
│       ├── js/
│       └── img/
├── requirements.txt
├── README.md
└── run.py

7. Modelo de Datos (ER Diagram)
generos (1) ────< (N) peliculas

peliculas (1) ────< (N) horarios >──── (1) salas

horarios (1) ────< (N) ventas

logins (1) ────(0..1) socios

socios (1) ────< (N) ventas    [opcional]

8. Entidades y Campos
🎞️ Pelicula
{
  "id": "int",
  "titulo": "string",
  "genero_id": "int",
  "duracion": "int",
  "director": "string",
  "descripcion": "string",
  "trailer": "string",
  "productora": "string",
  "idioma": "string",
  "VOSE": "boolean",
  "actores": "list<string>",
  "disponible": "boolean"
}

🏷️ Género
{
  "id": "int",
  "nombre": "string",
  "descripcion": "string"
}

🏟️ Sala
{
  "id": "int",
  "numero": "int",
  "capacidad": "int",
  "tipo": "normal|3D|IMAX|premium",
  "precio_base": "float"
}

🕒 Horario
{
  "id": "int",
  "pelicula_id": "int",
  "sala_id": "int",
  "hora": "datetime",
  "disponible": "boolean"
}

💳 Venta
{
  "id": "int",
  "horario_id": "int",
  "precio_total": "float",
  "cantidad": "int",
  "metodo_pago": "enum",
  "socio_id": "int (optional)"
}

🔐 Login
{
  "id": "int",
  "username": "string",
  "email": "string",
  "password_hash": "string",
  "rol": "usuario | administrador",
  "activo": "boolean",
  "bloqueado": "boolean",
  "creado_en": "datetime",
  "actualizado_en": "datetime"
}

👥 Socio
{
  "id": "int",
  "numero_socio": "string",
  "login_id": "int",
  "email": "string",
  "nivel": "Basic | Silver | Gold | VIP",
  "puntos": "int",
  "fecha_alta": "datetime",
  "activo": "boolean"
}

9. Instalación
git clone https://github.com/HueteDevs/Proyecto_Adecco
cd Proyecto_Adecco

Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

Instalar dependencias
pip install -r requirements.txt

10. Ejecución del Proyecto
Servidor de desarrollo
uvicorn app.main:app --reload

Documentación API

http://127.0.0.1:8000/docs
 (Swagger)

http://127.0.0.1:8000/redoc
 (ReDoc)

Alternativa
python run.py

11. Endpoints por Módulo
/peliculas   → CRUD completo
/generos     → Catálogo de géneros
/salas       → Gestión de salas
/horarios    → Programación del cine
/ventas      → Registro de ventas
/socios      → Fidelización
/auth        → Login y seguridad

12. Futuras Mejoras

Sistema completo de venta de entradas (frontend + backend)

Panel de administración

UI cinematográfica

Estadísticas avanzadas

Recomendador con IA

Tickets con QR

13. Licencia

MIT License.
